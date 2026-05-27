#!/usr/bin/env python3
"""Split an existing markdown file into longform-composer chapter files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

from longform_common import (
    build_manifest,
    count_words,
    ensure_project_structure,
    safe_filename,
    slugify,
    update_index,
    write_manifest,
    write_progress_log,
)


def split_by_headings(text: str, split_level: int) -> List[Tuple[str, str]]:
    lines = text.splitlines()
    chunks: List[Tuple[str, List[str]]] = []
    current_title = "introduction"
    current_lines: List[str] = []
    heading_re = re.compile(rf"^(#{{1,{split_level}}})\s+(.+?)\s*$")
    fence_marker: str | None = None

    for line in lines:
        fence_match = re.match(r"^\s*(```+|~~~+)", line)
        if fence_match:
            marker = fence_match.group(1)[0]
            if fence_marker == marker:
                fence_marker = None
            elif fence_marker is None:
                fence_marker = marker

        match = None if fence_marker else heading_re.match(line)
        if match and current_lines:
            chunks.append((current_title, current_lines))
            current_title = match.group(2).strip()
            current_lines = [line]
        elif match and not current_lines:
            current_title = match.group(2).strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        chunks.append((current_title, current_lines))

    return [(title, "\n".join(chunk).strip() + "\n") for title, chunk in chunks if "\n".join(chunk).strip()]


def split_large_chunks(chunks: List[Tuple[str, str]], max_words: int) -> List[Tuple[str, str]]:
    if max_words <= 0:
        return chunks

    result: List[Tuple[str, str]] = []
    for title, text in chunks:
        if count_words(text) <= max_words:
            result.append((title, text))
            continue

        paragraphs = re.split(r"\n\s*\n", text.strip())
        bucket: List[str] = []
        part = 1
        for para in paragraphs:
            candidate = "\n\n".join(bucket + [para])
            if bucket and count_words(candidate) > max_words:
                result.append((f"{title} part {part}", "\n\n".join(bucket).strip() + "\n"))
                bucket = [para]
                part += 1
            else:
                bucket.append(para)
        if bucket:
            suffix = f" part {part}" if part > 1 else ""
            result.append((f"{title}{suffix}", "\n\n".join(bucket).strip() + "\n"))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="split a markdown file into longform-composer chapter files")
    parser.add_argument("input", help="input markdown file")
    parser.add_argument("--title", help="project title; defaults to input stem")
    parser.add_argument("--output", help="project output directory; defaults to long_output/<slugified-title>")
    parser.add_argument("--split-level", type=int, default=2, choices=[1, 2, 3, 4, 5, 6], help="split at headings up to this level")
    parser.add_argument("--max-words", type=int, default=2500, help="further split chunks above this mixed-language word estimate")
    parser.add_argument("--force", action="store_true", help="allow writing into a non-empty output directory")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"error: input markdown file does not exist: {input_path}", file=sys.stderr)
        return 2
    if not input_path.is_file():
        print(f"error: input path is not a file: {input_path}", file=sys.stderr)
        return 2
    text = input_path.read_text(encoding="utf-8")
    title = args.title or input_path.stem.replace("_", " ").replace("-", " ").strip().title()
    output = Path(args.output) if args.output else Path("long_output") / slugify(title)

    if output.exists() and any(output.iterdir()) and not args.force:
        raise SystemExit(f"error: output directory exists and is not empty: {output}; use --force")

    chunks = split_by_headings(text, args.split_level)
    chunks = split_large_chunks(chunks, args.max_words)
    chapter_titles = [title for title, _ in chunks]

    ensure_project_structure(output)
    manifest = build_manifest(
        title=title,
        output_root=output,
        chapters=chapter_titles,
        delivery_mode="file-first",
        target_audience="auto",
        target_depth="source-preserving split",
        language="auto",
        style="preserve source markdown content where possible",
        user_request=f"split existing markdown file: {input_path}",
        target_words=args.max_words,
        chapter_status="draft",
    )

    for idx, (chapter_title, chapter_text) in enumerate(chunks):
        chapter = manifest["chapters"][idx]
        chapter_id = chapter["id"]
        filename = f"{chapter_id}_{safe_filename(chapter_title, f'chapter-{chapter_id}')}.md"
        chapter["file"] = f"chapters/{filename}"
        path = output / chapter["file"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(chapter_text, encoding="utf-8")

    write_manifest(output, manifest)
    update_index(output, manifest)
    write_progress_log(output, f"split {input_path} into {len(chunks)} chapter files")
    print("Longform split complete")
    print(f"  source: {input_path}")
    print(f"  output: {output}")
    print(f"  chapters: {len(chunks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
