# Longform Composer — 三端长文写作技能

> Claude Code × Codex × Gemini 三端 — 分段规划、manifest 驱动、章节写作、最终合并。

| 端 | 路径 |
|---|---|
| Claude Code | `claude/` |
| Codex | `codex/` |
| Gemini | `gemini/` |

---

## What's New — 2026-05-27

首次在 GitHub 发布三端完整版本。Claude、Codex、Gemini 三端 SKILL.md 及配套资源同步上线。

---


Longform Composer is a Claude Code skill for producing comprehensive markdown deliverables without relying on one oversized chat response. It plans the work, creates a manifest, writes chapter files, validates progress, and merges the final markdown.

## Best use cases

- complete technical reports, white papers, tutorials, manuals, and reviews
- segmented markdown output with final merge
- Claude Code tasks where responses become too short or truncated
- repo documentation that should be written into files instead of chat
- chat-only continuation when file output is unavailable

## Included resources

- `SKILL.md`: main skill instructions and trigger description
- `references/`: detailed protocols, schema, quality gates, and examples
- `assets/templates/`: reusable manifest, index, and chapter templates
- `scripts/init_longform_project.py`: create a project scaffold
- `scripts/validate_longform.py`: validate project state and chapter files
- `scripts/merge_markdown.py`: merge chapters into `final/final_merged.md`
- `scripts/split_markdown.py`: split an existing markdown file into chapter files
- `scripts/self_test.py`: smoke test for bundled scripts

`init_longform_project.py --force` refreshes generated files but preserves authored chapter content. Use `--overwrite-chapters` only when you intentionally want to replace existing chapter files.

## Quick script test

```bash
python scripts/self_test.py
```
