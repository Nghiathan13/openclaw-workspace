#!/usr/bin/env python3
"""Check Morning Report runtime readiness.

The helper reports deterministic JSON so the agent can distinguish missing
setup, local runtime issues, and optional audio/cron capabilities.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
WORKSPACE = SKILL_DIR.parent.parent
DEFAULT_STATE = SKILL_DIR / "state" / "current-topics.md"
DEFAULT_USER = WORKSPACE / "USER.md"
DEFAULT_AUDIO_HISTORY = SKILL_DIR / "state" / "audio-history"
DEFAULT_REPORT_HISTORY = SKILL_DIR / "state" / "report-history"
GOOGLE_TTS_URL = "https://translate.google.com/translate_tts"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)

sys.path.insert(0, str(SCRIPT_DIR))
from config_status import build_status  # noqa: E402


def command_result(cmd: list[str], timeout: int) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "ok": completed.returncode == 0,
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip()[:1000],
            "stderr": completed.stderr.strip()[:1000],
        }
    except FileNotFoundError as exc:
        return {"ok": False, "error": str(exc)}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timeout after {timeout}s"}


def check_python() -> dict[str, Any]:
    return {
        "ok": True,
        "executable": sys.executable,
        "version": sys.version.split()[0],
    }


def check_openclaw(timeout: int) -> dict[str, Any]:
    path = shutil.which("openclaw")
    result: dict[str, Any] = {"ok": bool(path), "path": path}
    if not path:
        result["error"] = "openclaw CLI not found on PATH"
        return result
    help_check = command_result(["openclaw", "--help"], timeout)
    result["help_check"] = help_check
    result["ok"] = bool(help_check.get("ok"))
    return result


def check_cron_help(timeout: int) -> dict[str, Any]:
    if not shutil.which("openclaw"):
        return {"ok": False, "error": "openclaw CLI not found on PATH"}
    return command_result(["openclaw", "cron", "--help"], timeout)


def check_cron_status(timeout: int) -> dict[str, Any]:
    if not shutil.which("openclaw"):
        return {"ok": False, "error": "openclaw CLI not found on PATH"}
    result = command_result(["openclaw", "cron", "status"], timeout)
    combined = f"{result.get('stdout', '')}\n{result.get('stderr', '')}"
    if "GatewaySecretRefUnavailableError" in combined:
        result["secret_ref_unavailable"] = True
        result["hint"] = (
            "cron CLI reached a gateway-auth path that cannot resolve secrets; "
            "use a gateway-resolved command path or supported --token."
        )
    return result


def check_writable_dir(path: Path, *, write_check: bool) -> dict[str, Any]:
    result: dict[str, Any] = {"path": str(path), "exists": path.exists()}
    try:
        path.mkdir(parents=True, exist_ok=True)
        result["exists"] = path.exists()
        result["is_dir"] = path.is_dir()
        if write_check:
            with tempfile.NamedTemporaryFile(prefix=".preflight-", dir=path, delete=False) as handle:
                tmp_path = Path(handle.name)
                handle.write(b"ok")
            tmp_path.unlink(missing_ok=True)
            result["writable"] = True
        else:
            result["writable"] = os.access(path, os.W_OK)
        result["ok"] = bool(result["is_dir"] and result["writable"])
    except Exception as exc:
        result["ok"] = False
        result["error"] = str(exc)
    return result


def check_paths(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "state_dir": check_writable_dir(Path(args.state).parent, write_check=not args.no_write_check),
        "audio_history": check_writable_dir(Path(args.audio_history), write_check=not args.no_write_check),
        "report_history": check_writable_dir(Path(args.report_history), write_check=not args.no_write_check),
    }


def check_audio_runtime(check_tts: bool, timeout: int) -> dict[str, Any]:
    result: dict[str, Any] = {
        "curl": {"ok": bool(shutil.which("curl")), "path": shutil.which("curl")},
        "ffmpeg": {
            "ok": bool(shutil.which("ffmpeg")),
            "path": shutil.which("ffmpeg"),
            "required": False,
        },
        "google_tts": {"checked": False},
    }
    if not check_tts:
        return result

    params = urllib.parse.urlencode(
        {
            "ie": "UTF-8",
            "client": "tw-ob",
            "tl": "en",
            "q": "Morning Report audio test.",
        }
    )
    request = urllib.request.Request(
        f"{GOOGLE_TTS_URL}?{params}",
        headers={"User-Agent": DEFAULT_USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = response.read(512)
        result["google_tts"] = {
            "checked": True,
            "ok": len(data) > 128,
            "bytes_sampled": len(data),
        }
    except urllib.error.HTTPError as exc:
        result["google_tts"] = {"checked": True, "ok": False, "error": f"HTTP {exc.code}"}
    except Exception as exc:
        result["google_tts"] = {"checked": True, "ok": False, "error": str(exc)}
    return result


def build_preflight(args: argparse.Namespace) -> dict[str, Any]:
    config = build_status(Path(args.state), Path(args.user))
    checks: dict[str, Any] = {
        "python": check_python(),
        "paths": check_paths(args),
        "config": config,
        "audio_runtime": check_audio_runtime(args.check_tts, args.timeout),
    }

    if args.no_cli:
        checks["openclaw_cli"] = {"ok": None, "skipped": True}
        checks["cron_help"] = {"ok": None, "skipped": True}
    else:
        checks["openclaw_cli"] = check_openclaw(args.timeout)
        checks["cron_help"] = check_cron_help(args.timeout)

    if args.check_cron_status:
        checks["cron_status"] = check_cron_status(args.timeout)

    problems: list[str] = []
    warnings: list[str] = []

    if not checks["python"].get("ok"):
        problems.append("python_unavailable")
    for name in ["state_dir", "audio_history", "report_history"]:
        if not checks["paths"][name].get("ok"):
            problems.append(f"{name}_not_writable")
    if not args.no_cli:
        if not checks["openclaw_cli"].get("ok"):
            problems.append("openclaw_cli_unavailable")
        if not checks["cron_help"].get("ok"):
            problems.append("cron_cli_unavailable")
    if args.check_cron_status and checks["cron_status"].get("secret_ref_unavailable"):
        warnings.append("gateway_secret_ref_unavailable")
    if args.check_cron_status and not checks["cron_status"].get("ok"):
        warnings.append("cron_status_not_verified")
    if args.check_tts and not checks["audio_runtime"]["google_tts"].get("ok"):
        warnings.append("google_tts_unavailable")
    if not checks["audio_runtime"]["curl"].get("ok"):
        warnings.append("curl_missing_using_urllib_fallback")
    if not checks["audio_runtime"]["ffmpeg"].get("ok"):
        warnings.append("ffmpeg_missing_using_binary_mp3_append_fallback")
    if not config.get("configured"):
        warnings.append("morning_report_not_configured")
    warnings.extend(config.get("warnings", []))

    environment_ok = not problems
    ready_to_run = environment_ok and bool(config.get("configured"))
    return {
        "success": True,
        "environment_ok": environment_ok,
        "configured": bool(config.get("configured")),
        "ready_to_run": ready_to_run,
        "problems": problems,
        "warnings": warnings,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Morning Report runtime readiness")
    parser.add_argument("--state", default=str(DEFAULT_STATE))
    parser.add_argument("--user", default=str(DEFAULT_USER))
    parser.add_argument("--audio-history", default=str(DEFAULT_AUDIO_HISTORY))
    parser.add_argument("--report-history", default=str(DEFAULT_REPORT_HISTORY))
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--check", action="store_true", help="Exit 0 only when ready to run")
    parser.add_argument("--env-check", action="store_true", help="Exit 0 only when environment checks pass")
    parser.add_argument("--check-cron-status", action="store_true", help="Probe cron status through the gateway")
    parser.add_argument("--check-tts", action="store_true", help="Probe Google TTS network access")
    parser.add_argument("--no-cli", action="store_true", help="Skip OpenClaw CLI checks")
    parser.add_argument("--no-write-check", action="store_true", help="Do not create temporary write-check files")
    parser.add_argument("--compact", action="store_true", help="Print compact JSON")
    args = parser.parse_args()

    result = build_preflight(args)
    print(json.dumps(result, ensure_ascii=False, indent=None if args.compact else 2))
    if args.check and not result["ready_to_run"]:
        return 1
    if args.env_check and not result["environment_ok"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
