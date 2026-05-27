# Manifest Schema

Use `manifest.yaml` as the authoritative state file for every long-form project. Keep it human-readable and deterministic. The bundled scripts support the schema below.

## Required top-level fields

```yaml
schema_version: "1.0"
project:
  title: "project title"
  slug: "project-title"
  created_at: "2026-05-24T00:00:00Z"
  delivery_mode: "file-first"
  target_audience: "expert"
  target_depth: "comprehensive"
  language: "zh-CN"
  user_request: "original user request or concise paraphrase"
constraints:
  max_chapter_words: 2500
  citation_policy: "follow the active environment rules"
  style: "clear, structured, domain-appropriate"
artifacts:
  index: "index.md"
  final: "final/final_merged.md"
progress:
  current_phase: "planning"
  current_chapter_id: "01"
chapters:
  - id: "01"
    title: "overview"
    file: "chapters/01_overview.md"
    status: "planned"
    target_words: 1200
    dependencies: ""
    summary: ""
    quality_flags: ""
```

## Status values

Use only these statuses:

- `planned`: chapter exists in outline but is not yet written.
- `draft`: chapter has substantive content but has not passed review.
- `reviewed`: chapter has passed local review but final merge has not been checked.
- `done`: chapter is ready to merge.
- `needs_revision`: chapter has known gaps.
- `skipped`: intentionally omitted with a reason in `summary` or `quality_flags`.

## Status lifecycle

Default lifecycle:

```text
planned -> draft -> reviewed -> done
```

Exception lifecycle:

```text
planned -> draft -> needs_revision -> draft -> reviewed -> done
```

Do not mark a chapter `done` while it contains TODO markers, empty examples, unresolved citation placeholders, or contradictions with the manifest.

## Chapter ordering

The chapter list order in `manifest.yaml` is canonical. The merge script uses this order, not filesystem sort order, when possible. Chapter IDs should be zero-padded strings such as `01`, `02`, and `03`.

## Minimal manifest for chat route

When no filesystem is available, maintain the same fields as a visible state block in chat:

```markdown
state:
  title: "..."
  mode: "chat-only"
  completed_parts: [1]
  next_part: 2
  total_parts: 6
  continuation_anchor: "continue with part 2/6: ..."
```
