#!/usr/bin/env python3
"""Record a Morning Report run into report history."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_HISTORY_DIR = SKILL_DIR / "state" / "report-history"
DEFAULT_AUDIT_LOG = SKILL_DIR / "state" / "audit.log"
DEFAULT_STATE = SKILL_DIR / "state" / "current-topics.md"
DEFAULT_USER = SKILL_DIR.parent.parent / "USER.md"

sys.path.insert(0, str(SCRIPT_DIR))
from audit_log import append_audit  # noqa: E402
from config_status import build_status  # noqa: E402


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def copy_if_present(src: Path | None, dest: Path) -> str | None:
    if src is None:
        return None
    if not src.exists():
        raise FileNotFoundError(f"missing file: {src}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    return str(dest)


def load_json_file(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    if not path.exists():
        raise FileNotFoundError(f"missing file: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON file must contain an object: {path}")
    return data


def make_run_dir(history_dir: Path, report_text: str, now: datetime) -> Path:
    digest = hashlib.sha256(report_text.encode("utf-8")).hexdigest()[:8]
    date_dir = history_dir / now.strftime("%Y-%m-%d")
    base_name = f"{now.strftime('%H%M%S')}-{digest}"
    candidate = date_dir / base_name
    suffix = 1
    while candidate.exists():
        suffix += 1
        candidate = date_dir / f"{base_name}-{suffix}"
    candidate.mkdir(parents=True, exist_ok=False)
    return candidate


def parse_json_arg(raw: str | None, label: str) -> Any:
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} must be valid JSON") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Record a Morning Report run")
    parser.add_argument("--report-file", required=True)
    parser.add_argument("--history-dir", default=str(DEFAULT_HISTORY_DIR))
    parser.add_argument("--audit-log", default=str(DEFAULT_AUDIT_LOG))
    parser.add_argument("--state", default=str(DEFAULT_STATE))
    parser.add_argument("--user", default=str(DEFAULT_USER))
    parser.add_argument("--audio-script-file")
    parser.add_argument("--audio-file")
    parser.add_argument("--audio-manifest")
    parser.add_argument("--audio-status", default="not_requested")
    parser.add_argument("--delivery-status", default="not_recorded")
    parser.add_argument("--source-url", action="append", default=[])
    parser.add_argument("--failed-url", action="append", default=[])
    parser.add_argument("--extra", help="Optional JSON object merged into manifest.extra")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    now = utc_now()

    try:
        report_path = Path(args.report_file)
        report_text = read_text_file(report_path)
        if not report_text.strip():
            raise ValueError("report file is empty")

        state_status = build_status(Path(args.state), Path(args.user))
        prefs = state_status.get("state", {}).get("report_preferences", {})

        if args.dry_run:
            preview = {
                "success": True,
                "dry_run": True,
                "created_at": now.isoformat(),
                "planned_history_dir": str(Path(args.history_dir)),
                "report_sha256": hashlib.sha256(report_text.encode("utf-8")).hexdigest(),
                "report_char_count": len(report_text),
                "topics": state_status.get("state", {}).get("active_topics", []),
                "optional_topics": state_status.get("state", {}).get("optional_topics", []),
                "report_preferences": prefs,
                "delivery_channel": prefs.get("Delivery channel", ""),
                "delivery_status": args.delivery_status,
                "audio_status": args.audio_status,
                "source_urls": args.source_url,
                "failed_urls": args.failed_url,
                "source_count": len(args.source_url),
                "failed_url_count": len(args.failed_url),
                "config_status": state_status,
                "extra": parse_json_arg(args.extra, "--extra") or {},
            }
            print(json.dumps(preview, ensure_ascii=False, indent=2))
            return 0

        run_dir = make_run_dir(Path(args.history_dir), report_text, now)
        local_report = run_dir / "report.md"
        local_report.write_text(report_text, encoding="utf-8")

        audio_script_path = copy_if_present(
            Path(args.audio_script_file) if args.audio_script_file else None,
            run_dir / "audio-script.txt",
        )
        audio_file_path = copy_if_present(
            Path(args.audio_file) if args.audio_file else None,
            run_dir / "morning-report.mp3",
        )
        audio_manifest = load_json_file(Path(args.audio_manifest) if args.audio_manifest else None)
        if audio_manifest is not None:
            (run_dir / "audio-manifest.json").write_text(
                json.dumps(audio_manifest, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        extra = parse_json_arg(args.extra, "--extra") or {}
        if not isinstance(extra, dict):
            raise ValueError("--extra must be a JSON object")

        manifest = {
            "success": True,
            "created_at": now.isoformat(),
            "run_dir": str(run_dir),
            "report_file": str(local_report),
            "report_sha256": hashlib.sha256(report_text.encode("utf-8")).hexdigest(),
            "report_char_count": len(report_text),
            "topics": state_status.get("state", {}).get("active_topics", []),
            "optional_topics": state_status.get("state", {}).get("optional_topics", []),
            "report_preferences": prefs,
            "delivery_channel": prefs.get("Delivery channel", ""),
            "delivery_status": args.delivery_status,
            "audio_status": args.audio_status,
            "audio_script_file": audio_script_path,
            "audio_file": audio_file_path,
            "audio_manifest_file": str(run_dir / "audio-manifest.json") if audio_manifest is not None else None,
            "source_urls": args.source_url,
            "failed_urls": args.failed_url,
            "source_count": len(args.source_url),
            "failed_url_count": len(args.failed_url),
            "config_status": state_status,
            "extra": extra,
        }
        audit_record = append_audit(
            "report_recorded",
            by="record_report.py",
            log_path=Path(args.audit_log),
            details={
                "run_dir": str(run_dir),
                "topics": manifest["topics"],
                "audio_status": args.audio_status,
                "delivery_status": args.delivery_status,
                "source_count": len(args.source_url),
                "failed_url_count": len(args.failed_url),
            },
        )
        manifest["audit_record"] = audit_record
        (run_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(f"record_report.py failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
