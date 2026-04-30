#!/usr/bin/env python3
"""
Geometry helpers for deterministic SVG technical figures.

Useful modes:
  python3 geometry_svg.py helix --output helix.svg
  python3 geometry_svg.py orbital-ring-demo --output orbital_ring_demo.svg

This script is intentionally dependency-free.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Iterable, List, Tuple

Point = Tuple[float, float]

def fmt(x: float) -> str:
    return f"{x:.3f}".rstrip("0").rstrip(".")

def polyline_path(points: Iterable[Point]) -> str:
    pts = list(points)
    if not pts:
        return ""
    head = f"M {fmt(pts[0][0])} {fmt(pts[0][1])}"
    tail = " ".join(f"L {fmt(x)} {fmt(y)}" for x, y in pts[1:])
    return f"{head} {tail}".strip()

def ellipse_arc_path(cx: float, cy: float, rx: float, ry: float, a0: float, a1: float) -> str:
    """SVG path for an elliptical arc. Angles in radians."""
    x0, y0 = cx + rx * math.cos(a0), cy + ry * math.sin(a0)
    x1, y1 = cx + rx * math.cos(a1), cy + ry * math.sin(a1)
    da = (a1 - a0) % (2 * math.pi)
    large = 1 if da > math.pi else 0
    sweep = 1
    return f"M {fmt(x0)} {fmt(y0)} A {fmt(rx)} {fmt(ry)} 0 {large} {sweep} {fmt(x1)} {fmt(y1)}"

def projected_cylinder_helix(
    cx: float,
    cy: float,
    length: float,
    radius_y: float,
    turns: float,
    phase: float = 0.0,
    handedness: int = 1,
    samples: int = 240,
) -> List[Point]:
    """
    Project a helix on a horizontal cylinder into 2D.
    x maps along cylinder axis.
    y oscillates sinusoidally around the visible cylinder.
    handedness = +1 or -1.
    """
    pts: List[Point] = []
    for i in range(samples + 1):
        t = i / samples
        x = cx - length / 2 + length * t
        theta = handedness * 2 * math.pi * turns * t + phase
        y = cy + radius_y * math.sin(theta)
        pts.append((x, y))
    return pts

def path_segments_by_visibility(points: List[Point], visible_fn) -> Tuple[List[List[Point]], List[List[Point]]]:
    visible, hidden = [], []
    cur = []
    cur_state = None
    for p in points:
        state = bool(visible_fn(p))
        if cur_state is None:
            cur_state = state
            cur = [p]
        elif state == cur_state:
            cur.append(p)
        else:
            if len(cur) >= 2:
                (visible if cur_state else hidden).append(cur)
            cur = [p]
            cur_state = state
    if len(cur) >= 2:
        (visible if cur_state else hidden).append(cur)
    return visible, hidden

def svg_header(width: int, height: int, title: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<title>{title}</title>
<defs>
<style>
  .bg {{ fill: white; }}
  .structure {{ fill:none; stroke:#222; stroke-width:3; stroke-linecap:round; stroke-linejoin:round; }}
  .secondary {{ fill:none; stroke:#666; stroke-width:2; stroke-linecap:round; stroke-linejoin:round; }}
  .hidden {{ fill:none; stroke:#999; stroke-width:2; stroke-dasharray:8 8; stroke-linecap:round; stroke-linejoin:round; }}
  .lane-a {{ fill:none; stroke:#1f77b4; stroke-width:4; stroke-linecap:round; stroke-linejoin:round; }}
  .lane-b {{ fill:none; stroke:#d62728; stroke-width:4; stroke-linecap:round; stroke-linejoin:round; }}
  .label {{ font-family:Helvetica,Arial,sans-serif; font-size:24px; fill:#222; }}
  .small {{ font-family:Helvetica,Arial,sans-serif; font-size:18px; fill:#555; }}
  .dimension {{ fill:none; stroke:#222; stroke-width:2; marker-start:url(#arrow); marker-end:url(#arrow); }}
  .arrow {{ fill:none; stroke:#222; stroke-width:2.5; marker-end:url(#arrow); }}
</style>
<marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto-start-reverse" markerUnits="strokeWidth">
  <path d="M 0 0 L 12 6 L 0 12 z" fill="#222"/>
</marker>
</defs>
<rect class="bg" x="0" y="0" width="{width}" height="{height}"/>
"""

def svg_footer() -> str:
    return "</svg>\n"

def helix_demo(output: Path):
    width, height = 1200, 650
    cx, cy = 600, 320
    length, ry = 760, 95
    lane1 = projected_cylinder_helix(cx, cy, length, ry, turns=5.5, phase=0, handedness=1)
    lane2 = projected_cylinder_helix(cx, cy, length, ry, turns=5.5, phase=math.pi, handedness=-1)

    parts = [svg_header(width, height, "Helical guide lane pair")]
    parts.append('<g id="guide_shell">\n')
    parts.append(f'<rect class="secondary" x="{fmt(cx-length/2)}" y="{fmt(cy-ry)}" width="{fmt(length)}" height="{fmt(2*ry)}" rx="30"/>\n')
    parts.append(f'<ellipse class="structure" cx="{fmt(cx-length/2)}" cy="{fmt(cy)}" rx="28" ry="{fmt(ry)}"/>\n')
    parts.append(f'<ellipse class="structure" cx="{fmt(cx+length/2)}" cy="{fmt(cy)}" rx="28" ry="{fmt(ry)}"/>\n')
    parts.append('</g>\n')

    for gid, cls, pts in [("right_handed_lane", "lane-a", lane1), ("left_handed_lane", "lane-b", lane2)]:
        visible, hidden = path_segments_by_visibility(pts, lambda p: p[1] >= cy)
        parts.append(f'<g id="{gid}">\n')
        for seg in hidden:
            parts.append(f'  <path class="hidden" d="{polyline_path(seg)}"/>\n')
        for seg in visible:
            parts.append(f'  <path class="{cls}" d="{polyline_path(seg)}"/>\n')
        parts.append('</g>\n')

    parts.append('<g id="labels">\n')
    parts.append('<text class="label" x="190" y="130">Projected helical guide lanes</text>\n')
    parts.append('<text class="small" x="190" y="160">Solid = foreground side; dashed = rear side</text>\n')
    parts.append('<text class="small" x="260" y="560">Blue and red lanes have opposite handedness and phase</text>\n')
    parts.append('</g>\n')
    parts.append(svg_footer())
    output.write_text("".join(parts), encoding="utf-8")

def orbital_ring_demo(output: Path):
    width, height = 1600, 1000
    cx, cy = 680, 560
    earth_r = 245
    ring_r = 330
    parts = [svg_header(width, height, "Orbital ring conceptual geometry demo")]
    parts.append('<g id="earth">\n')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{earth_r}" fill="#d8e7f3" stroke="#335" stroke-width="2"/>\n')
    parts.append(f'<text class="label" x="{cx-35}" y="{cy+8}">Earth</text>\n')
    parts.append('</g>\n')

    parts.append('<g id="orbital_ring">\n')
    parts.append(f'<path id="ring_background" class="hidden" d="{ellipse_arc_path(cx, cy, ring_r, ring_r*0.33, math.pi, 2*math.pi)}"/>\n')
    parts.append(f'<path id="ring_foreground" class="structure" d="{ellipse_arc_path(cx, cy, ring_r, ring_r*0.33, 0, math.pi)}"/>\n')
    parts.append('</g>\n')

    x = cx + ring_r + 65
    y0 = cy - earth_r*0.33
    y1 = cy - ring_r*0.33
    parts.append('<g id="altitude_dimension">\n')
    parts.append(f'<path class="dimension" d="M {fmt(x)} {fmt(y0)} L {fmt(x)} {fmt(y1)}"/>\n')
    parts.append(f'<path class="secondary" d="M {fmt(cx+earth_r)} {fmt(y0)} L {fmt(x-12)} {fmt(y0)}"/>\n')
    parts.append(f'<path class="secondary" d="M {fmt(cx+ring_r)} {fmt(y1)} L {fmt(x-12)} {fmt(y1)}"/>\n')
    parts.append(f'<text id="altitude_label" class="label" x="{fmt(x+18)}" y="{fmt((y0+y1)/2+8)}">500 km altitude gap</text>\n')
    parts.append('</g>\n')

    ix, iy = 1220, 515
    parts.append('<g id="guide_shell_inset">\n')
    parts.append('<rect x="1010" y="230" width="500" height="460" rx="22" fill="#fff" stroke="#ccc" stroke-width="2"/>\n')
    parts.append('<text class="label" x="1040" y="280">Guide-shell inset</text>\n')
    length, ry = 360, 55
    lane1 = projected_cylinder_helix(ix, iy, length, ry, 3.2, 0, 1, 160)
    lane2 = projected_cylinder_helix(ix, iy, length, ry, 3.2, math.pi, -1, 160)
    parts.append(f'<rect class="secondary" x="{fmt(ix-length/2)}" y="{fmt(iy-ry)}" width="{fmt(length)}" height="{fmt(2*ry)}" rx="20"/>\n')
    for gid, cls, pts in [("inset_lane_a", "lane-a", lane1), ("inset_lane_b", "lane-b", lane2)]:
        visible, hidden = path_segments_by_visibility(pts, lambda p: p[1] >= iy)
        parts.append(f'<g id="{gid}">\n')
        for seg in hidden:
            parts.append(f'  <path class="hidden" d="{polyline_path(seg)}"/>\n')
        for seg in visible:
            parts.append(f'  <path class="{cls}" d="{polyline_path(seg)}"/>\n')
        parts.append('</g>\n')
    parts.append('<text class="small" x="1040" y="650">Opposite-handed helical lanes on cylindrical guide shell</text>\n')
    parts.append('</g>\n')

    parts.append('<g id="callout">\n')
    parts.append('<path class="arrow" d="M 1000 600 C 900 610 850 660 790 665"/>\n')
    parts.append('</g>\n')
    parts.append('<text class="small" x="1320" y="940">Conceptual, not to scale</text>\n')
    parts.append(svg_footer())
    output.write_text("".join(parts), encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    h = sub.add_parser("helix")
    h.add_argument("--output", default="helix_demo.svg")

    o = sub.add_parser("orbital-ring-demo")
    o.add_argument("--output", default="orbital_ring_demo.svg")

    args = ap.parse_args()
    if args.cmd == "helix":
        helix_demo(Path(args.output))
    elif args.cmd == "orbital-ring-demo":
        orbital_ring_demo(Path(args.output))
    print(args.output)

if __name__ == "__main__":
    main()
