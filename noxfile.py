import json
import tempfile
from typing import Any

import nox

PYPROECT = nox.project.load_toml()
PYTHON_VERSIONS = nox.project.python_versions(PYPROECT)
PYTHON_DEFAULT_VERSION = PYTHON_VERSIONS[-1]


def get_deps(pyproject: dict[str, Any], group: str) -> list[str]:
    """Get list of dependencies from pyproject.toml for a given group."""
    return pyproject["tool"]["nox"]["dependency-group"][group]


TEST_DEPENDENCIES = get_deps(PYPROECT, "test")
DOCS_DEPENDENCIES = get_deps(PYPROECT, "docs")


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Tests using local pypiserver only"""
    session.install(*TEST_DEPENDENCIES, ".")
    test_dir = session.posargs or ["tests"]
    session.run("pytest", "--cov=readme_credly_badges", "--cov-report=", *test_dir)
    session.notify("coverage")


@nox.session
def coverage(session: nox.Session) -> None:
    """Coverage analysis"""
    session.install("coverage[toml]")
    session.run("coverage", "report", "--show-missing", "--fail-under=70")
    session.run("coverage", "erase")


@nox.session(python=PYTHON_DEFAULT_VERSION)
def lint(session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


@nox.session(python=PYTHON_VERSIONS)
def develop(session):
    """Set up development environment and load .env inline after installing dependencies."""
    session.run("python", "-m", "pip", "install", "--upgrade", "pip")
    session.install(*TEST_DEPENDENCIES, "python-dotenv", ".")

    # Use a temporary file to get clean JSON output from subprocess
    with tempfile.NamedTemporaryFile(mode="r+", delete=False) as tf:
        json_path = tf.name

    # Dump the .env variables as JSON into the tempfile using an inline script
    session.run(
        "python",
        "-c",
        (
            "import json; "
            "from pathlib import Path; "
            "from dotenv import dotenv_values; "
            f"path = Path('.env'); "
            f"json.dump(dotenv_values(path) if path.exists() else {{}}, open('{json_path}', 'w'))"
        ),
        external=True,
    )

    # Read and inject into session.env
    with open(json_path) as f:
        session.env.update(json.load(f))

    session.log("Loaded .env into session.env")


@nox.session(python=PYTHON_DEFAULT_VERSION)
def build_changelog(session: nox.Session) -> None:
    session.install("towncrier", ".")
    session.run("towncrier", "build", "--version", session.posargs[0], "--yes")


@nox.session(python=PYTHON_DEFAULT_VERSION)
def bump_version(session):
    """Bump project version via update_version.py"""
    session.install("toml")

    if not session.posargs:
        session.error("Usage: nox -s bump -- <new_version>")

    new_version = session.posargs[0]

    session.run("python", "scripts/update_version.py", new_version)


@nox.session(name="changelog")
def changelog(session):
    session.install(*DOCS_DEPENDENCIES, ".")
    session.run("towncrier", "build", "--version", session.posargs[0], "--yes")
