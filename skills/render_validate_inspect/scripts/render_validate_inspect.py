#!/usr/bin/env python3
"""
Validate, render, and lightly inspect an SVG.

Usage:
  python3 render_validate_inspect.py figure.svg --outdir previews
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "{http://www.w3.org/2000/svg}"

def strip_ns(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag

def validate_svg(svg_path: Path) -> dict:
    report = {"ok": True, "errors": [], "warnings": [], "stats": {}}
    try:
        tree = ET.parse(svg_path)
    except ET.ParseError as e:
        report["ok"] = False
        report["errors"].append(f"XML parse error: {e}")
        return report

    root = tree.getroot()
    if strip_ns(root.tag) != "svg":
        report["ok"] = False
        report["errors"].append("Root element is not <svg>.")
        return report

    attrs = root.attrib
    if "viewBox" not in attrs:
        report["warnings"].append("Missing viewBox.")
    if not list(root.iter(f"{SVG_NS}title")) and not any(strip_ns(e.tag) == "title" for e in root.iter()):
        report["warnings"].append("Missing <title>.")

    counts = {}
    ids = []
    texts = []
    embedded_images = 0
    for el in root.iter():
        name = strip_ns(el.tag)
        counts[name] = counts.get(name, 0) + 1
        if "id" in el.attrib:
            ids.append(el.attrib["id"])
        if name == "text":
            txt = "".join(el.itertext()).strip()
            if txt:
                texts.append(txt)
        if name == "image":
            embedded_images += 1

    groups = counts.get("g", 0)
    if groups < 3:
        report["warnings"].append(f"Only {groups} <g> groups found; technical figures should usually use named layers/groups.")
    if embedded_images:
        report["warnings"].append(f"Found {embedded_images} embedded/linked raster image element(s).")
    if counts.get("path", 0) > 200 and counts.get("text", 0) < 3:
        report["warnings"].append("Many paths but few text labels; check that the SVG is not an uneditable blob.")
    if not texts:
        report["warnings"].append("No text labels found.")

    duplicate_ids = sorted({x for x in ids if ids.count(x) > 1})
    if duplicate_ids:
        report["warnings"].append("Duplicate IDs: " + ", ".join(duplicate_ids[:20]))

    report["stats"] = {
        "element_counts": counts,
        "id_count": len(ids),
        "group_count": groups,
        "text_count": len(texts),
        "sample_text": texts[:20],
        "width": attrs.get("width"),
        "height": attrs.get("height"),
        "viewBox": attrs.get("viewBox"),
    }
    return report

def run(cmd: list[str]) -> tuple[bool, str]:
    try:
        cp = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        return cp.returncode == 0, (cp.stdout + cp.stderr).strip()
    except FileNotFoundError:
        return False, f"missing executable: {cmd[0]}"

def render_png(svg: Path, png: Path) -> tuple[bool, str]:
    if shutil.which("rsvg-convert"):
        return run(["rsvg-convert", "-f", "png", "-o", str(png), str(svg)])
    try:
        import cairosvg
        cairosvg.svg2png(url=str(svg), write_to=str(png))
        return True, "rendered with cairosvg"
    except Exception as e:
        if shutil.which("inkscape"):
            return run(["inkscape", str(svg), "--export-type=png", f"--export-filename={png}"])
        return False, f"No PNG renderer available. Install librsvg2-bin or cairosvg. Details: {e}"

def render_pdf(svg: Path, pdf: Path) -> tuple[bool, str]:
    if shutil.which("rsvg-convert"):
        return run(["rsvg-convert", "-f", "pdf", "-o", str(pdf), str(svg)])
    try:
        import cairosvg
        cairosvg.svg2pdf(url=str(svg), write_to=str(pdf))
        return True, "rendered with cairosvg"
    except Exception as e:
        if shutil.which("inkscape"):
            return run(["inkscape", str(svg), "--export-type=pdf", f"--export-filename={pdf}"])
        return False, f"No PDF renderer available. Install librsvg2-bin or cairosvg. Details: {e}"

def inspect_png(png: Path) -> dict:
    out = {"exists": png.exists(), "size_bytes": png.stat().st_size if png.exists() else 0}
    try:
        from PIL import Image
        with Image.open(png) as im:
            out.update({"width": im.width, "height": im.height, "mode": im.mode})
    except Exception as e:
        out["warning"] = f"Pillow not available or failed to inspect PNG: {e}"
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    svg = Path(args.svg)
    outdir = Path(args.outdir) if args.outdir else svg.parent
    outdir.mkdir(parents=True, exist_ok=True)

    report = validate_svg(svg)

    png = outdir / (svg.stem + ".png")
    pdf = outdir / (svg.stem + ".pdf")

    if report["ok"]:
        ok_png, msg_png = render_png(svg, png)
        ok_pdf, msg_pdf = render_pdf(svg, pdf)
        report["render"] = {
            "png": {"ok": ok_png, "path": str(png) if ok_png else None, "message": msg_png},
            "pdf": {"ok": ok_pdf, "path": str(pdf) if ok_pdf else None, "message": msg_pdf},
        }
        if ok_png:
            report["png_inspection"] = inspect_png(png)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("SVG:", svg)
        print("OK:", report["ok"])
        for e in report["errors"]:
            print("ERROR:", e)
        for w in report["warnings"]:
            print("WARNING:", w)
        if "render" in report:
            for kind, r in report["render"].items():
                print(f"{kind.upper()}:", "ok" if r["ok"] else "failed", r["path"] or "", "-", r["message"])
        print("Stats:", json.dumps(report.get("stats", {}), indent=2))

    sys.exit(0 if report["ok"] else 2)

if __name__ == "__main__":
    main()
