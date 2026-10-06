# Helical slug streams as a prestress and actuation primitive for active-support structures

A concept paper on the control of an active-support structure. The reference case is an orbital ring built from magnetically guided slug streams that run in shallow helical lanes around a large membrane tube.

The paper is a [Quarto](https://quarto.org) book. One source builds a website and a PDF.

## Reading it

- **Website and PDF:** built by GitHub Actions on every push to `main`. The site is published to GitHub Pages once Pages is enabled for this repository (Settings → Pages → Source: GitHub Actions). The PDF is also attached to each workflow run as an artifact.
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

## Layout

| Path | Contents |
| --- | --- |
| `index.qmd` | Cover image and abstract |
| `notation.qmd` | Symbol tables |
| `chapters/` | Chapters 1 to 9 |
| `appendices/` | Appendices A to F |
| `figures/` | Figure files |
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
