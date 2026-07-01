import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
PREFLIGHT_SCRIPT = SKILL_DIR / "scripts" / "preflight.py"
UPDATE_SCRIPT = SKILL_DIR / "scripts" / "update_config.py"


def run_preflight(tmp_path: Path, *extra_args: str, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            str(PREFLIGHT_SCRIPT),
            "--state",
            str(tmp_path / "current-topics.md"),
            "--user",
            str(tmp_path / "USER.md"),
            "--audio-history",
            str(tmp_path / "audio-history"),
            "--report-history",
            str(tmp_path / "report-history"),
            "--no-cli",
            "--compact",
            *extra_args,
        ],
        capture_output=True,
        text=True,
        check=check,
    )


class PreflightTests(unittest.TestCase):
    def test_missing_state_is_not_configured_but_environment_can_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "USER.md").write_text("# USER\n", encoding="utf-8")

            result = run_preflight(tmp_path, check=True)
            data = json.loads(result.stdout)

            self.assertTrue(data["success"])
            self.assertTrue(data["environment_ok"])
            self.assertFalse(data["configured"])
            self.assertFalse(data["ready_to_run"])
            self.assertIn("morning_report_not_configured", data["warnings"])
            self.assertEqual(data["checks"]["openclaw_cli"]["skipped"], True)

    def test_configured_state_is_ready_when_environment_checks_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "USER.md").write_text("# USER\n", encoding="utf-8")
            subprocess.run(
                [
                    sys.executable,
                    str(UPDATE_SCRIPT),
                    "--state",
                    str(tmp_path / "current-topics.md"),
                    "--user",
                    str(tmp_path / "USER.md"),
                    "--audit-log",
                    str(tmp_path / "audit.log"),
                    "setup",
                    "--topic",
                    "Indonesia cuisine",
                    "--delivery-time",
                    "7:00 AM",
                    "--timezone",
                    "Asia/Ho_Chi_Minh",
                    "--report-style",
                    "Concise",
                    "--report-language",
                    "English",
                    "--audio-summary",
                    "Enabled",
                    "--delivery-channel",
                    "Telegram",
                    "--user-status",
                    "enabled",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            result = run_preflight(tmp_path, "--check", check=True)
            data = json.loads(result.stdout)

            self.assertTrue(data["environment_ok"])
            self.assertTrue(data["configured"])
            self.assertTrue(data["ready_to_run"])
            self.assertEqual(data["problems"], [])


if __name__ == "__main__":
    unittest.main()
