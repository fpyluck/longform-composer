#!/usr/bin/env python3
"""Merge chapter markdown files for a longform-composer project."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List

from longform_common import (
    chapter_anchor,
    chapter_path,
    count_words,
    demote_headings,
    get_chapters,
    get_title,
    load_project,
    normalize_status,
    table_cell,
    write_progress_log,
)

DEFAULT_INCLUDE_STATUSES = {"draft", "reviewed", "done", "needs_revision"}


def display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return os.path.relpath(path, root)


def build_toc(chapters: List[Dict[str, object]]) -> str:
    lines = ["## Contents", ""]
    for chapter in chapters:
        cid = str(chapter.get("id", ""))
        title = str(chapter.get("title", "untitled"))
        summary = str(chapter.get("summary") or "").strip()
        suffix = f" - {summary}" if summary else ""
        lines.append(f"- [{cid}. {title}](#{chapter_anchor(title)}){suffix}")
    return "\n".join(lines).strip() + "\n"


def build_document_profile(manifest: Dict[str, object], included: List[Dict[str, object]]) -> str:
    project = manifest.get("project") if isinstance(manifest.get("project"), dict) else {}
    constraints = manifest.get("constraints") if isinstance(manifest.get("constraints"), dict) else {}
    lines = [
        "## Document profile",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Audience | {table_cell(project.get('target_audience'))} |",
        f"| Depth | {table_cell(project.get('target_depth'))} |",
        f"| Language | {table_cell(project.get('language'))} |",
        f"| Style | {table_cell(constraints.get('style'))} |",
        f"| Request | {table_cell(project.get('user_request'))} |",
        f"| Source chapters | {len(included)} |",
    ]
    return "\n".join(lines).strip() + "\n"


def merge(root: Path, output: Path | None = None, include_planned: bool = False, no_toc: bool = False) -> Path:
    manifest = load_project(root)
    title = get_title(manifest)
    chapters = get_chapters(manifest)
    included: List[Dict[str, object]] = []
    chapter_blocks: List[str] = []
    warnings: List[str] = []

    for chapter in chapters:
        status = normalize_status(chapter.get("status"))
        if status == "skipped":
            continue
        if status == "planned" and not include_planned:
            warnings.append(f"skipping planned chapter {chapter.get('id')}: {chapter.get('title')}")
            continue
        if status not in DEFAULT_INCLUDE_STATUSES and not include_planned:
            warnings.append(f"skipping chapter {chapter.get('id')} with status {status}")
            continue

        path = chapter_path(root, chapter)
        if not path.exists():
            warnings.append(f"missing chapter file: {chapter.get('file')}")
            continue
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            warnings.append(f"empty chapter file: {chapter.get('file')}")
            continue

        included.append(chapter)
        normalized = demote_headings(text, levels=1)
        chapter_blocks.append(normalized.strip())

    if output is None:
        output = root / "final" / "final_merged.md"
    else:
        output = output if output.is_absolute() else root / output
    output.parent.mkdir(parents=True, exist_ok=True)

    parts: List[str] = [
        f"# {title}",
        "",
        "> Complete merged Markdown generated from the chapter set. Treat this file as the semantic source for optional document exports.",
        "",
        build_document_profile(manifest, included),
        "",
    ]
    if not no_toc:
        parts.append(build_toc(included))
        parts.append("")
    for block in chapter_blocks:
        parts.append("---")
        parts.append("")
        parts.append(block)
        parts.append("")

    if warnings:
        parts.append("---")
        parts.append("")
        parts.append("## Merge notes")
        parts.append("")
        for warning in warnings:
            parts.append(f"- {warning}")
        parts.append("")

    output.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    output_label = display_path(output, root)
    write_progress_log(root, f"merged {len(included)} chapters into {output_label}")
    print("Longform merge complete")
    print(f"  root: {root}")
    print(f"  output: {output}")
    print(f"  chapters merged: {len(included)}")
    print(f"  word units: {count_words(output.read_text(encoding='utf-8'))}")
    if warnings:
        print("Merge warnings:", file=sys.stderr)
        for warning in warnings:
            print(f"  - {warning}", file=sys.stderr)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="merge markdown chapters in manifest order")
    parser.add_argument("--root", required=True, help="project root containing manifest.yaml")
    parser.add_argument("--output", help="output path, relative to root unless absolute")
    parser.add_argument("--include-planned", action="store_true", help="include planned chapters if files exist")
    parser.add_argument("--no-toc", action="store_true", help="do not generate a table of contents")
    args = parser.parse_args()

    merge(Path(args.root), Path(args.output) if args.output else None, include_planned=args.include_planned, no_toc=args.no_toc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
