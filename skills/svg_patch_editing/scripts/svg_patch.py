#!/usr/bin/env python3
"""
Apply simple JSON patches to an SVG by element ID.

Usage:
  python3 svg_patch.py input.svg output.svg patch.json

Patch format:
[
  {"op": "set_text", "id": "label1", "text": "New text"},
  {"op": "set_attr", "id": "thing", "attr": "stroke", "value": "#222"},
  {"op": "translate", "id": "inset", "dx": 50, "dy": -20},
  {"op": "delete", "id": "bad_arrow"},
  {"op": "replace_path", "id": "curve", "d": "M 0 0 L 10 10"},
  {"op": "add_child_raw", "id": "labels", "svg": "<text id='x' x='10' y='10'>Hi</text>"}
]
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

def parse_fragment(raw: str) -> ET.Element:
    wrapped = f'<g xmlns="{SVG_NS}">{raw}</g>'
    root = ET.fromstring(wrapped)
    if len(root) != 1:
        raise ValueError("add_child_raw requires exactly one top-level SVG element.")
    return copy.deepcopy(root[0])

def build_id_index(root):
    idx = {}
    parents = {}
    for parent in root.iter():
        for child in list(parent):
            parents[child] = parent
    for el in root.iter():
        eid = el.attrib.get("id")
        if eid:
            idx[eid] = el
    return idx, parents

def append_translate(transform: str, dx: float, dy: float) -> str:
    add = f"translate({dx:g} {dy:g})"
    if not transform:
        return add
    m = re.fullmatch(r"\s*translate\(([-0-9.]+)[ ,]+([-0-9.]+)\)\s*", transform)
    if m:
        return f"translate({float(m.group(1)) + dx:g} {float(m.group(2)) + dy:g})"
    return transform + " " + add

def apply_patch(root, op):
    idx, parents = build_id_index(root)
    eid = op.get("id")
    if not eid or eid not in idx:
        raise KeyError(f"Element id not found: {eid!r}")
    el = idx[eid]
    kind = op.get("op")

    if kind == "set_attr":
        el.set(op["attr"], str(op["value"]))
    elif kind == "set_text":
        el.text = str(op["text"])
        for child in list(el):
            el.remove(child)
    elif kind == "translate":
        dx, dy = float(op.get("dx", 0)), float(op.get("dy", 0))
        el.set("transform", append_translate(el.attrib.get("transform", ""), dx, dy))
    elif kind == "delete":
        parent = parents.get(el)
        if parent is None:
            raise ValueError("Cannot delete root element.")
        parent.remove(el)
    elif kind == "replace_path":
        el.set("d", op["d"])
    elif kind == "add_child_raw":
        child = parse_fragment(op["svg"])
        el.append(child)
    else:
        raise ValueError(f"Unknown op: {kind}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_svg")
    ap.add_argument("output_svg")
    ap.add_argument("patch_json")
    args = ap.parse_args()

    tree = ET.parse(args.input_svg)
    root = tree.getroot()
    patches = json.loads(Path(args.patch_json).read_text(encoding="utf-8"))
    if isinstance(patches, dict):
        patches = [patches]

    for op in patches:
        apply_patch(root, op)

    tree.write(args.output_svg, encoding="utf-8", xml_declaration=True)
    print(args.output_svg)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"svg_patch.py error: {e}", file=sys.stderr)
        sys.exit(2)
