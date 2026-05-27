---
name: longform-composer
description: orchestrate comprehensive long-form markdown deliverables that are too large or structured for a single chat response. use when the user asks for a complete, systematic, tutorial, report, manual, white paper, review, specification, book-like answer, segmented md files, chapters, continuation anchors, manifest, checkpointing, or final merged markdown; when the user says outputs are too short; or when the task likely needs multiple sections, files, examples, or passes. prefer durable files with manifest, index, chapter files, validation, and merge; use chat-only numbered parts only when a filesystem is unavailable or explicitly requested.
---

# Longform Composer

## Core Principle

Do not try to force a large deliverable into one chat message. Convert long-form work into durable markdown artifacts, explicit checkpoints, deterministic validation, and a final merged deliverable. This skill is a packaging and workflow layer: it must preserve the model's intended meaning, claims, emphasis, uncertainty, and user-facing answer semantics while changing only organization, storage, and delivery. It does not change model token limits, context limits, rate limits, or product quotas.

## Output Route

- **File route**: Default when a filesystem, repository, or workspace is available. Create files, update progress state, validate, merge, and summarize paths in chat. If the current repo has an obvious docs location, place outputs there; otherwise use `long_output/<project-slug>/`.
- **Chat route**: Use only when the user explicitly requests chat-only output or no durable file output is available. Split into numbered parts and keep continuation state.
- **Chat preview**: With file output, chat may include a concise preview or reading guide, but the full deliverable remains in files unless the user asks otherwise.

## File-First Workflow

1. Clarify silently from the user request when possible: topic, audience, depth, final format, source/citation requirements, and any constraints already stated.
2. Create a project folder using this layout unless the repository has a better convention:

   ```text
   long_output/<project-slug>/
     manifest.yaml
     index.md
     chapters/
     final/
     logs/
     notes/
     sources/
   ```

3. Create or update `manifest.yaml` before writing long content. Record the project title, delivery mode, audience, depth, style constraints, artifacts, and chapter plan.
4. Create `index.md` as the user-facing table of contents and reading guide.
5. Write each chapter as a separate markdown file under `chapters/`. Keep chapters independently coherent and avoid hidden dependency on chat history.
6. Update chapter status as work becomes verifiable: `planned` -> `draft` -> `reviewed` -> `done`, or `needs_revision` when issues remain.
7. Run a consistency pass: check missing chapters, repeated sections, broken heading hierarchy, incomplete placeholders, source/citation gaps, and mismatch between `index.md`, `manifest.yaml`, and actual files.
8. Before final merge, do a light `减法` pass: remove duplicated explanations, low-signal transitions, repeated summaries, and unnecessary scaffolding. Preserve facts, evidence, user constraints, needed caveats, emphasis, and uncertainty.
9. Merge chapters into `final/final_merged.md` after validation. Use `scripts/merge_markdown.py` when available.
10. In chat, return only a concise delivery note: what was created, important paths, reading order, known limitations, and next useful action.

## Artifact Contract

A project is complete only when these files exist:

- `manifest.yaml`: authoritative state and chapter order.
- `index.md`: readable outline and navigation guide.
- `chapters/*.md`: one focused chapter per file.
- `final/final_merged.md`: merged full deliverable, unless the user explicitly asked for segmented files only.
- `logs/progress.md`: short change log for resumed or multi-pass work.

Use `references/manifest-schema.md` for the full manifest schema and status lifecycle.

## Chapter Contract

Use this as a default chapter shape, adapting or omitting sections when the deliverable's genre calls for a different structure:

```markdown
# <chapter title>

> chapter objective: <one sentence describing what this chapter must accomplish>

## core content
...

## examples or implementation details
...

## chapter summary
...

## handoff to next chapter
...
```

Adapt section names to the user's language and domain. Preserve a stable heading hierarchy. Do not duplicate large blocks across chapters; use short cross-references instead.

## Scripted Operations

Use bundled scripts for deterministic file operations whenever possible:

- `scripts/init_longform_project.py`: initialize a long-form markdown project with manifest, index, folders, and chapter stubs.
- `scripts/validate_longform.py`: validate manifest consistency, chapter files, statuses, placeholders, and merge readiness.
- `scripts/merge_markdown.py`: merge chapter files in manifest order into `final/final_merged.md` with a table of contents.
- `scripts/split_markdown.py`: split an existing long markdown file into chapter files and generate a manifest.
- `scripts/self_test.py`: run a quick local smoke test for the bundled scripts.

Typical file-first command sequence:

```bash
python scripts/init_longform_project.py --title "project title" --chapters "overview|background|implementation|examples|risks|checklist"
python scripts/validate_longform.py --root long_output/project-title
python scripts/merge_markdown.py --root long_output/project-title
```

## Chat-Only Protocol

When durable files are unavailable, follow `references/chat-only-protocol.md`:

1. First output a compact table of contents and total planned parts.
2. Then output one numbered part at a time by default, such as `part 1/6`, unless the user asks for a larger batch.
3. End each part at a clean heading boundary.
4. Include a continuation anchor, for example: `continue with part 2/6: <next heading>`.
5. Maintain a short state block listing completed and remaining sections.
6. Never claim that this bypasses platform limits.

## Quality Gates

Before delivery, verify:

- Every planned chapter has a file and status.
- Done chapters contain substantive content, not placeholders.
- The final file follows manifest order.
- Headings are coherent after merge.
- User constraints are reflected in the manifest and output where they affect the deliverable.
- Claims that require current or external evidence follow the surrounding environment's browsing and citation rules.
- The final light `减法` review has not changed the intended answer semantics.
- The chat response does not paste the entire long document when files are the intended deliverable.

See `references/quality-gates.md` for detailed review checks and failure handling.
