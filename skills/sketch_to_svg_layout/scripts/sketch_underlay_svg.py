#!/usr/bin/env python3
"""
Create an SVG scaffold with a raster sketch as a faded underlay.

Usage:
  python3 sketch_underlay_svg.py sketch.jpg output.svg --width 1600 --height 1000
"""
from __future__ import annotations

import argparse
import base64
import mimetypes
from pathlib import Path
from xml.sax.saxutils import escape

def image_size(path: Path):
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.width, im.height
    except Exception:
        return None, None

def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sketch")
    ap.add_argument("output")
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=1000)
    ap.add_argument("--opacity", type=float, default=0.22)
    ap.add_argument("--link", action="store_true", help="Link image file instead of embedding it.")
    args = ap.parse_args()

    sketch = Path(args.sketch)
    iw, ih = image_size(sketch)
    width, height = args.width, args.height

    if iw and ih:
        scale = min(width / iw, height / ih) * 0.92
        draw_w, draw_h = iw * scale, ih * scale
    else:
        draw_w, draw_h = width * 0.86, height * 0.86

    x, y = (width - draw_w) / 2, (height - draw_h) / 2
    href = escape(str(sketch)) if args.link else data_uri(sketch)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<title>Sketch reconstruction scaffold</title>
<defs>
<style>
  .bg {{ fill: white; }}
  .structure {{ fill:none; stroke:#222; stroke-width:3; stroke-linecap:round; stroke-linejoin:round; }}
  .hidden {{ fill:none; stroke:#999; stroke-width:2; stroke-dasharray:8 8; }}
  .arrow {{ fill:none; stroke:#222; stroke-width:2.5; marker-end:url(#arrow); }}
  .label {{ font-family:Helvetica,Arial,sans-serif; font-size:28px; fill:#222; }}
  .small {{ font-family:Helvetica,Arial,sans-serif; font-size:18px; fill:#555; }}
</style>
<marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto-start-reverse" markerUnits="strokeWidth">
  <path d="M 0 0 L 12 6 L 0 12 z" fill="#222"/>
</marker>
</defs>
<rect id="page_background" class="bg" x="0" y="0" width="{width}" height="{height}"/>
<g id="reference_sketch" opacity="{args.opacity}">
  <image href="{href}" x="{x:.3f}" y="{y:.3f}" width="{draw_w:.3f}" height="{draw_h:.3f}" preserveAspectRatio="xMidYMid meet"/>
</g>
<g id="reconstructed_geometry"></g>
<g id="dimensions"></g>
<g id="arrows"></g>
<g id="labels"></g>
<g id="notes">
  <text class="small" x="24" y="{height-24}">Sketch underlay is for layout reference only; final geometry should be reconstructed as editable vectors.</text>
</g>
</svg>
"""
    Path(args.output).write_text(svg, encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()
