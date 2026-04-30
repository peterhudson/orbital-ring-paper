---
name: technical_figure_redteam
description: Critique technical diagrams for correctness, ambiguity, misleading geometry, bad labels, occlusion errors, scale confusion, and paper-readiness. Use before finalizing engineering or scientific figures.
---

# Technical Figure Red-Team Skill

Use this skill to review a diagram before the user relies on it in a paper, memo, or presentation.

## Core principle

A technical figure is successful if it prevents misunderstanding. Attractive but misleading diagrams must be rejected.

## Red-team workflow

1. Read the user's intended claim or caption.
2. Inspect the SVG structure and rendered preview if available.
3. Compare the visual encoding against the physical/conceptual model.
4. Identify reader-confusion risks.
5. Separate blocking issues from polish issues.
6. Suggest concrete patch actions using IDs or groups where possible.

## Review categories

Check:

- Conceptual correctness
- Geometry/projection correctness
- Scale and exaggeration
- Foreground/background ordering
- Hidden-line convention
- Label placement
- Arrow target correctness
- Directionality and handedness
- Semantic colour consistency
- Visual clutter
- Caption/figure mismatch
- Accessibility and grayscale legibility
- Editability and named layers

## Severity scale

Use:

- `BLOCKER`: likely to make a reader understand the concept incorrectly
- `MAJOR`: ambiguity or visual issue that materially reduces comprehension
- `MINOR`: polish, consistency, or publication-cleanup issue
- `NICE_TO_HAVE`: optional improvement

## Output format

Return:

```markdown
## Technical figure red-team

### Verdict
[ready / revise / major redesign]

### Blocking issues
- ...

### Major issues
- ...

### Minor issues
- ...

### Patch plan
1. ...
2. ...
3. ...
```

## Use bundled script

Use `scripts/figure_redteam_template.py` to generate a structured checklist from an SVG:

```bash
python3 scripts/figure_redteam_template.py figure.svg --intent "..."
```

The script does not replace judgement; it creates a consistent audit scaffold.
