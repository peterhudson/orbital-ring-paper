# Repository Cleanup Plan

## Keep (minimal paper package)

These are the files required to preserve the main memo and the images it directly references:

- `docs/active-support-orbital-ring-using-momentum-inflated-slug-streams.md`
- `figures/orbital-ring-title-render-v2.jpeg`
- `figures/figure-1a-orbital-ring-global-geometry.svg`
- `figures/figure-1b-orbital-ring-local-helical-lanes-single-lane.svg`
- `figures/figure-2-balanced-four-lane-cell.svg`
- `figures/figure-2b-balanced-cell-force-cancellation.svg`
- `figures/figure-3-opposed-balanced-cells-bending.svg`
- `figures/figure-4-opposed-balanced-cells-moment.svg`

## Optional keep (if you want source/export history)

These are not required by the main markdown file, but may be useful to retain as working assets:

- Alternate cover render: `figures/orbital-ring-title-render.jpeg`
- Alternate Figure 1b artwork: `figures/figure-1b-orbital-ring-local-helical-lanes.svg`
- Raster/PDF exports for figures in use (if needed for publishing workflows)

## Remove candidates

Everything else in this repository appears removable for a minimal memo-only repo, including:

- Other papers/memos in `docs/`.
- All files in `docs/figures/`.
- DOCX/PDF interim/export copies of the paper unless explicitly needed.
- Unreferenced files in `figures/` (extra variants, PNG/PDF exports, construction artifacts).
- `skills/` tool scaffolding.
- `scripts/` automation scripts.
- `tmp/` scratch artifacts.
- `memory/` notes.
- Root metadata/docs not needed for publication-only storage (`README.md`, `USER.md`, `IDENTITY.md`) if you want a truly minimal archive.

## Safe cleanup sequence

1. Create a backup branch or zip archive.
2. Delete all remove candidates.
3. Run a broken-link check by searching markdown image refs and verifying each target exists.
4. Open the main markdown file in your renderer and visually confirm all figures load.
5. Commit as: `chore: prune repo to memo and referenced assets`.
