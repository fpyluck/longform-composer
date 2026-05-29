#!/usr/bin/env python3
"""Smoke test for longform-composer bundled scripts."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from longform_common import create_chapter_stub, dump_simple_yaml, load_manifest, parse_manifest_lite, write_manifest

SCRIPT_DIR = Path(__file__).resolve().parent


def script_cmd(script: str, *args: object) -> list[str]:
    return [sys.executable, str(SCRIPT_DIR / script), *(str(arg) for arg in args)]


def init_cmd(root: Path, title: str, chapters: str, *extra: str) -> list[str]:
    return script_cmd("init_longform_project.py", "--title", title, "--output", root, "--chapters", chapters, *extra)


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+ " + " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def run_capture(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    print("+ " + " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, check=False, text=True, capture_output=True)


def set_all_statuses(root: Path, status: str) -> None:
    manifest = load_manifest(root / "manifest.yaml")
    for chapter in manifest["chapters"]:
        chapter["status"] = status
    write_manifest(root, manifest)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="longform-composer-test-") as tmp:
        root = Path(tmp) / "sample-project"
        run(init_cmd(root, "Sample Project", "overview|implementation|checklist", "--force"))

        first_chapter = sorted((root / "chapters").glob("*.md"))[0]
        authored_text = "# Authored\n\nThis chapter content should survive a safe --force refresh.\n"
        first_chapter.write_text(authored_text, encoding="utf-8")
        safe_force = run_capture(init_cmd(root, "Sample Project", "overview|implementation|checklist", "--force"))
        assert safe_force.returncode == 0, safe_force.stderr
        assert first_chapter.read_text(encoding="utf-8") == authored_text, "--force replaced authored chapter content"
        assert "--overwrite-chapters" in safe_force.stderr, "safe --force warning did not name the destructive override"

        destructive_force = run_capture(init_cmd(root, "Sample Project", "overview|implementation|checklist", "--force", "--overwrite-chapters"))
        assert destructive_force.returncode == 0, destructive_force.stderr
        assert authored_text not in first_chapter.read_text(encoding="utf-8"), "--overwrite-chapters did not replace authored content"

        stale_stub = root / "chapters" / "01_overview.md"
        stale_stub.write_text(create_chapter_stub("old overview"), encoding="utf-8")
        renamed_stub = run_capture(init_cmd(root, "Sample Project", "overview|implementation|checklist", "--force"))
        assert renamed_stub.returncode == 0, renamed_stub.stderr
        assert "# overview" in stale_stub.read_text(encoding="utf-8"), "--force did not refresh a stale generated stub"

        for chapter_file in sorted((root / "chapters").glob("*.md")):
            chapter_file.write_text(
                f"# {chapter_file.stem}\n\n"
                "## core content\n\n"
                "This is substantive test content for the smoke test. " * 30
                + "\n\n## chapter summary\n\nThe test chapter is complete.\n",
                encoding="utf-8",
            )

        set_all_statuses(root, "done")

        run(script_cmd("validate_longform.py", "--root", root))
        run(script_cmd("merge_markdown.py", "--root", root))
        run(script_cmd("export_longform.py", "--root", root, "--format", "docx"))
        final = root / "final" / "final_merged.md"
        docx = root / "exports" / "final_merged.docx"
        assert final.exists(), "merged file was not created"
        assert docx.exists(), "docx export was not created"
        assert "# Sample Project" in final.read_text(encoding="utf-8")

        outside_merge = Path(tmp) / "outside-final.md"
        outside = run_capture(script_cmd("merge_markdown.py", "--root", root, "--output", outside_merge))
        assert outside.returncode == 0, outside.stderr
        assert outside_merge.exists(), "outside-root merge output missing"

        placeholder_root = Path(tmp) / "placeholder-project"
        run(init_cmd(placeholder_root, "Placeholder Project", "placeholder", "--force"))
        placeholder_chapter = next((placeholder_root / "chapters").glob("*.md"))
        placeholder_chapter.write_text("# Placeholder\n\nTODO\n\n<!-- write chapter content here -->\n", encoding="utf-8")
        set_all_statuses(placeholder_root, "done")
        placeholder_report = run_capture(script_cmd("validate_longform.py", "--root", placeholder_root))
        assert placeholder_report.returncode == 0, placeholder_report.stdout + placeholder_report.stderr
        assert placeholder_report.stdout.count("contains placeholder pattern") >= 2, "validation reported only one placeholder pattern"

        try:
            import yaml  # noqa: F401

            has_yaml = True
        except ImportError:
            has_yaml = False
        if has_yaml:
            bad_root = Path(tmp) / "bad-manifest"
            bad_root.mkdir()
            (bad_root / "manifest.yaml").write_text('project:\n  title: "unterminated\nchapters:\n  - id: "01"\n', encoding="utf-8")
            bad_report = run_capture(script_cmd("validate_longform.py", "--root", bad_root))
            assert bad_report.returncode == 1, "malformed PyYAML manifest did not fail validation"
            assert "cannot parse YAML manifest with PyYAML" in bad_report.stdout, bad_report.stdout

        lite_roundtrip = parse_manifest_lite(dump_simple_yaml({"project": {"title": r"literal\ntext"}}))
        assert lite_roundtrip["project"]["title"] == r"literal\ntext", "lite parser changed literal backslash-n"

        source = Path(tmp) / "source.md"
        source.write_text("# Source\n\nIntro.\n\n```python\n# Not A Chapter\nprint('x')\n```\n\n## A\n\nAlpha.\n\n## B\n\nBeta.\n", encoding="utf-8")
        split_root = Path(tmp) / "split-project"
        run(script_cmd("split_markdown.py", source, "--title", "Split Project", "--output", split_root, "--force"))
        assert (split_root / "manifest.yaml").exists(), "split manifest missing"
        split_manifest = load_manifest(split_root / "manifest.yaml")
        split_titles = [chapter["title"] for chapter in split_manifest["chapters"]]
        assert "Not A Chapter" not in split_titles, "split treated fenced code heading as a chapter"
        run(script_cmd("validate_longform.py", "--root", split_root))
        run(script_cmd("merge_markdown.py", "--root", split_root))
        run(script_cmd("export_longform.py", "--root", split_root, "--format", "docx", "--engine", "python-docx"))
        assert (split_root / "final" / "final_merged.md").exists(), "split project did not merge"
        assert (split_root / "exports" / "final_merged.docx").exists(), "split project did not export docx"

        missing_input = run_capture(script_cmd("split_markdown.py", Path(tmp) / "missing.md"))
        assert missing_input.returncode == 2, "missing input should return a usage-style error"
        assert "Traceback" not in missing_input.stderr, "missing input produced a traceback"

    print("self-test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
