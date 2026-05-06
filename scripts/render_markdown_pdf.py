#!/usr/bin/env python3
"""Render a Markdown file to a timestamped PDF.

Usage:
    python scripts/render_markdown_pdf.py [path/to/file.md] [--output-dir DIR]

Requires `pandoc` to be installed and available on PATH.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


WIDE_TABLE_LUA_FILTER = r"""
local function has_class(classes, target)
  for _, class in ipairs(classes) do
    if class == target then
      return true
    end
  end
  return false
end

function Div(el)
  if not has_class(el.classes, "wide-table") then
    return nil
  end

  local left = el.attributes["left"] or "-0.08\\textwidth"
  local right = el.attributes["right"] or left
  local begin_wide_table = "\\begingroup\\begin{adjustwidth}{"
    .. left
    .. "}{"
    .. right
    .. "}"
    .. "\\centering"
    .. "\\setlength{\\columnwidth}{\\linewidth}"
    .. "\\setlength{\\LTleft}{0pt plus 1fill}"
    .. "\\setlength{\\LTright}{0pt plus 1fill}"
  local blocks = {pandoc.RawBlock("latex", begin_wide_table)}

  for _, block in ipairs(el.content) do
    table.insert(blocks, block)
  end

  table.insert(blocks, pandoc.RawBlock("latex", "\\end{adjustwidth}\\endgroup"))
  return blocks
end
""".lstrip()


def build_output_name(input_path: Path, output_dir: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    filename = f"{input_path.stem}-{timestamp}.pdf"
    return output_dir / filename


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a Markdown file to a timestamped PDF using pandoc."
    )
    parser.add_argument(
        "markdown_file",
        nargs="?",
        default="docs/active-support-orbital-ring-using-momentum-inflated-slug-streams.md",
        help="Path to the .md file to render.",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory for generated PDFs (default: current directory).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.markdown_file).resolve()
    output_dir = Path(args.output_dir).resolve()

    if not input_path.exists() or input_path.suffix.lower() != ".md":
        print(f"Error: markdown file not found or not a .md file: {input_path}", file=sys.stderr)
        return 1

    if shutil.which("pandoc") is None:
        print(
            "Error: pandoc is not installed or not on PATH. Install pandoc first.",
            file=sys.stderr,
        )
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)
    output_pdf = build_output_name(input_path, output_dir)

    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        wide_table_filter = temp_dir / "wide-tables.lua"
        wide_table_filter.write_text(WIDE_TABLE_LUA_FILTER, encoding="utf-8")

        header_file = temp_dir / "wide-table-header.tex"
        header_file.write_text("\\usepackage{changepage}\n", encoding="utf-8")

        cmd = [
            "pandoc",
            str(input_path),
            "--resource-path",
            str(input_path.parent),
            "--lua-filter",
            str(wide_table_filter),
            "--include-in-header",
            str(header_file),
            "-o",
            str(output_pdf),
        ]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as exc:
            print(f"Error: pandoc failed with exit code {exc.returncode}", file=sys.stderr)
            return exc.returncode

    print(f"Generated PDF: {output_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
