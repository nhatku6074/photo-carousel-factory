from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_carousel.py"


def load_validator():
    if not SCRIPT.exists():
        raise AssertionError("validate_carousel.py is not implemented")
    spec = importlib.util.spec_from_file_location("validate_carousel", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("validator module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_project(root: Path) -> dict:
    config = {
        "name": "validation-test",
        "canvas": {"width": 360, "height": 640},
        "safe_area": {"left": 20, "right": 20, "top": 30, "bottom": 50},
        "font": None,
        "requires_product_reveal": True,
        "slides": [
            {
                "id": "01-hook",
                "type": "hook",
                "base": "01-base.png",
                "output": "01-hook.png",
                "copy": "A useful hook",
                "line_breaks": ["A useful hook"],
                "text_center_y": 200,
                "font_start": 40,
            },
            {
                "id": "02-product",
                "type": "product-reveal",
                "base": "02-base.png",
                "output": "02-product.png",
                "copy": "A simple reveal",
                "line_breaks": ["A simple reveal"],
                "text_center_y": 180,
                "font_start": 40,
            },
        ],
    }
    (root / "generated").mkdir()
    (root / "slides").mkdir()
    (root / "qa").mkdir()
    (root / "project.json").write_text(json.dumps(config), encoding="utf-8")
    for slide in config["slides"]:
        Image.new("RGB", (360, 640), "#3b536d").save(root / "generated" / slide["base"])
        Image.new("RGB", (360, 640), "#3b536d").save(root / "slides" / slide["output"])
    metrics = [
        {"file": "01-hook.png", "left": 30, "right": 330, "top": 100, "bottom": 250},
        {"file": "02-product.png", "left": 30, "right": 330, "top": 100, "bottom": 250},
    ]
    (root / "qa" / "caption-metrics.json").write_text(json.dumps(metrics), encoding="utf-8")
    return config


def failure_codes(report: dict) -> set[str]:
    return {item["code"] for item in report["failures"]}


class ValidateCarouselTests(unittest.TestCase):
    def test_validate_delivery_passes_for_complete_project(self) -> None:
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            build_project(project)
            report = validator.validate_delivery(project)
            self.assertEqual(report["status"], "pass")
            self.assertEqual(report["files_checked"], 2)
            self.assertEqual(report["failures"], [])

    def test_validate_delivery_rejects_wrong_dimensions(self) -> None:
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            build_project(project)
            Image.new("RGB", (300, 600), "#111111").save(project / "slides" / "01-hook.png")
            report = validator.validate_delivery(project)
            self.assertEqual(report["status"], "fail")
            self.assertIn("dimensions", failure_codes(report))

    def test_validate_delivery_rejects_missing_product_reveal(self) -> None:
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            config = build_project(project)
            config["slides"][1]["type"] = "point"
            (project / "project.json").write_text(json.dumps(config), encoding="utf-8")
            report = validator.validate_delivery(project)
            self.assertEqual(report["status"], "fail")
            self.assertIn("product_reveal", failure_codes(report))

    def test_validate_delivery_rejects_empty_output(self) -> None:
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            build_project(project)
            (project / "slides" / "02-product.png").write_bytes(b"")
            report = validator.validate_delivery(project)
            self.assertEqual(report["status"], "fail")
            self.assertIn("empty_output", failure_codes(report))


if __name__ == "__main__":
    unittest.main()
