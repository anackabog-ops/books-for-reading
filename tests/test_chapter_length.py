import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/generate-chapter-audio.py"
spec = importlib.util.spec_from_file_location("chapter_audio_length", SCRIPT)
audio = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audio)
LIMITS = {"target": 800, "min": 700, "max": 900}


def chapter(words):
    return {"blocks": [{"items": [{"text": words, "translation": "ещё сто слов", "note": "словарь"}]}]}


class ChapterLengthTest(unittest.TestCase):
    def test_counts_only_narrative_and_preserves_accented_words(self):
        self.assertTrue(hasattr(audio, "chapter_word_count"), "chapter length check is missing")
        self.assertEqual(7, audio.chapter_word_count(chapter("— Ąžuolas, ėmė, ūžė. Tòmas grį̃žo. Ačiū! vis-à-vis 123")))

    def test_rejects_short_and_long_chapters_including_the_original_failure(self):
        self.assertTrue(hasattr(audio, "validate_chapter_length"), "chapter length gate is missing")
        for count in (328, 699, 901):
            with self.subTest(count=count), self.assertRaisesRegex(ValueError, "700–900"):
                audio.validate_chapter_length(chapter("žodis " * count), LIMITS)
        for count in (700, 800, 900):
            self.assertEqual(count, audio.validate_chapter_length(chapter("žodis " * count), LIMITS))

    def test_latest_chapter_matches_the_restored_agreement(self):
        self.assertTrue(hasattr(audio, "chapter_word_count"), "chapter length check is missing")
        book = json.loads((ROOT / "books/jusu-iprastas-uzsakymas.json").read_text())
        count = audio.chapter_word_count(book["chapters"][-1])
        self.assertGreaterEqual(count, 700, "a short scene is not the agreed complete chapter")
        self.assertLessEqual(count, 900)

    def test_length_only_check_does_not_need_speech_or_a_work_directory(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(ROOT / "books/jusu-iprastas-uzsakymas.json"),
             "--chapter", "8", "--check-length-only", "--credentials", "/nonexistent/credentials.json"],
            capture_output=True, text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("target 800", result.stdout)

    def test_short_chapter_is_rejected_before_credentials_or_synthesis(self):
        with tempfile.TemporaryDirectory() as directory:
            book = Path(directory) / "book.json"
            book.write_text(json.dumps({"id": "jusu-iprastas-uzsakymas", "chapters": [chapter("žodis " * 328)]}))
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(book), "--chapter", "1", "--work-dir", directory,
                 "--credentials", "/nonexistent/credentials.json"], capture_output=True, text=True,
            )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("328", result.stderr)
        self.assertIn("700–900", result.stderr)
        self.assertNotIn("Synthesizing", result.stdout)

    def test_other_books_do_not_inherit_this_books_length_requirement(self):
        with tempfile.TemporaryDirectory() as directory:
            book = Path(directory) / "book.json"
            book.write_text(json.dumps({"id": "another-book", "chapters": [chapter("žodis " * 328)]}))
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(book), "--chapter", "1"], capture_output=True, text=True,
            )
        self.assertIn("--work-dir is required", result.stderr)
        self.assertNotIn("chapter length", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
