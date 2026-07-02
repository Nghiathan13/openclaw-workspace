import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "generate_audio.py"


class GenerateAudioTests(unittest.TestCase):
    def run_audio(self, text: str, *args: str) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            text_file = Path(tmp) / "audio.txt"
            text_file.write_text(text, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--text-file", str(text_file), "--dry-run", *args],
                capture_output=True,
                text=True,
                check=True,
            )
            return json.loads(result.stdout)

    def test_dry_run_splits_under_chunk_limit(self):
        data = self.run_audio(
            "Chao buoi sang. "
            "Thi truong bat dong san Viet Nam co nhieu tin hieu can theo doi, "
            "bao gom nguon cung, tin dung, ha tang va thanh khoan thuc te. "
            "Nguoi mua nen kiem tra phap ly du an truoc khi quyet dinh.",
            "--chunk-limit",
            "80",
            "--lang",
            "vi",
        )

        self.assertTrue(data["success"])
        self.assertGreater(data["chunk_count"], 1)
        self.assertTrue(all(len(chunk) <= 80 for chunk in data["chunks"]))
        self.assertFalse(data["length_ok"])
        self.assertTrue(any(item.startswith("under_min_words") for item in data["length_warnings"]))

    def test_language_alias_maps_english_to_en(self):
        data = self.run_audio(
            "Good morning. This is a short audio summary.",
            "--lang",
            "English",
        )

        self.assertEqual(data["requested_lang"], "English")
        self.assertEqual(data["lang"], "en")

    def test_length_metadata_reports_target_range(self):
        text = " ".join(f"word{i}" for i in range(460))
        data = self.run_audio(text, "--lang", "English", "--min-words", "450", "--max-words", "750")

        self.assertEqual(data["word_count"], 460)
        self.assertEqual(data["target_min_words"], 450)
        self.assertEqual(data["target_max_words"], 750)
        self.assertTrue(data["length_ok"])
        self.assertEqual(data["length_warnings"], [])

    def test_language_is_required_to_avoid_implicit_voice_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            text_file = Path(tmp) / "audio.txt"
            text_file.write_text("Good morning. This is a short audio summary.", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--text-file", str(text_file), "--dry-run"],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--lang", result.stderr)


if __name__ == "__main__":
    unittest.main()
