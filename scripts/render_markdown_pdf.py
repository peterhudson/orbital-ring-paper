#!/usr/bin/env python3
"""Render a Markdown file to a timestamped PDF with embedded figures/graphics.

Usage:
    python scripts/render_markdown_pdf.py [path/to/file.md] [--output-dir DIR]

Requirements:
- pandoc installed and available on PATH
- a HTML-capable PDF engine (defaults to `weasyprint`)
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_MARKDOWN = "docs/active-support-orbital-ring-using-momentum-inflated-slug-streams.md"


def build_output_name(input_path: Path, output_dir: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    filename = f"{input_path.stem}-{timestamp}.pdf"
    return output_dir / filename


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Render a Markdown file to a timestamped PDF (including figures/graphics) "
            "using pandoc."
        )
    )
    parser.add_argument(
        "markdown_file",
        nargs="?",
        default=DEFAULT_MARKDOWN,
        help="Path to the .md file to render.",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory for generated PDFs (default: current directory).",
    )
    parser.add_argument(
        "--pdf-engine",
        default="weasyprint",
        help=(
            "Pandoc PDF engine for HTML-rich markdown (default: weasyprint). "
            "Examples: weasyprint, wkhtmltopdf"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.markdown_file).resolve()
    output_dir = Path(args.output_dir).resolve()
    repo_root = Path(__file__).resolve().parents[1]

    if not input_path.exists() or input_path.suffix.lower() != ".md":
        print(f"Error: markdown file not found or not a .md file: {input_path}", file=sys.stderr)
        return 1

    if shutil.which("pandoc") is None:
        print("Error: pandoc is not installed or not on PATH. Install pandoc first.", file=sys.stderr)
        return 1

    if shutil.which(args.pdf_engine) is None:
        print(
            f"Error: PDF engine '{args.pdf_engine}' is not installed or not on PATH.",
            file=sys.stderr,
        )
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)
    output_pdf = build_output_name(input_path, output_dir)

    # Ensure relative image paths (e.g. ../figures/...) are resolved consistently.
    resource_path = ":".join(
        [
            str(input_path.parent),
            str(repo_root),
            str(repo_root / "figures"),
        ]
    )

    cmd = [
        "pandoc",
        str(input_path),
        "--standalone",
        "--from",
        "markdown+raw_html",
        "--to",
        "html5",
        "--resource-path",
        resource_path,
        "--pdf-engine",
        args.pdf_engine,
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
