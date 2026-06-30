import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
UPDATE_SCRIPT = SKILL_DIR / "scripts" / "update_config.py"
STATUS_SCRIPT = SKILL_DIR / "scripts" / "config_status.py"


class ConfigHelperTests(unittest.TestCase):
    def test_setup_writes_state_and_user_preferences(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            state = tmp_path / "current-topics.md"
            user = tmp_path / "USER.md"
            audit = tmp_path / "audit.log"
            user.write_text("# USER\n\nExisting content.\n", encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    str(UPDATE_SCRIPT),
                    "--state",
                    str(state),
                    "--user",
                    str(user),
                    "--audit-log",
                    str(audit),
                    "setup",
                    "--topic",
                    "Vietnam real estate",
                    "--delivery-time",
                    "7:00 AM",
                    "--timezone",
                    "Asia/Ho_Chi_Minh",
                    "--report-style",
                    "Concise",
                    "--report-language",
                    "Vietnamese",
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

            status = subprocess.run(
                [
                    sys.executable,
                    str(STATUS_SCRIPT),
                    "--state",
                    str(state),
                    "--user",
                    str(user),
                    "--check",
                    "--compact",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            data = json.loads(status.stdout)

            self.assertTrue(data["configured"])
            self.assertEqual(data["missing_required"], [])
            self.assertEqual(data["state"]["active_topics"], ["Vietnam real estate"])
            self.assertEqual(data["user"]["morning_report_preferences"]["Status"], "enabled")
            self.assertIn("Existing content.", user.read_text(encoding="utf-8"))
            audit_records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(audit_records[-1]["action"], "config_updated")

    def test_status_check_fails_when_required_config_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            state = tmp_path / "current-topics.md"
            user = tmp_path / "USER.md"
            state.write_text(
                "# Current Topics\n\n"
                "## Setup status\n\n"
                "Status: not_configured\n\n"
                "## Active topics\n\n"
                "None provided.\n",
                encoding="utf-8",
            )
            user.write_text("# USER\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(STATUS_SCRIPT),
                    "--state",
                    str(state),
                    "--user",
                    str(user),
                    "--check",
                    "--compact",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            data = json.loads(result.stdout)
            self.assertFalse(data["configured"])
            self.assertIn("Status: configured", data["missing_required"])
            self.assertIn("Active topics", data["missing_required"])


if __name__ == "__main__":
    unittest.main()
