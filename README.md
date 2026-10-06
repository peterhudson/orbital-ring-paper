# Helical slug streams as a prestress and actuation primitive for active-support structures

A concept paper on the control of an active-support structure. The reference case is an orbital ring built from magnetically guided slug streams that run in shallow helical lanes around a large membrane tube.

The paper is a [Quarto](https://quarto.org) book. One source builds a website and a PDF. A nine-page version, `paper/short-paper.qmd`, states the main results without the derivations.

## Reading it

- **Website:** <https://peterhudson.github.io/orbital-ring-paper/>, published from `main` by GitHub Actions. (Publishing needs Pages enabled with "GitHub Actions" as the source, and the repository variable `PUBLISH_PAGES` set to `true`.)
- **PDFs:** the book and the short paper are built on every push and pull request and attached to the workflow run as an artifact. On the website they are `orbital-ring-paper.pdf` and `short-paper.pdf`.
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

quarto render paper/short-paper.qmd --to pdf   # the short paper, into paper/
```

The short paper takes its figures from `figures/generated/` and its numbers from the book. When a test fails after a change of input, both need the new number.

## Calculations

The numbers in the text come from `analysis/`, plain Python with numpy, scipy and matplotlib.

```sh
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

`analysis/params.py` holds every input of the reference case. `tests/test_refcase.py` checks each number quoted in the paper against it, so after changing an input the failing tests list the statements that need updating.

Three models of the whole ring check one another. `analysis/truss.py` is a pin-jointed frame whose members also carry streams; `analysis/ring.py` and `analysis/ladder.py` build the ring and a two-chord frame from it. `analysis/ring_modes.py` is a linear model, one mode at a time, in which each stream has its own position, speed and spacing. `analysis/ring_particles.py` is a nonlinear simulation of the ring with the streams as separate slugs. `tests/test_ring.py` and `tests/test_ring_modes.py` compare them with each other and with the closed forms in the text.

Shape control has its own pair of models for a straight run of ring, `analysis/collective.py` (eigenvalues per wavelength) and `analysis/particles.py` (a particle simulation), and `analysis/ring_control.py` builds the controllers for the whole ring, which `analysis/ring_particles.py` can then run. `tests/test_collective.py` and `tests/test_ring_control.py` check the simulations against the linear predictions.

`analysis/ring_loads.py` adds up the modes to give the ring's response to a point load, put on suddenly or moving, with steering alone and with the stators holding the long modes (`tests/test_ring_loads.py`).

`analysis/ring_balance.py` asks what unequal streams do to the controlled ring (`tests/test_ring_balance.py`).

`analysis/closure.py` turns the closure loop into a gain (`tests/test_closure.py`).

`analysis/generalize.py` applies the same force balance to arches and columns of momentum and to rings on other worlds (`tests/test_generalize.py`). `tests/test_figures.py` pins the numbers behind the explanatory figures.

The whole suite takes about a minute, most of it in the particle simulations.

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
| `paper/` | The short paper: one file and its own small Quarto project |
| `references.bib` | Bibliography. Each entry was checked against a publisher or library record. |
| `_quarto.yml` | Book configuration: chapter order, output formats |

## Editing conventions

- **Headings** carry no numbers. Quarto numbers chapters, sections and appendices.
- **Cross-references** use labels, not typed numbers:
  - sections: `{#sec-name}` on the heading, `@sec-name` in the text
  - figures: `![Caption](../figures/file.svg){#fig-name}`, then `@fig-name`
  - equations: `$$ ... $$ {#eq-name}`, then `@eq-name`
- **Equations** are labeled only when they are a result or are referred to elsewhere.
- **Citations** use keys from `references.bib`: `[@lofstrom1985launch]`. Cite a source only for what it has been checked to say.
- **Symbols** are listed in `notation.qmd`. Add new ones there, and check the list before reusing a letter.
- **Units** are SI.
