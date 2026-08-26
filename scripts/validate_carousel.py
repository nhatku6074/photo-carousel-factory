from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, UnidentifiedImageError


def _failure(code: str, message: str, file: str | None = None) -> dict:
    item = {"code": code, "message": message}
    if file is not None:
        item["file"] = file
    return item


def validate_delivery(project_dir: Path) -> dict:
    project_dir = Path(project_dir).resolve()
    config_path = project_dir / "project.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    slides = config.get("slides", [])
    expected_size = (int(config["canvas"]["width"]), int(config["canvas"]["height"]))
    safe_area = config["safe_area"]
    failures: list[dict] = []
    warnings: list[dict] = []
    files_checked = 0
    observed_dimensions: dict[str, list[int]] = {}

    if config.get("requires_product_reveal") and not any(slide.get("type") == "product-reveal" for slide in slides):
        failures.append(_failure("product_reveal", "a product-reveal slide is required but not configured"))

    output_names = [slide.get("output") for slide in slides]
    if len(output_names) != len(set(output_names)):
        failures.append(_failure("duplicate_output", "configured output filenames must be unique"))

    for slide in slides:
        base = project_dir / "generated" / slide["base"]
        output = project_dir / "slides" / slide["output"]
        if not base.is_file():
            failures.append(_failure("missing_source", "configured base image is missing", slide["base"]))
        elif base.stat().st_size == 0:
            failures.append(_failure("empty_source", "configured base image is empty", slide["base"]))

        if not output.is_file():
            failures.append(_failure("missing_output", "rendered slide is missing", slide["output"]))
            continue
        if output.stat().st_size == 0:
            failures.append(_failure("empty_output", "rendered slide is empty", slide["output"]))
            continue

        files_checked += 1
        try:
            with Image.open(output) as image:
                size = image.size
                image.verify()
        except (UnidentifiedImageError, OSError) as exc:
            failures.append(_failure("invalid_image", f"rendered slide is not a readable image: {exc}", slide["output"]))
            continue
        observed_dimensions[slide["output"]] = [size[0], size[1]]
        if size != expected_size:
            failures.append(
                _failure(
                    "dimensions",
                    f"expected {expected_size[0]}x{expected_size[1]}, found {size[0]}x{size[1]}",
                    slide["output"],
                )
            )

    metrics_path = project_dir / "qa" / "caption-metrics.json"
    if not metrics_path.is_file():
        warnings.append({"code": "caption_metrics", "message": "caption metrics are missing"})
    else:
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        by_file = {item.get("file"): item for item in metrics}
        for slide in slides:
            metric = by_file.get(slide["output"])
            if metric is None:
                failures.append(_failure("caption_metrics", "caption metrics missing for slide", slide["output"]))
                continue
            if metric["left"] < safe_area["left"] or metric["right"] > expected_size[0] - safe_area["right"]:
                failures.append(_failure("caption_safe_area", "caption exceeds horizontal safe area", slide["output"]))
            if metric["top"] < safe_area["top"] or metric["bottom"] > expected_size[1] - safe_area["bottom"]:
                failures.append(_failure("caption_safe_area", "caption exceeds vertical safe area", slide["output"]))

    report = {
        "status": "pass" if not failures else "fail",
        "project": config.get("name", project_dir.name),
        "expected_files": len(slides),
        "files_checked": files_checked,
        "expected_dimensions": [expected_size[0], expected_size[1]],
        "observed_dimensions": observed_dimensions,
        "failures": failures,
        "warnings": warnings,
    }
    qa_dir = project_dir / "qa"
    qa_dir.mkdir(parents=True, exist_ok=True)
    (qa_dir / "validation-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a rendered photo carousel delivery")
    parser.add_argument("project", type=Path, help="Project directory containing project.json")
    args = parser.parse_args()
    report = validate_delivery(args.project)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
