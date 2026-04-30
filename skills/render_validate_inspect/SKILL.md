---
name: render_validate_inspect
description: Validate, render, and inspect SVG technical figures. Use after creating or editing SVG diagrams to produce PNG/PDF previews and catch XML, geometry, bounds, label, and dependency problems.
---

# Render Validate Inspect Skill

Use this skill after generating or editing SVG files.

## Core principle

Never assume a generated SVG is correct. Validate, render, and inspect it before returning it to the user when tools are available.

## Workflow

1. Validate XML well-formedness.
2. Extract width, height, viewBox, element IDs, text labels, image embeds, and path count.
3. Warn about missing viewBox, missing title, missing named groups, embedded rasters, and text outside obvious bounds.
4. Render to PNG and PDF if rendering tools are available.
5. Inspect output size and basic image properties.
6. Report warnings and created preview files.

## Use bundled script

Use:

```bash
python3 scripts/render_validate_inspect.py path/to/figure.svg --outdir path/to/output
```

The script tries:

- `rsvg-convert`
- Python `cairosvg`
- `inkscape`

If none are available, it still validates and reports missing render dependencies.

## Pass/fail attitude

Treat hard XML parse errors as blocking.

Treat these as warnings:

- no `viewBox`
- no `<title>`
- too few named groups
- embedded `<image>` elements
- excessive paths relative to simple primitives
- no text labels in a labelled technical figure
- no arrow markers where arrows are expected
