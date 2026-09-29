"""Check shared runtime pins without contacting a package registry."""

from pathlib import Path
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def check_dependency_sync(root: Path) -> list[str]:
    project = tomllib.loads((root / "pyproject.toml").read_text())
    declared = project["project"]["dependencies"]
    direct_names = [
        re.split(r"[<>=!~\[; ]", value, maxsplit=1)[0].lower().replace("_", "-") for value in declared
    ]
    locks = {
        filename: tomllib.loads((root / filename).read_text())["package"]
        for filename in ("uv.lock", "pdm.lock", "poetry.lock")
    }
    pins = {}
    for line in (root / "requirements.txt").read_text().splitlines():
        match = re.match(r"([\w.-]+)==([^\s;]+)", line)
        if match:
            pins[match[1].lower().replace("_", "-")] = match[2]
    errors = []
    for name in direct_names:
        versions = {
            filename: {
                package["version"]
                for package in packages
                if package["name"].lower().replace("_", "-") == name
            }
            for filename, packages in locks.items()
        }
        expected = versions["uv.lock"]
        for filename, actual in versions.items():
            if not expected or actual != expected:
                errors.append(f"{name}: {filename}={sorted(actual)}, uv.lock={sorted(expected)}")
        if pins.get(name) not in expected:
            errors.append(f"{name}: requirements.txt={pins.get(name)}, uv.lock={sorted(expected)}")
    auto = project.get("project", {}).get("gscore_auto_update_dep", [])
    for requirement in auto:
        if requirement not in declared:
            errors.append(f"gscore_auto_update_dep does not match project dependencies: {requirement}")
    return errors


if __name__ == "__main__":
    problems = check_dependency_sync(ROOT)
    if problems:
        sys.exit("\n".join(problems))
    sys.stdout.write("Runtime dependency pins are consistent across all four files.\n")
