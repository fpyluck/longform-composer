# Examples

## Example 1: technical white paper

User request:

```text
Use longform-composer to write a complete technical white paper on an early gastric cancer endoscopic ai quality-control system. Split it into md files and merge a final markdown.
```

Recommended behavior:

1. Create `long_output/early-gastric-cancer-ai-qc/`.
2. Create a manifest with chapters such as clinical problem, product scope, data pipeline, model design, validation, deployment, regulatory notes, and checklist.
3. Write each chapter under `chapters/`.
4. Validate and merge.
5. Return paths and a concise reading guide.

## Example 2: existing long markdown split

User request:

```text
This markdown is too long. Split it into chapter files and create a manifest.
```

Recommended command:

```bash
python scripts/split_markdown.py input.md --title "project title" --output long_output/project-title --split-level 2
```

Then validate:

```bash
python scripts/validate_longform.py --root long_output/project-title
```

## Example 3: chat-only continuation

User request:

```text
Do not create files. Explain this topic in segmented md in chat.
```

Recommended behavior:

- Announce the planned number of parts.
- Output part 1 in the first response unless the user asks for a larger batch.
- End with a continuation anchor.
- Resume from the anchor in later turns.

## Example 4: codebase documentation

User request:

```text
Analyze this repo and produce full developer documentation. Codex keeps writing too little.
```

Recommended behavior:

- Use the file route and put outputs under `docs/longform/<project-slug>/` if the repository has a `docs/` folder.
- Create manifest and chapter files.
- Run available tests or linters only when the documentation task requires verifying commands.
- Summarize paths rather than pasting the entire documentation in chat.
