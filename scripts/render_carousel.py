from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


SYSTEM_FONT_CANDIDATES = [
    Path(r"C:\Windows\Fonts\arialbd.ttf"),
    Path(r"C:\Windows\Fonts\segoeuib.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    Path("/Library/Fonts/Arial Bold.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
]


def load_config(path: Path) -> dict:
    config = json.loads(path.read_text(encoding="utf-8"))
    validate_config(config)
    return config


def validate_config(config: dict) -> None:
    canvas = config.get("canvas", {})
    if not all(isinstance(canvas.get(key), int) and canvas[key] > 0 for key in ("width", "height")):
        raise ValueError("canvas width and height must be positive integers")

    safe_area = config.get("safe_area", {})
    if not all(isinstance(safe_area.get(key), int) and safe_area[key] >= 0 for key in ("left", "right", "top", "bottom")):
        raise ValueError("safe_area values must be non-negative integers")
    if safe_area["left"] + safe_area["right"] >= canvas["width"]:
        raise ValueError("horizontal safe area leaves no usable canvas")
    if safe_area["top"] + safe_area["bottom"] >= canvas["height"]:
        raise ValueError("vertical safe area leaves no usable canvas")

    slides = config.get("slides")
    if not isinstance(slides, list) or not slides:
        raise ValueError("slides must be a non-empty list")

    ids = [slide.get("id") for slide in slides]
    outputs = [slide.get("output") for slide in slides]
    if any(not value for value in ids) or len(set(ids)) != len(ids):
        raise ValueError("slide ids must be non-empty and unique")
    if any(not value for value in outputs) or len(set(outputs)) != len(outputs):
        raise ValueError("slide outputs must be non-empty and unique")

    required = {"type", "base", "copy", "line_breaks", "text_center_y", "font_start"}
    for slide in slides:
        missing = required.difference(slide)
        if missing:
            raise ValueError(f"slide {slide.get('id')} is missing fields: {sorted(missing)}")
        if not isinstance(slide["line_breaks"], list) or not slide["line_breaks"]:
            raise ValueError(f"slide {slide['id']} must define line_breaks")
        if not all(isinstance(line, str) and line.strip() for line in slide["line_breaks"]):
            raise ValueError(f"slide {slide['id']} contains an empty caption line")


def find_font(explicit: str | Path | None = None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    if os.environ.get("CAROUSEL_FONT"):
        candidates.append(Path(os.environ["CAROUSEL_FONT"]).expanduser())
    candidates.extend(SYSTEM_FONT_CANDIDATES)
    for path in candidates:
        if path.is_file():
            return path
    raise FileNotFoundError(
        "No bold TrueType font was found. Set CAROUSEL_FONT or project.json font to a .ttf/.otf file."
    )


def cover_crop(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(
        image.convert("RGB"),
        size,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )


def fit_caption(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    start_size: int,
    max_width: int,
    max_height: int,
    font_path: Path,
) -> tuple[ImageFont.FreeTypeFont, int, list[tuple[int, int, int, int]]]:
    for size in range(int(start_size), 11, -2):
        font = ImageFont.truetype(str(font_path), size=size)
        spacing = max(4, int(size * 0.14))
        stroke = max(2, int(size * 0.09))
        boxes = [draw.textbbox((0, 0), line, font=font, stroke_width=stroke) for line in lines]
        widths = [box[2] - box[0] for box in boxes]
        heights = [box[3] - box[1] for box in boxes]
        total_height = sum(heights) + spacing * (len(lines) - 1)
        if max(widths) <= max_width and total_height <= max_height:
            return font, spacing, boxes
    raise ValueError(f"caption cannot fit within the configured area: {lines}")


def add_caption(
    canvas: Image.Image,
    slide: dict,
    safe_area: dict,
    font_path: Path,
) -> dict[str, int]:
    draw = ImageDraw.Draw(canvas)
    lines = list(slide["line_breaks"])
    max_width = canvas.width - safe_area["left"] - safe_area["right"]
    safe_height = canvas.height - safe_area["top"] - safe_area["bottom"]
    max_height = min(int(slide.get("caption_max_height", canvas.height * 0.22)), safe_height)
    font, spacing, boxes = fit_caption(
        draw,
        lines,
        int(slide["font_start"]),
        max_width,
        max_height,
        font_path,
    )
    heights = [box[3] - box[1] for box in boxes]
    total_height = sum(heights) + spacing * (len(lines) - 1)
    y = int(slide["text_center_y"]) - total_height // 2
    metrics = {
        "left": canvas.width,
        "right": 0,
        "top": y,
        "bottom": 0,
        "font_size": font.size,
    }
    stroke = max(2, int(font.size * 0.09))
    shadow_stroke = stroke + max(1, int(font.size * 0.03))

    for line, box, height in zip(lines, boxes, heights):
        width = box[2] - box[0]
        x = (canvas.width - width) // 2
        draw.text(
            (x + 2, y + 4),
            line,
            font=font,
            fill=(0, 0, 0),
            stroke_width=shadow_stroke,
            stroke_fill=(0, 0, 0),
        )
        draw.text(
            (x, y),
            line,
            font=font,
            fill=(255, 255, 255),
            stroke_width=stroke,
            stroke_fill=(0, 0, 0),
        )
        metrics["left"] = min(metrics["left"], x)
        metrics["right"] = max(metrics["right"], x + width)
        metrics["bottom"] = max(metrics["bottom"], y + height)
        y += height + spacing

    if metrics["left"] < safe_area["left"] or metrics["right"] > canvas.width - safe_area["right"]:
        raise ValueError(f"caption violates horizontal safe area: {metrics}")
    if metrics["top"] < safe_area["top"] or metrics["bottom"] > canvas.height - safe_area["bottom"]:
        raise ValueError(f"caption violates vertical safe area: {metrics}")
    return metrics


def make_contact_sheet(images: list[Image.Image], output: Path) -> None:
    thumb_height = 480
    thumb_width = max(1, round(images[0].width * thumb_height / images[0].height))
    sheet = Image.new("RGB", (thumb_width * len(images), thumb_height), "white")
    for index, image in enumerate(images):
        sheet.paste(image.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS), (index * thumb_width, 0))
    sheet.save(output, format="PNG", optimize=True)


def render_project(project_dir: Path) -> dict:
    project_dir = Path(project_dir).resolve()
    config = load_config(project_dir / "project.json")
    canvas_size = (int(config["canvas"]["width"]), int(config["canvas"]["height"]))
    generated = project_dir / "generated"
    slides_dir = project_dir / "slides"
    qa_dir = project_dir / "qa"
    slides_dir.mkdir(parents=True, exist_ok=True)
    qa_dir.mkdir(parents=True, exist_ok=True)
    font_path = find_font(config.get("font"))
    rendered: list[Image.Image] = []
    metrics: list[dict] = []

    for index, slide in enumerate(config["slides"], start=1):
        source = generated / slide["base"]
        if not source.is_file() or source.stat().st_size == 0:
            raise FileNotFoundError(f"missing or empty base image: {source}")
        with Image.open(source) as base_image:
            canvas = cover_crop(base_image, canvas_size)
        caption_metrics = add_caption(canvas, slide, config["safe_area"], font_path)
        output = slides_dir / slide["output"]
        canvas.save(output, format="PNG", optimize=True)
        rendered.append(canvas.copy())
        metrics.append({"index": index, "id": slide["id"], "file": slide["output"], **caption_metrics})

    metrics_path = qa_dir / "caption-metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    make_contact_sheet(rendered, qa_dir / "contact-sheet.png")
    return {
        "status": "pass",
        "project": config.get("name", project_dir.name),
        "rendered": len(rendered),
        "slides_dir": str(slides_dir),
        "contact_sheet": str(qa_dir / "contact-sheet.png"),
        "caption_metrics": str(metrics_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a numbered social photo carousel")
    parser.add_argument("project", type=Path, help="Project directory containing project.json and generated/")
    args = parser.parse_args()
    print(json.dumps(render_project(args.project), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

