# Project configuration

The renderer reads `project.json` from a project directory.

## Example

```json
{
  "name": "fictional-demo",
  "canvas": {"width": 1080, "height": 1920},
  "safe_area": {"left": 60, "right": 60, "top": 150, "bottom": 240},
  "font": null,
  "requires_product_reveal": true,
  "slides": [
    {
      "id": "01-hook",
      "type": "hook",
      "base": "01-hook-base.png",
      "output": "01-hook.png",
      "copy": "3 desk habits stealing your focus",
      "line_breaks": ["3 desk habits", "stealing your focus"],
      "text_center_y": 760,
      "font_start": 104
    }
  ]
}
```

## Root fields

- `name`: stable project identifier.
- `canvas.width`, `canvas.height`: positive integer output dimensions.
- `safe_area.left`, `right`, `top`, `bottom`: non-negative pixel margins.
- `font`: optional path to a TrueType or OpenType font. When null, the renderer checks `CAROUSEL_FONT` and portable system candidates.
- `requires_product_reveal`: whether at least one slide must have type `product-reveal`.
- `slides`: ordered, non-empty list of slide objects.

## Slide fields

- `id`: unique stable identifier.
- `type`: `hook`, `point`, `product-reveal`, or another descriptive type.
- `base`: filename inside `generated`.
- `output`: unique filename inside `slides`.
- `copy`: canonical caption for metadata and review.
- `line_breaks`: one or more strings rendered as fixed lines.
- `text_center_y`: vertical center of the caption block in pixels.
- `font_start`: maximum font size. The renderer decreases it until the caption fits.

## Project layout

```text
project/
|-- project.json
|-- generated/
|   `-- text-free base images
|-- slides/
|   `-- numbered publish-ready images
`-- qa/
    |-- contact-sheet.png
    |-- caption-metrics.json
    `-- validation-report.json
```

Do not put provider credentials or private keys in `project.json`.

