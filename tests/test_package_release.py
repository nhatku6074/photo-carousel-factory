from __future__ import annotations

import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "package_release.py"


def load_packager():
    if not SCRIPT.exists():
        raise AssertionError("package_release.py is not implemented")
    spec = importlib.util.spec_from_file_location("package_release", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("packager module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_fake_skill(root: Path) -> Path:
    skill = root / "photo-carousel-factory"
    (skill / "scripts" / "__pycache__").mkdir(parents=True)
    (skill / "examples" / "demo" / "generated").mkdir(parents=True)
    (skill / "examples" / "demo" / "slides").mkdir()
    (skill / "examples" / "demo" / "qa").mkdir()
    (skill / ".git").mkdir()
    (skill / "dist").mkdir()
    (skill / "SKILL.md").write_text("---\nname: photo-carousel-factory\ndescription: test\n---\n", encoding="utf-8")
    (skill / "LICENSE").write_text("MIT", encoding="utf-8")
    (skill / "scripts" / "tool.py").write_text("print('ok')\n", encoding="utf-8")
    (skill / "scripts" / "__pycache__" / "tool.pyc").write_bytes(b"cache")
    (skill / ".git" / "config").write_text("private", encoding="utf-8")
    (skill / ".env").write_text("API_KEY=secret", encoding="utf-8")
    (skill / "credentials.json").write_text('{"token":"secret"}', encoding="utf-8")
    (skill / "dist" / "old.zip").write_bytes(b"old")
    (skill / "examples" / "demo" / "generated" / "base.png").write_bytes(b"public-base")
    (skill / "examples" / "demo" / "slides" / "rendered.png").write_bytes(b"generated-output")
    (skill / "examples" / "demo" / "qa" / "report.json").write_text("{}", encoding="utf-8")
    return skill


class PackageReleaseTests(unittest.TestCase):
    def test_release_zip_has_single_skill_root(self) -> None:
        packager = load_packager()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill = build_fake_skill(root)
            archive = packager.package_skill(skill, "1.2.3", root / "release")
            with zipfile.ZipFile(archive) as bundle:
                roots = {name.split("/", 1)[0] for name in bundle.namelist() if name}
            self.assertEqual(roots, {"photo-carousel-factory"})

    def test_release_zip_excludes_private_and_generated_artifacts(self) -> None:
        packager = load_packager()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill = build_fake_skill(root)
            archive = packager.package_skill(skill, "1.2.3", root / "release")
            with zipfile.ZipFile(archive) as bundle:
                names = set(bundle.namelist())
            joined = "\n".join(sorted(names))
            self.assertNotIn(".git/", joined)
            self.assertNotIn("__pycache__", joined)
            self.assertNotIn(".env", joined)
            self.assertNotIn("credentials.json", joined)
            self.assertNotIn("dist/old.zip", joined)
            self.assertNotIn("examples/demo/slides/", joined)
            self.assertNotIn("examples/demo/qa/", joined)
            self.assertIn("photo-carousel-factory/examples/demo/generated/base.png", names)

    def test_release_zip_contains_entrypoint_license_and_script(self) -> None:
        packager = load_packager()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill = build_fake_skill(root)
            archive = packager.package_skill(skill, "1.2.3", root / "release")
            with zipfile.ZipFile(archive) as bundle:
                names = set(bundle.namelist())
            self.assertIn("photo-carousel-factory/SKILL.md", names)
            self.assertIn("photo-carousel-factory/LICENSE", names)
            self.assertIn("photo-carousel-factory/scripts/tool.py", names)


if __name__ == "__main__":
    unittest.main()
