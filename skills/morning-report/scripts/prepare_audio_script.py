#!/usr/bin/env python3
"""Prepare a clean spoken audio script from a delivered Morning Report."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

FENCE_RE = re.compile(r"^\s*```")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s*")
LIST_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((?:https?://|mailto:)[^)]+\)")
URL_RE = re.compile(r"https?://\S+")
INLINE_MARKUP_RE = re.compile(r"[*_`]+")
SENTENCE_RE = re.compile(r"(?<=[.!?。！？])\s+")
WORD_RE = re.compile(r"\b[\w']+\b", re.UNICODE)


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def clean_line(line: str) -> str:
    line = line.strip()
    if not line:
        return ""
    if line.startswith("MEDIA:"):
        return ""
    if TABLE_SEPARATOR_RE.match(line):
        return ""
    if line.startswith("|") and line.endswith("|"):
        return ""

    line = HEADING_RE.sub("", line).strip()
    line = LIST_RE.sub("", line).strip()
    line = MARKDOWN_LINK_RE.sub(r"\1", line)
    line = URL_RE.sub("", line)
    line = INLINE_MARKUP_RE.sub("", line)
    line = re.sub(r"\s+", " ", line).strip()
    line = line.strip(" -|")
    return line


def markdown_to_spoken_text(markdown: str) -> str:
    lines: list[str] = []
    in_fence = False
    for raw_line in markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        if FENCE_RE.match(raw_line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = clean_line(raw_line)
        if line:
            lines.append(line)

    text = " ".join(lines)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def trim_to_max_words(text: str, max_words: int) -> tuple[str, bool]:
    if max_words <= 0 or count_words(text) <= max_words:
        return text, False

    sentences = [part.strip() for part in SENTENCE_RE.split(text) if part.strip()]
    kept: list[str] = []
    for sentence in sentences:
        candidate = " ".join([*kept, sentence]).strip()
        if count_words(candidate) > max_words:
            break
        kept.append(sentence)

    if kept:
        return " ".join(kept).strip(), True

    words = text.split()
    return " ".join(words[:max_words]).strip(), True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a Morning Report audio script")
    parser.add_argument("--report-file", required=True, help="Delivered Morning Report Markdown file")
    parser.add_argument("--output", required=True, help="Output text file for TTS")
    parser.add_argument("--max-words", type=int, default=750, help="Soft maximum word count for the audio script")
    parser.add_argument("--dry-run", action="store_true", help="Print metadata without writing output")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        report_path = Path(args.report_file)
        output_path = Path(args.output)
        report = report_path.read_text(encoding="utf-8")
        script, truncated = trim_to_max_words(markdown_to_spoken_text(report), args.max_words)
        if not script:
            raise ValueError("audio script is empty after cleaning report")

        metadata: dict[str, Any] = {
            "success": True,
            "report_file": str(report_path),
            "output": str(output_path),
            "word_count": count_words(script),
            "char_count": len(script),
            "max_words": args.max_words,
            "truncated": truncated,
        }

        if not args.dry_run:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(script + "\n", encoding="utf-8")

        print(json.dumps(metadata, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(f"prepare_audio_script.py failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
