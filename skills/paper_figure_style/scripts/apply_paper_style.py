#!/usr/bin/env python3
"""
Inject a conservative paper-figure style block and arrow marker into an SVG.

Usage:
  python3 apply_paper_style.py input.svg output.svg
"""
from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

STYLE_TEXT = """
.background { fill: #ffffff; }
.structure { fill: none; stroke: #222222; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }
.secondary { fill: none; stroke: #666666; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.hidden { fill: none; stroke: #999999; stroke-width: 2; stroke-dasharray: 8 8; stroke-linecap: round; stroke-linejoin: round; }
.dimension { fill: none; stroke: #222222; stroke-width: 2; marker-start: url(#arrow); marker-end: url(#arrow); }
.arrow { fill: none; stroke: #222222; stroke-width: 2.5; marker-end: url(#arrow); }
.label { font-family: Helvetica, Arial, sans-serif; font-size: 28px; fill: #222222; }
.small-label, .small { font-family: Helvetica, Arial, sans-serif; font-size: 21px; fill: #333333; }
.note { font-family: Helvetica, Arial, sans-serif; font-size: 18px; fill: #555555; }
.lane-a { fill: none; stroke: #1f77b4; stroke-width: 4; stroke-linecap: round; stroke-linejoin: round; }
.lane-b { fill: none; stroke: #d62728; stroke-width: 4; stroke-linecap: round; stroke-linejoin: round; }
.earth { fill: #d8e7f3; stroke: #333355; stroke-width: 2; }
"""

def q(tag: str) -> str:
    return f"{{{SVG_NS}}}{tag}"

def ensure_defs(root):
    defs = root.find(q("defs"))
    if defs is None:
        defs = ET.Element(q("defs"))
        root.insert(0, defs)
    return defs

def remove_existing_style(defs):
    for child in list(defs):
        if child.tag == q("style") and child.attrib.get("id") == "paper_figure_style":
            defs.remove(child)
        if child.tag == q("marker") and child.attrib.get("id") == "arrow":
            defs.remove(child)

def add_style(defs):
    style = ET.Element(q("style"), {"id": "paper_figure_style"})
    style.text = STYLE_TEXT
    defs.insert(0, style)

    marker = ET.Element(q("marker"), {
        "id": "arrow",
        "markerWidth": "12",
        "markerHeight": "12",
        "refX": "10",
        "refY": "6",
        "orient": "auto-start-reverse",
        "markerUnits": "strokeWidth",
    })
    path = ET.Element(q("path"), {"d": "M 0 0 L 12 6 L 0 12 z", "fill": "#222222"})
    marker.append(path)
    defs.append(marker)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_svg")
    ap.add_argument("output_svg")
    args = ap.parse_args()

    tree = ET.parse(args.input_svg)
    root = tree.getroot()
    defs = ensure_defs(root)
    remove_existing_style(defs)
    add_style(defs)
    tree.write(args.output_svg, encoding="utf-8", xml_declaration=True)
    print(args.output_svg)

if __name__ == "__main__":
    main()
