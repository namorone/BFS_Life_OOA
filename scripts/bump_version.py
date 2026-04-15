#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "VERSION"
FRONTEND_PACKAGE_JSON = ROOT / "apps/frontend/package.json"
FRONTEND_PACKAGE_LOCK = ROOT / "apps/frontend/package-lock.json"
BACKEND_PYPROJECT = ROOT / "apps/backend/pyproject.toml"


def parse_version(raw: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", raw.strip())
    if not match:
        raise ValueError(f"Invalid version format: {raw!r}. Expected MAJOR.MINOR.PATCH")
    return tuple(int(part) for part in match.groups())


def bump_version(current: str, bump_type: str) -> str:
    major, minor, patch = parse_version(current)
    if bump_type == "patch":
        patch += 1
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError(f"Unknown bump type: {bump_type}")
    return f"{major}.{minor}.{patch}"


def update_version_file(new_version: str) -> None:
    VERSION_FILE.write_text(f"{new_version}\n", encoding="utf-8")


def update_frontend_json(path: Path, new_version: str) -> None:
    content = json.loads(path.read_text(encoding="utf-8"))
    content["version"] = new_version
    path.write_text(f"{json.dumps(content, indent=2)}\n", encoding="utf-8")


def update_backend_pyproject(new_version: str) -> None:
    content = BACKEND_PYPROJECT.read_text(encoding="utf-8")
    updated = re.sub(
        r'(?m)^version\s*=\s*"[0-9]+\.[0-9]+\.[0-9]+"$',
        f'version = "{new_version}"',
        content,
        count=1,
    )
    if updated == content:
        raise RuntimeError("Failed to update backend version in pyproject.toml")
    BACKEND_PYPROJECT.write_text(updated, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bump SemVer version across VERSION, frontend and backend files.",
    )
    parser.add_argument(
        "bump_type",
        choices=["patch", "minor", "major"],
        help="Which SemVer part to increment.",
    )
    args = parser.parse_args()

    current_version = VERSION_FILE.read_text(encoding="utf-8").strip()
    new_version = bump_version(current_version, args.bump_type)

    update_version_file(new_version)
    update_frontend_json(FRONTEND_PACKAGE_JSON, new_version)
    update_frontend_json(FRONTEND_PACKAGE_LOCK, new_version)
    update_backend_pyproject(new_version)

    print(f"Version bumped: {current_version} -> {new_version}")
    print(f"Suggested tag: v{new_version}")


if __name__ == "__main__":
    main()
