# Operating Protocol

This reference expands the main workflow for high-stakes or very large deliverables. Treat Longform as a carrier for the answer: it may reorganize and checkpoint content, but it must not change the answer's meaning, claims, emphasis, uncertainty, or user-facing commitments.

## 1. Intake compression

Convert the user's request into a short internal project brief:

- topic and desired deliverable
- target audience and assumed expertise
- required depth
- language and style
- source/citation requirements
- output route: file or chat
- explicit exclusions

Do not ask for clarification when the request already contains enough information to make a strong default choice. Prefer proceeding with stated assumptions.

## 2. Outline design

For expert deliverables, use as many chapters as needed for distinct responsibilities. Each chapter should have:

- one objective
- a title that can stand alone
- target length
- dependencies, if any
- completion criteria

## 3. File creation pass

Create files in this order:

1. `manifest.yaml`
2. `index.md`
3. `chapters/*.md` stubs or complete chapters
4. `logs/progress.md`
5. `final/final_merged.md` after merge

If the environment supports shell commands, use `scripts/init_longform_project.py` for steps 1-4.

## 4. Drafting pass

Write chapters in an order that preserves coherence. Add summaries, handoffs, examples, or checklists only when they improve the final deliverable. Update manifest status after writing or review.

## 5. Review pass

Review at the levels that apply:

- local chapter quality: completeness, claims, terminology, and useful examples
- cross-chapter quality: overlap, gaps, order, and references
- final artifact quality: heading hierarchy, navigation, and consistency with user constraints

Use `scripts/validate_longform.py` before merge and after merge when script execution is available.

## 6. Light subtraction pass

Before final delivery, run a light `减法` review over the merged document or chapter set:

- remove repeated setup, duplicated explanations, and low-signal transitions
- condense repeated summaries when the final genre does not need them
- simplify section structure that does not change navigation or meaning
- preserve facts, citations, constraints, caveats, examples, emphasis, uncertainty, and any content needed to satisfy the user's requested depth

## 7. Final response

Do not paste the full final document into chat unless explicitly requested. Return:

- artifact paths
- a concise summary
- reading order
- known limitations or assumptions
- next suggested action only if it directly helps completion
