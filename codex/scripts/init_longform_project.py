#!/usr/bin/env python3
"""Initialize a longform-composer markdown project."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from longform_common import (
    build_manifest,
    create_chapter_stub,
    default_chapter_titles,
    ensure_project_structure,
    slugify,
    update_index,
    write_manifest,
    write_progress_log,
)


def parse_chapters(raw: str | None) -> list[str]:
    if not raw:
        return default_chapter_titles()
    delimiter = "|" if "|" in raw else ","
    chapters = [part.strip() for part in raw.split(delimiter) if part.strip()]
    return chapters or default_chapter_titles()


def build_output_path(title: str, output: str | None) -> Path:
    if output:
        return Path(output)
    return Path("long_output") / slugify(title)


def equivalent_text(left: str, right: str) -> bool:
    left_normalized = left.replace("\r\n", "\n").replace("\r", "\n").rstrip()
    right_normalized = right.replace("\r\n", "\n").replace("\r", "\n").rstrip()
    return left_normalized == right_normalized


def is_chapter_stub(text: str, expected_stub: str) -> bool:
    if not text.strip():
        return True
    if equivalent_text(text, expected_stub):
        return True
    match = re.match(r"^#\s+(.+?)\s*$", text.replace("\r\n", "\n").replace("\r", "\n"), flags=re.MULTILINE)
    if not match:
        return False
    return equivalent_text(text, create_chapter_stub(match.group(1).strip()))


def main() -> int:
    parser = argparse.ArgumentParser(description="initialize a long-form markdown project")
    parser.add_argument("--title", required=True, help="project title")
    parser.add_argument("--output", help="project output directory; defaults to long_output/<slugified-title>")
    parser.add_argument("--chapters", help="chapter titles separated by | or ,")
    parser.add_argument("--mode", default="file-first", choices=["file-first", "repo-integrated", "hybrid", "chat-only"])
    parser.add_argument("--audience", default="expert", help="target audience label")
    parser.add_argument("--depth", default="comprehensive", help="target depth label")
    parser.add_argument("--language", default="auto", help="language label, for example zh-CN or en")
    parser.add_argument(
        "--style",
        default="clear, structured, export-friendly, domain-appropriate; use tables, checklists, and callouts only when they improve comprehension over prose",
        help="style constraints",
    )
    parser.add_argument("--user-request", default="", help="original request or concise paraphrase")
    parser.add_argument("--target-words", type=int, default=1500, help="target words or mixed-language units per chapter")
    parser.add_argument("--force", action="store_true", help="refresh generated manifest, index, and empty/stub chapter files")
    parser.add_argument("--overwrite-chapters", action="store_true", help="also replace authored chapter files; destructive")
    args = parser.parse_args()

    root = build_output_path(args.title, args.output)
    if root.exists() and any(root.iterdir()) and not args.force:
        print(f"error: output directory already exists and is not empty: {root}", file=sys.stderr)
        print("use --force to overwrite generated files", file=sys.stderr)
        return 2

    chapters = parse_chapters(args.chapters)
    ensure_project_structure(root)
    manifest = build_manifest(
        title=args.title,
        output_root=root,
        chapters=chapters,
        delivery_mode=args.mode,
        target_audience=args.audience,
        target_depth=args.depth,
        language=args.language,
        style=args.style,
        user_request=args.user_request,
        target_words=args.target_words,
        chapter_status="planned",
    )
    write_manifest(root, manifest)
    update_index(root, manifest)

    skipped_authored: list[Path] = []
    written_chapters = 0
    preserved_chapters = 0
    for chapter in manifest["chapters"]:
        path = root / chapter["file"]
        stub = create_chapter_stub(str(chapter["title"]))
        if path.exists():
            if not args.force:
                preserved_chapters += 1
                continue
            current = path.read_text(encoding="utf-8")
            if not args.overwrite_chapters and not is_chapter_stub(current, stub):
                skipped_authored.append(path)
                preserved_chapters += 1
                continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(stub, encoding="utf-8")
        written_chapters += 1

    write_progress_log(root, "initialized long-form project")
    print("Longform project initialized")
    print(f"  root: {root}")
    print(f"  manifest: {root / 'manifest.yaml'}")
    print(f"  index: {root / 'index.md'}")
    print(f"  chapters: {len(manifest['chapters'])} total, {written_chapters} written, {preserved_chapters} preserved")
    if skipped_authored:
        print("  preserved authored chapters:", file=sys.stderr)
        for path in skipped_authored:
            print(f"  - {path}", file=sys.stderr)
        print("  use --overwrite-chapters with --force to replace authored chapter files", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
