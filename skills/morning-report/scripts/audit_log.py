#!/usr/bin/env python3
"""Append Morning Report audit events as JSONL."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_AUDIT_LOG = SKILL_DIR / "state" / "audit.log"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def append_audit(
    action: str,
    *,
    details: dict[str, Any] | None = None,
    by: str = "agent",
    log_path: Path = DEFAULT_AUDIT_LOG,
) -> dict[str, Any]:
    record = {
        "ts": utc_now(),
        "action": action,
        "by": by,
        "details": details or {},
    }
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def parse_details(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("--details must be a JSON object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a Morning Report audit event")
    parser.add_argument("--action", required=True)
    parser.add_argument("--details", help="JSON object")
    parser.add_argument("--by", default="agent")
    parser.add_argument("--log", default=str(DEFAULT_AUDIT_LOG))
    args = parser.parse_args()

    try:
        record = append_audit(
            args.action,
            details=parse_details(args.details),
            by=args.by,
            log_path=Path(args.log),
        )
    except Exception as exc:
        print(f"audit_log.py failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
