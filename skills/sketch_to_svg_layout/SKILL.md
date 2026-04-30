---
name: sketch_to_svg_layout
description: Convert user-supplied sketches into clean SVG layout plans and editable vector figure scaffolds. Use for pen-and-paper diagram sketches, rough layouts, annotated screenshots, and turning sketch intent into technical figures.
---

# Sketch to SVG Layout Skill

Use this skill when the user supplies a sketch or rough visual layout and wants a clean technical vector diagram.

## Core principle

Treat sketches as layout intent, not geometry truth. Reconstruct the figure as clean vector geometry.

## Sketch interpretation workflow

1. Identify the major objects, labels, arrows, insets, and spatial relationships.
2. Separate layout intent from messy hand-drawn artifacts.
3. Create a structured diagram spec.
4. Create an SVG with:
   - the sketch as a low-opacity locked underlay, if useful
   - named vector layers for reconstructed geometry
   - labels and callouts as editable text
5. Rebuild geometry using vector primitives rather than tracing every pen wobble.
6. Render and inspect when possible.
7. Ask for a revision only if ambiguity blocks reconstruction.

## Underlay workflow

Use the bundled script to create a starter SVG with the sketch image placed as a faded reference layer:

```bash
python3 scripts/sketch_underlay_svg.py sketch.jpg output.svg --width 1600 --height 1000
```

Then draw clean vector geometry above it.

## Optional contour workflow

If Pillow is installed, the script can also estimate image size and create a normalized underlay. Do not treat automatically detected contours as final geometry unless the user specifically wants a trace.

## Reconstruction rules

Always:

- keep the original sketch in `reference_sketch` group
- put reconstructed elements in separate named groups
- keep labels editable
- keep callout arrows editable
- mark uncertain interpretations in comments or a short note

Avoid:

- copying accidental hand jitter
- overfitting to sketch proportions when the diagram needs conceptual clarity
- using image generation to "clean up" technical geometry
