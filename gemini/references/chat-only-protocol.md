# Chat-Only Protocol

Use this only when file output is unavailable or the user explicitly requests segmented chat output.

## First response shape

```markdown
# <deliverable title>

planned structure: <n> parts
current output: part 1/<n>

## table of contents
1. ...
2. ...

---

# part 1/<n>: <title>
...

---

state:
  next_part: 2
  continuation_anchor: "continue with part 2/<n>: <next title>"
```

## Continuation rules

- Start each continuation with the part number and title.
- Continue from the stored anchor.
- Repeat only the minimal state required for coherence.
- Do not reprint earlier parts unless the user asks for consolidation.
- Stop at a section boundary.
- When all parts are complete, provide a final compact index and optional merged version only if it fits comfortably.

## Part sizing

Prefer complete subtopics over large parts that risk truncation. Keep examples near the concept they illustrate when possible.

## State block template

```markdown
state:
  title: "..."
  completed_parts: [1, 2]
  next_part: 3
  continuation_anchor: "continue with part 3/6: ..."
```
