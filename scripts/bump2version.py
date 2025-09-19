from pathlib import Path

import tomlkit  # type: ignore[import-untyped]


def update_version_in_pyproject(pyproject_path: Path, new_version: str) -> None:
    """
    Update the [project].version field in the pyproject.toml file.

    Args:
        pyproject_path (Path): Path to the pyproject.toml file.
        new_version (str): New version string to set.
    """
    # Read the file
    content = pyproject_path.read_text(encoding="utf-8")

    # Parse TOML
    data = tomlkit.parse(content)

    # Check that the version field exists
    if "project" not in data or "version" not in data["project"]:
        raise KeyError("[project].version not found in pyproject.toml")

    # Update version
    data["project"]["version"] = new_version

    # Write back to file
    pyproject_path.write_text(tomlkit.dumps(data), encoding="utf-8")


if __name__ == "__main__":
    import sys

    EXPECTED_ARG_COUNT = 2

    if len(sys.argv) != EXPECTED_ARG_COUNT:
        sys.exit(1)

    new_ver = sys.argv[1]
    pyproject_file = Path("pyproject.toml")

    try:
        update_version_in_pyproject(pyproject_file, new_ver)
    except Exception:
        sys.exit(1)
