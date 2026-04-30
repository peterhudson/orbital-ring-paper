---
name: geometric_diagram_construction
description: Construct technically correct SVG geometry for diagrams, including arcs, ellipses, helices, projected 3D objects, dimension arrows, coordinate frames, exploded views, orbital rings, and guide-shell cross-sections.
---

# Geometric Diagram Construction Skill

Use this skill when the figure depends on geometry being right, not merely attractive.

## Core principle

Draw from explicit construction. Define coordinates, dimensions, projections, and occlusion before creating SVG paths.

## Geometry workflow

1. Choose a coordinate system.
2. List physical or conceptual objects.
3. Assign drawing-space coordinates and scale.
4. Choose projection: orthographic, oblique, section view, or symbolic.
5. Compute paths from geometry.
6. Draw hidden/rear geometry before foreground geometry.
7. Add dimensions, arrows, and labels last.
8. Mark conceptual scale explicitly.

## Required checks

Before returning:

- Are arcs and ellipses geometrically consistent?
- Do arrows point to the intended object or gap?
- Are hidden lines dashed and foreground lines solid?
- Are handedness, flow direction, and local/global coordinates unambiguous?
- If a helix is shown, does it visibly wrap with a coherent pitch and handedness?
- If an inset is shown, does the callout connect to a plausible source region?
- If the diagram is not physically to scale, is that obvious or labelled?

## Helix convention

For a cylinder with axis parameter `s`, radius `r`, angular parameter `theta`, and pitch `p`:

- right-handed and left-handed helices must be visually distinguishable
- paired lanes should not cross unless the physical design requires it
- use arrowheads or small tangent markers to show flow direction
- use clipping, opacity, or dashed rear segments to separate front/back

## Orbital-ring convention

For orbital-ring figures:

- distinguish Earth surface, altitude gap, and ring/guide-shell structure
- avoid making a low-altitude ring look like a huge deep-space halo unless the figure is explicitly symbolic
- show ring foreground and background separately when possible
- keep detailed insets off to the side to avoid line clutter
- if altitude is exaggerated, label the exaggeration

## Use bundled script

Use `scripts/geometry_svg.py` for reusable geometric path generation, especially for:

- SVG path commands
- arrow endpoints
- ellipses and arcs
- helical paths on a projected cylinder
- sample orbital-ring figure generation
