#!/usr/bin/env python3
"""
Generate a structured technical-figure red-team checklist from an SVG.

Usage:
  python3 figure_redteam_template.py figure.svg --intent "Show altitude gap and helical lanes"
"""
from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

def strip_ns(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag

def inspect(svg_path: Path):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    counts = {}
    ids = []
    texts = []
    for el in root.iter():
        name = strip_ns(el.tag)
        counts[name] = counts.get(name, 0) + 1
        if "id" in el.attrib:
            ids.append(el.attrib["id"])
        if name == "text":
            t = "".join(el.itertext()).strip()
            if t:
                texts.append(t)
    return counts, ids, texts, root.attrib

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg")
    ap.add_argument("--intent", default="")
    args = ap.parse_args()
    counts, ids, texts, attrs = inspect(Path(args.svg))

    print("# Technical figure red-team")
    print()
    print("## Inputs")
    print(f"- SVG: `{args.svg}`")
    if args.intent:
        print(f"- Intended purpose: {args.intent}")
    print(f"- ViewBox: `{attrs.get('viewBox', 'MISSING')}`")
    print(f"- Width/height: `{attrs.get('width', '?')}` × `{attrs.get('height', '?')}`")
    print(f"- Groups: {counts.get('g', 0)}")
    print(f"- Paths: {counts.get('path', 0)}")
    print(f"- Text labels: {len(texts)}")
    print()
    print("## Existing IDs")
    for i in ids[:80]:
        print(f"- `{i}`")
    if len(ids) > 80:
        print(f"- ... {len(ids)-80} more")
    print()
    print("## Text labels found")
    for t in texts[:40]:
        print(f"- {t}")
    if len(texts) > 40:
        print(f"- ... {len(texts)-40} more")
    print()
    print("## Review checklist")
    checks = [
        "Does the figure communicate the intended claim without relying on hidden context?",
        "Are arrows pointing to the correct targets, not merely nearby visual objects?",
        "Are dimensions measuring gaps/thicknesses/radii that match their labels?",
        "Are hidden/rear-side elements dashed or visually subordinate?",
        "Are foreground/background relationships unambiguous?",
        "Are handedness, directionality, and flow arrows shown where needed?",
        "Are labels outside dense geometry and free of line collisions?",
        "Is any scale exaggeration labelled?",
        "Would the figure still work in grayscale?",
        "Are semantic colours used consistently?",
        "Are named groups present for later editing?",
        "Does the caption match the actual visual encoding?"
    ]
    for c in checks:
        print(f"- [ ] {c}")
    print()
    print("## Findings")
    print("### BLOCKER")
    print("- ")
    print()
    print("### MAJOR")
    print("- ")
    print()
    print("### MINOR")
    print("- ")
    print()
    print("## Patch plan")
    print("1. ")

if __name__ == "__main__":
    main()
