---
name: vector-diagrams
description: Create and revise deterministic technical vector diagrams as editable SVG, with optional PNG/PDF export and geometry self-checks. Use when asked to create, revise, clean up, or export a technical diagram, paper figure, schematic, vector graphic, geometry illustration, coordinate diagram, orbital-ring figure, or SVG.
---

# Vector Diagrams

Prefer deterministic vector graphics over raster image generation.

Do not invent visually plausible but geometrically wrong details. Treat diagrams as compiled geometry, not artwork.

## Workflow

1. Convert the user's request into a short diagram specification before drawing.
2. Identify the coordinate system, scale, labels, arrows, layers, and intended viewpoint.
3. Generate editable SVG using simple primitives: `line`, `polyline`, `path`, `circle`, `ellipse`, `rect`, `text`, `marker`, `clipPath`, `defs`, `g`, and transforms.
4. Use named SVG groups such as `earth`, `ring`, `guide_shell`, `helical_lanes`, `labels`, `arrows`, `dimensions`, `callouts`, and `inset`.
5. Save the SVG to a sensible filename under `figures/`.
6. If rendering tools are available, render a PNG preview and inspect it for obvious mistakes.
7. For revision requests, patch the existing SVG instead of regenerating the whole figure unless the user asks for a redesign.

## Output contract

When creating a figure, provide:

- editable SVG
- PNG preview if rendering is available
- PDF export if rendering is available
- a short note describing what was created and where the files are saved

If export tools are missing, still create the SVG and explain which export tool is missing.

## Style defaults

Use a clean technical-paper style:

- white background
- sans-serif text
- black or dark gray structural lines
- restrained colour only when it distinguishes semantic elements
- consistent stroke widths
- dimension arrows with arrowheads
- dashed lines only for hidden or reference geometry
- labels outside dense geometry where possible

## SVG quality rules

- Keep text editable.
- Keep groups named.
- Do not flatten everything into one giant path.
- Do not use embedded raster images unless explicitly requested.
- Use `viewBox`.
- Avoid text overlapping arrows or object outlines.
- Use hidden-line or clipping conventions for foreground/background ambiguity.
- Use explicit markers for arrowheads.
- Include a small "not to scale" note if the diagram is conceptual.

## Self-check before returning

Review the figure against the user's intent:

- Are arrows pointing to the correct target?
- Are labels attached to the correct objects?
- Is foreground/background ordering clear?
- Are helices actually helical rather than decorative stripes?
- Are handedness and directionality visually unambiguous?
- Are dimension arrows measuring the intended gap, thickness, or radius?
- Is the figure technically clarifying rather than merely attractive?

## Orbital-ring-specific primitives

For orbital-ring diagrams, be especially careful with:

- Earth surface versus altitude gap
- guide-shell cross-section
- orbital ring centreline
- helical left-handed and right-handed lanes
- paired counter-propagating slug streams
- four-lane balanced cells
- stator-8 cross-sections
- exploded insets
- local coordinate frames
- hidden rear-side geometry
- foreground ring section clarity

When the user supplies a sketch, treat it as layout intent, not a literal raster to trace.
