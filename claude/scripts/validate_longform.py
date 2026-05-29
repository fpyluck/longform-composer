#!/usr/bin/env python3
"""Validate a longform-composer project."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

from longform_common import ALLOWED_STATUSES, chapter_path, count_words, get_chapters, load_project, normalize_status

PLACEHOLDER_PATTERNS = [
    r"TODO",
    r"TBD",
    r"\[citation needed\]",
    r"<!--\s*write chapter content here\s*-->",
    r"<!--\s*add examples",
    r"<!--\s*summarize",
    r"<!--\s*explain how",
    r"<(state|write|include|summarize|explain)\b[^>]*>",
]


def add(report: Dict[str, List[str]], level: str, message: str) -> None:
    report.setdefault(level, []).append(message)


def validate(root: Path, strict: bool = False) -> Dict[str, Any]:
    report: Dict[str, Any] = {"root": str(root), "errors": [], "warnings": [], "info": []}

    manifest_path = root / "manifest.yaml"
    if not manifest_path.exists():
        add(report, "errors", f"missing manifest: {manifest_path}")
        return report

    try:
        manifest = load_project(root)
    except Exception as exc:
        add(report, "errors", f"cannot parse manifest: {exc}")
        return report

    index_path = root / "index.md"
    if not index_path.exists():
        add(report, "warnings", "missing index.md")

    chapters = get_chapters(manifest)
    if not chapters:
        add(report, "errors", "manifest has no chapters")
        return report

    seen_ids: set[str] = set()
    seen_files: set[str] = set()
    numeric_ids: list[int] = []

    for idx, chapter in enumerate(chapters, start=1):
        cid = str(chapter.get("id", "")).strip()
        title = str(chapter.get("title", "")).strip()
        rel_file = str(chapter.get("file", "")).strip()
        status = normalize_status(chapter.get("status"))

        label = cid or f"chapter-{idx}"
        if not cid:
            add(report, "errors", f"chapter {idx} missing id")
        elif cid in seen_ids:
            add(report, "errors", f"duplicate chapter id: {cid}")
        else:
            seen_ids.add(cid)
            if cid.isdigit():
                numeric_ids.append(int(cid))

        if not title:
            add(report, "errors", f"chapter {label} missing title")

        if not rel_file:
            add(report, "errors", f"chapter {label} missing file")
            continue
        if rel_file in seen_files:
            add(report, "errors", f"duplicate chapter file: {rel_file}")
        seen_files.add(rel_file)

        if status not in ALLOWED_STATUSES:
            add(report, "errors", f"chapter {label} has invalid status: {status}")

        path = chapter_path(root, chapter)
        if not path.exists():
            add(report, "errors", f"chapter {label} file does not exist: {rel_file}")
            continue

        text = path.read_text(encoding="utf-8")
        words = count_words(text)
        add(report, "info", f"chapter {label}: {words} word units, status={status}, file={rel_file}")

        if not text.strip():
            add(report, "errors", f"chapter {label} is empty")
        if status == "done" and words < 250:
            add(report, "warnings", f"chapter {label} is marked done but is short ({words} word units)")
        if status in {"reviewed", "done"}:
            matches = []
            for pattern in PLACEHOLDER_PATTERNS:
                if re.search(pattern, text, flags=re.IGNORECASE):
                    matches.append(pattern)
            for pattern in matches:
                add(report, "errors" if strict else "warnings", f"chapter {label} contains placeholder pattern: {pattern}")
        if not re.search(r"^#\s+", text, flags=re.MULTILINE):
            add(report, "warnings", f"chapter {label} has no top-level heading")
        if rel_file.startswith("chapters/") and cid and not Path(rel_file).name.startswith(cid):
            add(report, "warnings", f"chapter {label} filename should start with its id")

    if numeric_ids and numeric_ids != sorted(numeric_ids):
        add(report, "warnings", "chapter ids are not in ascending order")

    final_path = root / "final" / "final_merged.md"
    if final_path.exists():
        final_text = final_path.read_text(encoding="utf-8")
        add(report, "info", f"final_merged.md exists with {count_words(final_text)} word units")
    else:
        add(report, "warnings", "final/final_merged.md does not exist yet")

    if strict and report["warnings"]:
        add(report, "errors", "strict mode treats warnings as blocking")

    return report


def print_report(report: Dict[str, Any]) -> None:
    print("Longform validation report")
    print(f"  root: {report['root']}")
    for level in ["errors", "warnings", "info"]:
        items = report.get(level, [])
        if not items:
            continue
        print(f"\n{level.upper()} ({len(items)})")
        for item in items:
            print(f"  - {item}")


def main() -> int:
    parser = argparse.ArgumentParser(description="validate a longform-composer project")
    parser.add_argument("--root", required=True, help="project root containing manifest.yaml")
    parser.add_argument("--strict", action="store_true", help="treat warnings as blocking where applicable")
    parser.add_argument("--json", action="store_true", help="print machine-readable json")
    args = parser.parse_args()

    report = validate(Path(args.root), strict=args.strict)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(report)

    return 1 if report.get("errors") else 0


if __name__ == "__main__":
    raise SystemExit(main())
