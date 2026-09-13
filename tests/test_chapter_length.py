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
LIMITS = {"min": 400, "max": 800}


def chapter(words):
    return {"blocks": [{"items": [{"text": words, "translation": "ещё сто слов", "note": "словарь"}]}]}


class ChapterLengthTest(unittest.TestCase):
    def test_counts_only_narrative_and_preserves_accented_words(self):
        self.assertEqual(7, audio.chapter_word_count(chapter("— Ąžuolas, ėmė, ūžė. Tòmas grį̃žo. Ačiū! vis-à-vis 123")))

    def test_usual_range_has_no_single_target(self):
        self.assertTrue(hasattr(audio, "chapter_length_report"), "advisory length report is missing")
        for count in (400, 600, 800):
            with self.subTest(count=count):
                report = audio.chapter_length_report(chapter("žodis " * count), LIMITS)
                self.assertIn(str(count), report)
                self.assertIn("400–800", report)
                self.assertNotIn("review", report.lower())
                self.assertNotIn("target", report.lower())

    def test_outliers_request_editorial_review_without_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            book = Path(directory) / "book.json"
            for count in (328, 399, 801):
                with self.subTest(count=count):
                    book.write_text(json.dumps({"id": "jusu-iprastas-uzsakymas", "chapters": [chapter("žodis " * count)]}))
                    result = subprocess.run(
                        [sys.executable, str(SCRIPT), str(book), "--chapter", "1", "--check-length-only",
                         "--credentials", "/nonexistent/credentials.json"], capture_output=True, text=True,
                    )
                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertIn(str(count), result.stdout)
                    self.assertIn("400–800", result.stdout)
                    self.assertIn("editorial review", result.stdout.lower())
                    self.assertNotIn("Synthesizing", result.stdout)

    def test_synthesis_path_reports_short_chapter_without_length_rejection(self):
        with tempfile.TemporaryDirectory() as directory:
            book = Path(directory) / "book.json"
            book.write_text(json.dumps({"id": "jusu-iprastas-uzsakymas", "chapters": [chapter("žodis " * 328)]}))
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(book), "--chapter", "1"], capture_output=True, text=True,
            )
        self.assertIn("328", result.stdout)
        self.assertIn("editorial review", result.stdout.lower())
        self.assertIn("--work-dir is required", result.stderr)

    def test_other_books_do_not_inherit_this_books_length_guidance(self):
        with tempfile.TemporaryDirectory() as directory:
            book = Path(directory) / "book.json"
            book.write_text(json.dumps({"id": "another-book", "chapters": [chapter("žodis " * 328)]}))
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(book), "--chapter", "1"], capture_output=True, text=True,
            )
        self.assertIn("--work-dir is required", result.stderr)
        self.assertNotIn("Chapter length", result.stdout)


if __name__ == "__main__":
    unittest.main()
