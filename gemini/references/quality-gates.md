# Quality Gates

Use these checks before telling the user the long-form deliverable is complete.

## Planning gate

- The project has a clear title and slug.
- The manifest records the user's goal and constraints.
- The outline has no duplicate chapter responsibilities.
- Each chapter has a target audience and depth implied by the project fields.
- The chosen output route matches the environment and user request.

## Draft gate

- Every chapter file exists.
- Each chapter has a clear top-level title.
- Each chapter has substantive content, not only headings.
- Examples, code, tables, or checklists are included when they materially improve the deliverable.
- There are no unresolved placeholders such as `TODO`, `TBD`, `[citation needed]`, or empty sections.

## Source and citation gate

- Current, legal, medical, financial, scientific, product, or policy claims follow the active environment's browsing and citation requirements.
- Citations are attached near the claims they support.
- The final document distinguishes facts, assumptions, and recommendations.
- Source notes are kept in `sources/` or a references section when the project requires traceability.

## Merge gate

- Merged chapter order matches `manifest.yaml`.
- The final file has one primary H1 title.
- Chapter headings are demoted or normalized so the final hierarchy is readable.
- The table of contents points to the actual chapter sequence.
- Repeated summaries are either retained intentionally or condensed for the final genre.
- A light `减法` pass removes redundant prose or structure without changing answer semantics, emphasis, uncertainty, required coverage, evidence, caveats, or useful examples.

## Delivery gate

- The agent response does not dump the complete long document by default.
- The response includes the final artifact path.
- Known limitations are stated plainly.
- The user can resume from the manifest if the session is interrupted.
