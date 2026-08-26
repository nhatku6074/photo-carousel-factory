from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillPackageTests(unittest.TestCase):
    def test_public_entrypoints_and_docs_exist(self) -> None:
        required = [
            "SKILL.md",
            "README.md",
            "README.zh-CN.md",
            "LICENSE",
            "PUBLICATION.md",
            "agents/openai.yaml",
            "assets/demo-contact-sheet.png",
        ]
        self.assertEqual([item for item in required if not (ROOT / item).is_file()], [])

    def test_skill_frontmatter_is_finished_and_discoverable(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: photo-carousel-factory\n"))
        self.assertIn("description:", text)
        self.assertNotIn("TODO", text)

    def test_public_text_does_not_contain_private_product_or_local_path(self) -> None:
        text_files = [
            ROOT / "SKILL.md",
            ROOT / "README.md",
            ROOT / "README.zh-CN.md",
            ROOT / "PUBLICATION.md",
            *sorted((ROOT / "references").glob("*.md")),
        ]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in text_files)
        self.assertNotIn("C:\\Users\\Cheng", combined)
        self.assertNotIn("PIXVERSE_API_KEY", combined)
        self.assertNotIn("ark-", combined)


if __name__ == "__main__":
    unittest.main()
