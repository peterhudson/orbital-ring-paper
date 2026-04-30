#!/usr/bin/env python3
"""
Create a clean standalone SVG scaffold with markers, styles, and named layers.

Usage:
  python3 svg_scaffold.py output.svg --width 1600 --height 1000 --title "Figure"
"""
import argparse
from pathlib import Path
from xml.sax.saxutils import escape

def make_svg(width: int, height: int, title: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{width}" height="{height}" viewBox="0 0 {width} {height}"
     role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">Editable technical diagram scaffold.</desc>
  <defs>
    <style>
      .background {{ fill: #ffffff; }}
      .structure {{ fill: none; stroke: #222222; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }}
      .secondary {{ fill: none; stroke: #666666; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
      .hidden {{ fill: none; stroke: #999999; stroke-width: 2; stroke-dasharray: 8 8; stroke-linecap: round; stroke-linejoin: round; }}
      .dimension {{ fill: none; stroke: #222222; stroke-width: 2; marker-start: url(#arrow); marker-end: url(#arrow); }}
      .arrow {{ fill: none; stroke: #222222; stroke-width: 2.5; marker-end: url(#arrow); }}
      .label {{ font-family: Helvetica, Arial, sans-serif; font-size: 28px; fill: #222222; }}
      .small-label {{ font-family: Helvetica, Arial, sans-serif; font-size: 21px; fill: #333333; }}
      .note {{ font-family: Helvetica, Arial, sans-serif; font-size: 18px; fill: #555555; }}
    </style>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6"
            orient="auto-start-reverse" markerUnits="strokeWidth">
      <path d="M 0 0 L 12 6 L 0 12 z" fill="#222222"/>
    </marker>
  </defs>

  <rect id="page_background" class="background" x="0" y="0" width="{width}" height="{height}"/>

  <g id="reference_geometry"></g>
  <g id="hidden_geometry"></g>
  <g id="main_geometry"></g>
  <g id="dimensions"></g>
  <g id="arrows"></g>
  <g id="callouts"></g>
  <g id="labels"></g>
  <g id="insets"></g>
  <text id="not_to_scale_note" class="note" x="{width - 170}" y="{height - 28}">Not to scale</text>
</svg>
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("output")
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=1000)
    ap.add_argument("--title", default="Technical figure")
    args = ap.parse_args()

    Path(args.output).write_text(make_svg(args.width, args.height, args.title), encoding="utf-8")
    print(args.output)

if __name__ == "__main__":
    main()
