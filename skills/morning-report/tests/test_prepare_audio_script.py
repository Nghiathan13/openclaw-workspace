import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "prepare_audio_script.py"


class PrepareAudioScriptTests(unittest.TestCase):
    def run_helper(self, markdown: str, *args: str) -> tuple[dict, str]:
        with tempfile.TemporaryDirectory() as tmp:
            report_file = Path(tmp) / "report.md"
            output_file = Path(tmp) / "audio.txt"
            report_file.write_text(markdown, encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--report-file",
                    str(report_file),
                    "--output",
                    str(output_file),
                    *args,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            return json.loads(result.stdout), output_file.read_text(encoding="utf-8")

    def test_removes_markdown_urls_tables_and_media_directive(self):
        metadata, audio = self.run_helper(
            "# Morning Brief — Test\n\n"
            "| Source | URL |\n"
            "| --- | --- |\n"
            "| Example | https://example.com |\n\n"
            "- **Key update:** [Demand rose](https://example.com/story).\n"
            "MEDIA:/tmp/morning-report.mp3\n"
        )

        self.assertTrue(metadata["success"])
        self.assertIn("Morning Brief", audio)
        self.assertIn("Key update: Demand rose.", audio)
        self.assertNotIn("https://", audio)
        self.assertNotIn("MEDIA:", audio)
        self.assertNotIn("|", audio)

    def test_truncates_at_max_words(self):
        markdown = "# Report\n\n" + " ".join(f"word{i}." for i in range(20))
        metadata, audio = self.run_helper(markdown, "--max-words", "10")

        self.assertTrue(metadata["truncated"])
        self.assertLessEqual(metadata["word_count"], 10)
        self.assertLessEqual(len(audio.split()), 10)


if __name__ == "__main__":
    unittest.main()
