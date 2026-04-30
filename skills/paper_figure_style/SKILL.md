---
name: paper_figure_style
description: Apply a consistent technical-paper visual style to SVG figures, including typography, stroke widths, semantic colour, labels, arrows, dimensions, hidden lines, insets, and publication-oriented export conventions.
---

# Paper Figure Style Skill

Use this skill when creating or revising figures intended for a paper, memo, preprint, or technical presentation.

## Core principle

A paper figure should be calm, legible, editable, and semantically consistent. Do not optimize for flashy visual impact.

## Style defaults

Use the shared style tokens in:

```text
references/style_tokens.json
```

Default canvas:

- 1600 × 1000 px for landscape figures
- 1200 × 900 px for compact figures
- white background
- generous margins

Typography:

- Helvetica/Arial/sans-serif
- 28 px primary labels
- 21 px small labels
- 18 px notes
- keep labels editable

Lines:

- 3 px primary structure
- 2 px secondary/reference lines
- 2 px dashed hidden lines
- 2 px dimension lines
- 2.5 px arrows
- round caps and joins

Colour:

- use dark gray/black for structure
- use restrained semantic colour only when it distinguishes concepts
- ensure grayscale legibility
- do not use colour as the only indicator of meaning

Layer order:

1. background
2. reference geometry
3. hidden/rear geometry
4. main geometry
5. dimensions
6. arrows/callouts
7. labels
8. notes

## Figure conventions

Use:

- dashed rear/hidden geometry
- solid foreground geometry
- double-headed arrows for dimensions
- single-headed arrows for flow/direction/callouts
- side insets for dense local detail
- "not to scale" note when conceptual
- consistent caption terminology

Avoid:

- decorative shadows
- gradients unless they encode depth or object identity
- overly saturated colours
- text over dense geometry
- unlabeled colours
- inconsistent arrowhead styles

## Use bundled script

Use:

```bash
python3 scripts/apply_paper_style.py input.svg output.svg
```

The script injects or replaces a basic style block and arrow marker. It is intentionally conservative and should not flatten or rewrite geometry.
