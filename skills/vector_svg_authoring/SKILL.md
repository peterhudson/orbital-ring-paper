---
name: vector_svg_authoring
description: Create clean editable SVG technical diagrams from prose, sketches, or specifications. Use for vector graphics, SVG figures, labelled paper diagrams, schematics, technical illustrations, arrows, dimensions, callouts, and diagram cleanup.
---

# Vector SVG Authoring Skill

Use this skill when the user needs a deterministic editable vector diagram, especially for technical-paper figures.

## Core principle

Create diagrams as structured SVG code, not as raster artwork. Prefer explicit geometry, named groups, reusable definitions, and editable text.

## Output defaults

Create:

- an editable `.svg`
- a short note describing the coordinate system and named groups
- a PNG/PDF preview only if a rendering skill or rendering tool is available

## SVG authoring rules

Always:

- Use a `viewBox`.
- Use named groups with stable IDs.
- Keep text as editable `<text>` elements.
- Use simple primitives wherever possible: `line`, `polyline`, `path`, `circle`, `ellipse`, `rect`, `text`, `marker`, `clipPath`, `defs`, and `g`.
- Put reusable arrowheads, markers, gradients, and styles in `<defs>`.
- Use semantic layer IDs such as `background`, `reference_geometry`, `main_geometry`, `hidden_geometry`, `arrows`, `dimensions`, `labels`, `callouts`, and `insets`.
- Use CSS classes or inline styles consistently.
- Preserve stable IDs so later patching can target objects reliably.
- Include a small "not to scale" note when the diagram is conceptual.

Avoid:

- giant uneditable path blobs
- embedded rasters unless explicitly requested
- decorative pseudo-technical lines
- overlapping labels and arrows
- regenerating the whole file for a small revision

## Standard workflow

1. Restate the requested figure as a compact diagram spec.
2. Identify canvas size, coordinate system, semantic objects, labels, arrows, and inset needs.
3. Create SVG with named groups and meaningful IDs.
4. Validate XML well-formedness if possible.
5. Render a preview if possible.
6. Inspect for obvious geometry, label, and layering errors.
7. Return file paths and a short summary.

## Technical figure defaults

Use:

- white background
- dark neutral structural lines
- restrained semantic colour
- 2-4 px strokes for primary geometry
- 20-32 px font sizes for large 1600 px figures
- dashed lines only for hidden/reference geometry
- arrowheads only when direction matters
- double-headed dimension arrows for measured distances

## Revision workflow

When the user asks for a change:

1. Find the relevant named group or element ID.
2. Patch only that group or element.
3. Preserve unrelated geometry.
4. Re-render and inspect if possible.
5. Report exactly what changed.

## Orbital-ring caution

For orbital-ring diagrams, never draw merely decorative stripes when the concept requires helical guide lanes. A helical lane must show pitch, handedness, direction, and foreground/background ordering clearly.
