from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path


EXCLUDED_DIRECTORIES = {
    ".git",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "dist",
    "node_modules",
    "venv",
}

EXCLUDED_FILENAMES = {
    ".env",
    "credentials.json",
    "secrets.json",
}

EXCLUDED_SUFFIXES = {
    ".key",
    ".pem",
    ".pyc",
    ".pyo",
}


def should_include(relative: Path) -> bool:
    if any(part in EXCLUDED_DIRECTORIES for part in relative.parts):
        return False
    if relative.parts and relative.parts[0] == "examples" and any(part in {"slides", "qa"} for part in relative.parts):
        return False
    if relative.name in EXCLUDED_FILENAMES or relative.name.startswith(".env."):
        return False
    if relative.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    return True


def package_skill(skill_dir: Path, version: str, output_dir: Path | None = None) -> Path:
    skill_dir = Path(skill_dir).resolve()
    if not (skill_dir / "SKILL.md").is_file():
        raise FileNotFoundError(f"missing Skill entrypoint: {skill_dir / 'SKILL.md'}")
    if not (skill_dir / "LICENSE").is_file():
        raise FileNotFoundError(f"missing license: {skill_dir / 'LICENSE'}")

    output_dir = Path(output_dir).resolve() if output_dir else skill_dir / "dist"
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{skill_dir.name}-v{version}.zip"
    included: list[str] = []

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for file in sorted(path for path in skill_dir.rglob("*") if path.is_file()):
            relative = file.relative_to(skill_dir)
            if not should_include(relative):
                continue
            archive_name = Path(skill_dir.name) / relative
            bundle.write(file, archive_name.as_posix())
            included.append(archive_name.as_posix())

    if not included:
        raise RuntimeError("release archive would be empty")
    return archive


def main() -> int:
    parser = argparse.ArgumentParser(description="Package a validated Codex Skill release ZIP")
    parser.add_argument("skill", type=Path, help="Skill root containing SKILL.md")
    parser.add_argument("--version", default="1.0.0", help="Release version without a leading v")
    parser.add_argument("--output", type=Path, default=None, help="Optional output directory")
    args = parser.parse_args()
    archive = package_skill(args.skill, args.version, args.output)
    print(json.dumps({"status": "pass", "archive": str(archive)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
