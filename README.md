# Helical slug streams as a prestress and actuation primitive for active-support structures

A concept paper on the control of an active-support structure. The reference case is an orbital ring built from magnetically guided slug streams that run in shallow helical lanes around a large membrane tube.

The paper is a [Quarto](https://quarto.org) book. One source builds a website and a PDF.

## Reading it

- **PDF:** built by GitHub Actions on every push and pull request, and attached to the workflow run as an artifact.
- **Website:** published to GitHub Pages from `main` once two switches are on: Pages enabled with "GitHub Actions" as the source (Settings → Pages), and the repository variable `PUBLISH_PAGES` set to `true` (Settings → Secrets and variables → Actions → Variables). Until then the deploy step is skipped.
- **On GitHub directly:** the `.qmd` files are readable as plain text, but GitHub does not render the equations, cross-references or figure captions. Use the built site or PDF.

## Building it locally

Requirements:

- Quarto 1.6 or newer
- A LaTeX distribution with XeLaTeX (`quarto install tinytex` is enough)
- `rsvg-convert` for the SVG figures in the PDF (`librsvg2-bin` on Debian/Ubuntu, `librsvg` on Homebrew)

```sh
quarto render            # website and PDF, into _book/
quarto render --to html  # website only
quarto render --to pdf   # PDF only
quarto preview           # live-reloading preview while editing
```

## Calculations

The numbers in the text come from `analysis/`, plain Python with numpy, scipy and matplotlib.

```sh
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

`analysis/params.py` holds every input of the reference case. `tests/test_refcase.py` checks each number quoted in the paper against it, so after changing an input the failing tests list the statements that need updating.

`analysis/truss.py` is the structural model used for the whole-ring results: a pin-jointed frame whose members also carry streams. `analysis/ring.py` and `analysis/ladder.py` build the ring and the two-chord frame from it, and `tests/test_ring.py` checks the model against the closed forms in the text.

Figures drawn from the calculations live in `figures/generated/` and are committed, so the book builds without Python. To redraw them:

```sh
python -m analysis.make_figures
```

## Layout

| Path | Contents |
| --- | --- |
| `index.qmd` | Cover image and abstract |
| `notation.qmd` | Symbol tables |
| `chapters/` | Chapters, numbered in reading order |
| `appendices/` | Appendices A to F |
| `figures/` | Figure files. `figures/generated/` is drawn by `analysis/make_figures.py`. |
| `analysis/` | Calculations and simulations |
| `tests/` | Checks that tie the text to the calculations |
| `_quarto.yml` | Book configuration: chapter order, output formats |

## Editing conventions

- **Headings** carry no numbers. Quarto numbers chapters, sections and appendices.
- **Cross-references** use labels, not typed numbers:
  - sections: `{#sec-name}` on the heading, `@sec-name` in the text
  - figures: `![Caption](../figures/file.svg){#fig-name}`, then `@fig-name`
  - equations: `$$ ... $$ {#eq-name}`, then `@eq-name`
- **Equations** are labelled only when they are a result or are referred to elsewhere.
- **Symbols** are listed in `notation.qmd`. Add new ones there, and check the list before reusing a letter.
- **Units** are SI.
