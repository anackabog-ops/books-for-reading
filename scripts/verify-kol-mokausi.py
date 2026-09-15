#!/usr/bin/env python3
"""Check complete reader data and prepared SSML; optionally verify generated MP3s."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("chapter_audio", ROOT / "scripts/generate-chapter-audio.py")
audio = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audio)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(book_path, casting_path, prepared, require_audio=False):
    book = json.loads(book_path.read_text(encoding="utf-8"))
    cast = json.loads(casting_path.read_text(encoding="utf-8"))
    require(book["id"] == "kol-mokausi-gyventi", "Wrong book")
    require(cast.get("bookId") == book["id"], "Wrong casting book")
    require(len(book["chapters"]) == 18, "Expected all 18 chapters")
    require(set(cast["chapters"]) == {c["id"] for c in book["chapters"]}, "Casting coverage mismatch")
    words = units = notes = recordings = 0
    for number, chapter in enumerate(book["chapters"], 1):
        label = chapter["id"]
        require(label == f"chapter-{number}", "Chapter order/ID mismatch")
        require(bool(chapter.get("practice", "").strip()), f"{label}: missing practice")
        items = [i for b in chapter["blocks"] for i in b["items"]]
        units += len(items)
        for index, item in enumerate(items, 1):
            location = f"{label}, item {index}"
            count = len(re.findall(r"[^\W\d_]+(?:[-’'][^\W\d_]+)*", audio.plain_text(item["text"])))
            lines = [s for s in item.get("note", "").splitlines() if s.strip()]
            require(count > 0, f"{location}: no words")
            require(len(lines) == count, f"{location}: {count} words but {len(lines)} notes")
            require(bool(re.search("[А-Яа-яЁё]", item.get("translation", ""))), f"{location}: missing Russian translation")
            require(all(re.match(r"^\*\*[^*]+\*\*(?: → \*\*[^*]+\*\*)? — .+", line) for line in lines), f"{location}: malformed note")
            words += count
            notes += len(lines)
        c = cast["chapters"][label]
        ssml, phrases = audio.build_ssml(chapter, c.get("femaleBlocks", []), c.get("narratorSpans", {}),
                                         c.get("narratorVoice", "lt-LT-LeonasNeural"), c.get("blockVoices", {}))
        digest = hashlib.sha256(ssml.encode()).hexdigest()
        saved = prepared / label / f"{digest}.ssml"
        require(saved.is_file() and saved.read_text(encoding="utf-8") == ssml, f"{label}: missing/stale SSML")
        xml = ET.fromstring(ssml)
        marks = [e.attrib["mark"] for e in xml.iter() if e.tag.endswith("}bookmark")]
        require(marks == [p["mark"] for p in phrases], f"{label}: bookmark coverage/order")
        require(len(set(marks)) == len(items), f"{label}: duplicate bookmarks")
        normalize = lambda s: re.sub(r"\s+", " ", s).strip()
        require(normalize("".join(xml.itertext())) == normalize(" ".join(p["text"] for p in phrases)),
                f"{label}: spoken text differs")
        if require_audio:
            directory = ROOT / "assets/audio" / book["id"] / label
            manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
            require(manifest["sourceSha256"] == digest, f"{label}: stale audio")
            require(manifest["timingVersion"] == audio.AUDIO_TIMING_VERSION, f"{label}: stale timing")
            require(manifest["voiceSwitchGapSeconds"] == audio.VOICE_SWITCH_GAP_SECONDS, f"{label}: wrong voice gap")
            require(len(manifest["phrases"]) == len(items), f"{label}: audio coverage")
            end = 0
            paths = [chapter.get("audio")]
            for expected, actual, item in zip(phrases, manifest["phrases"], items):
                for key in ("mark", "block", "item", "text", "voice", "segments"):
                    require(actual.get(key) == expected.get(key), f"{label}: audio {key} mismatch")
                require(actual["start"] == end and actual["end"] > end, f"{label}: noncontiguous timing")
                end = actual["end"]
                require(item.get("audio") == actual["audio"], f"{label}: clip link mismatch")
                paths.append(item.get("audio"))
            require(end == manifest["duration"] and end > 0, f"{label}: chapter duration mismatch")
            require(paths[0] == str(directory.relative_to(ROOT) / "chapter.mp3"), f"{label}: chapter path mismatch")
            for src in paths:
                require(isinstance(src, str), f"{label}: missing audio path")
                target = (ROOT / src).resolve()
                require(target.parent == directory.resolve() and target.suffix == ".mp3", f"{label}: invalid audio path")
                require(target.is_file() and target.stat().st_size > 0, f"{label}: missing/empty MP3")
                subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(target), "-f", "null", "-"],
                               check=True, stdout=subprocess.DEVNULL)
                recordings += 1
    require((words, units, notes) == (5947, 963, 5947), "Full source totals changed; review against PDF")
    require(book["wordCount"] == words, "Book word count mismatch")
    catalog = json.loads((ROOT / "books/catalog.json").read_text(encoding="utf-8"))
    entries = [b for b in catalog["books"] if b["id"] == book["id"]]
    require(len(entries) == 1 and entries[0]["wordCount"] == words, "Catalog count/entry mismatch")
    require(bool(book.get("appendices")), "Missing source appendix")
    return dict(chapters=18, units=units, words=words, notes=notes,
                preparedSSML=18, decodedMP3s=recordings,
                limitations=["Structural checks do not certify linguistic accuracy.",
                             "Samira pronunciation and mobile/listening review remain pending."])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared-dir", required=True, type=Path)
    parser.add_argument("--require-audio", action="store_true")
    args = parser.parse_args()
    report = validate(ROOT / "books/kol-mokausi-gyventi.json",
                      ROOT / "author-plans/kol-mokausi-gyventi-casting.json",
                      args.prepared_dir, args.require_audio)
    (args.prepared_dir / "verification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
