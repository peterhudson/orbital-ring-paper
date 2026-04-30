---
name: svg_patch_editing
description: Make targeted edits to existing SVG diagrams without regenerating the whole figure. Use for moving groups, changing labels, changing attributes, replacing path data, deleting elements, and preserving unrelated geometry.
---

# SVG Patch Editing Skill

Use this skill when the user asks for a revision to an existing SVG.

## Core principle

Patch, do not redraw. Preserve all unrelated geometry, IDs, styles, and labels.

## Revision workflow

1. Read the existing SVG.
2. Identify target element by ID, group, label text, or nearby context.
3. Prefer ID-based edits.
4. Apply the smallest safe patch.
5. Validate XML.
6. Render preview if possible.
7. Report changed IDs and unchanged assumptions.

## Supported patch types

Use the bundled script for simple JSON-defined operations:

- `set_attr`: set an XML attribute on an element by ID
- `set_text`: replace text content of a text element by ID
- `translate`: append or update a `transform="translate(dx dy)"` on an element by ID
- `delete`: remove an element by ID
- `replace_path`: replace `d` attribute on a path by ID
- `add_child_raw`: add raw SVG markup inside a group by ID

## Example patch file

```json
[
  {"op": "set_text", "id": "altitude_label", "text": "500 km altitude gap"},
  {"op": "translate", "id": "guide_shell_inset", "dx": 80, "dy": -20},
  {"op": "set_attr", "id": "ring_foreground", "attr": "stroke-width", "value": "4"}
]
```

Run:

```bash
python3 scripts/svg_patch.py input.svg output.svg patch.json
```

## Safety rules

- Never use broad regex replacement for SVG unless ID-based patching is impossible.
- Do not delete unlabeled groups unless the intent is clear.
- Preserve XML namespaces.
- Keep a backup or write to a new output file.
- After patching, run render/validate/inspect if available.
