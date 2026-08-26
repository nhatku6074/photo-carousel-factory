from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_carousel.py"


def load_renderer():
    if not SCRIPT.exists():
        raise AssertionError("render_carousel.py is not implemented")
    spec = importlib.util.spec_from_file_location("render_carousel", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("renderer module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample_config() -> dict:
    return {
        "name": "test-project",
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
                "copy": "Three habits stealing focus",
                "line_breaks": ["Three habits", "stealing focus"],
                "text_center_y": 250,
                "font_start": 42,
            },
            {
                "id": "02-product",
                "type": "product-reveal",
                "base": "02-base.png",
                "output": "02-product.png",
                "copy": "Keep the routine simple",
                "line_breaks": ["Keep the routine", "simple"],
                "text_center_y": 180,
                "font_start": 42,
            },
        ],
    }


class RenderCarouselTests(unittest.TestCase):
    def test_validate_config_rejects_duplicate_outputs(self) -> None:
        renderer = load_renderer()
        config = sample_config()
        config["slides"][1]["output"] = config["slides"][0]["output"]
        with self.assertRaisesRegex(ValueError, "unique"):
            renderer.validate_config(config)

    def test_fit_caption_respects_safe_width(self) -> None:
        renderer = load_renderer()
        canvas = Image.new("RGB", (360, 640), "#42526e")
        draw = ImageDraw.Draw(canvas)
        font, _, boxes = renderer.fit_caption(
            draw,
            ["A deliberately long caption line"],
            start_size=52,
            max_width=300,
            max_height=120,
            font_path=renderer.find_font(),
        )
        self.assertGreaterEqual(font.size, 12)
        self.assertLessEqual(max(box[2] - box[0] for box in boxes), 300)

    def test_render_project_creates_ordered_slides_contact_sheet_and_metrics(self) -> None:
        renderer = load_renderer()
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            generated = project / "generated"
            generated.mkdir()
            config = sample_config()
            (project / "project.json").write_text(json.dumps(config), encoding="utf-8")
            Image.new("RGB", (400, 700), "#375a7f").save(generated / "01-base.png")
            Image.new("RGB", (400, 700), "#6b8e23").save(generated / "02-base.png")

            report = renderer.render_project(project)

            outputs = sorted((project / "slides").glob("*.png"))
            self.assertEqual([path.name for path in outputs], ["01-hook.png", "02-product.png"])
            self.assertTrue((project / "qa" / "contact-sheet.png").exists())
            metrics_path = project / "qa" / "caption-metrics.json"
            self.assertTrue(metrics_path.exists())
            metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
            self.assertEqual(len(metrics), 2)
            self.assertEqual(report["rendered"], 2)
            with Image.open(outputs[0]) as rendered_image:
                self.assertEqual(rendered_image.size, (360, 640))


if __name__ == "__main__":
    unittest.main()
