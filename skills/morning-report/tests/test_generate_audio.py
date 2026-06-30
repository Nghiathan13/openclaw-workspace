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

    def test_language_alias_maps_vietnamese_to_vi(self):
        data = self.run_audio(
            "Chao buoi sang. Day la ban tom tat am thanh ngan.",
            "--lang",
            "Vietnamese",
        )

        self.assertEqual(data["requested_lang"], "Vietnamese")
        self.assertEqual(data["lang"], "vi")


if __name__ == "__main__":
    unittest.main()
