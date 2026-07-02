import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
UPDATE_SCRIPT = SKILL_DIR / "scripts" / "update_config.py"
RECORD_SCRIPT = SKILL_DIR / "scripts" / "record_report.py"
HISTORY_SCRIPT = SKILL_DIR / "scripts" / "history_status.py"


class ReportHistoryTests(unittest.TestCase):
    def test_config_update_record_report_and_history_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            state = tmp_path / "current-topics.md"
            user = tmp_path / "USER.md"
            audit = tmp_path / "audit.log"
            history = tmp_path / "report-history"
            report = tmp_path / "report.md"
            report.write_text(
                "# Morning Report — Test\n\nShort report body with one sourced claim.\n",
                encoding="utf-8",
            )
            user.write_text("# USER\n", encoding="utf-8")

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
                    "English",
                    "--audio-summary",
                    "Disabled",
                    "--delivery-channel",
                    "Telegram",
                    "--user-status",
                    "enabled",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
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
                    "replace-topics",
                    "--topic",
                    "Vietnam stock market",
                    "--sync-user",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            recorded = subprocess.run(
                [
                    sys.executable,
                    str(RECORD_SCRIPT),
                    "--report-file",
                    str(report),
                    "--history-dir",
                    str(history),
                    "--audit-log",
                    str(audit),
                    "--state",
                    str(state),
                    "--user",
                    str(user),
                    "--audio-status",
                    "disabled",
                    "--delivery-status",
                    "prepared",
                    "--source-url",
                    "https://example.com/source",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            manifest = json.loads(recorded.stdout)
            run_dir = Path(manifest["run_dir"])

            self.assertTrue((run_dir / "report.md").exists())
            self.assertTrue((run_dir / "manifest.json").exists())
            self.assertEqual(manifest["topics"], ["Vietnam stock market"])
            self.assertEqual(manifest["audio_status"], "disabled")
            self.assertEqual(manifest["source_count"], 1)
            self.assertIn("audit_record", manifest)

            audit_records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
            self.assertEqual([record["action"] for record in audit_records], [
                "config_updated",
                "config_updated",
                "report_recorded",
            ])

            status = subprocess.run(
                [
                    sys.executable,
                    str(HISTORY_SCRIPT),
                    "--report-history",
                    str(history),
                    "--audio-history",
                    str(tmp_path / "audio-history"),
                    "--audit-log",
                    str(audit),
                    "--limit",
                    "1",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            data = json.loads(status.stdout)
            self.assertEqual(data["report_history"][0]["topics"], ["Vietnam stock market"])
            self.assertEqual(data["audit_tail"][0]["action"], "report_recorded")

    def test_record_report_dry_run_does_not_write_history_or_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            state = tmp_path / "current-topics.md"
            user = tmp_path / "USER.md"
            audit = tmp_path / "audit.log"
            history = tmp_path / "report-history"
            report = tmp_path / "report.md"
            report.write_text("# Morning Report — Dry Run\n", encoding="utf-8")
            user.write_text("# USER\n", encoding="utf-8")

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
                    "AI agents",
                    "--delivery-time",
                    "7:00 AM",
                    "--timezone",
                    "Asia/Ho_Chi_Minh",
                    "--report-style",
                    "Concise",
                    "--report-language",
                    "English",
                    "--audio-summary",
                    "Disabled",
                    "--delivery-channel",
                    "Telegram",
                    "--user-status",
                    "enabled",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            audit.unlink()

            result = subprocess.run(
                [
                    sys.executable,
                    str(RECORD_SCRIPT),
                    "--report-file",
                    str(report),
                    "--history-dir",
                    str(history),
                    "--audit-log",
                    str(audit),
                    "--state",
                    str(state),
                    "--user",
                    str(user),
                    "--dry-run",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            data = json.loads(result.stdout)

            self.assertTrue(data["dry_run"])
            self.assertFalse(history.exists())
            self.assertFalse(audit.exists())


if __name__ == "__main__":
    unittest.main()
