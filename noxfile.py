# ----------------------------
# Noxfile
# ----------------------------
from pathlib import Path
from typing import Any

import nox  # type: ignore[import-untyped]

# ----------------------------
# Constants / Configuration
# ----------------------------
PYPROJECT: dict[str, Any] = nox.project.load_toml()
PYTHON_VERSIONS: list[str] = nox.project.python_versions(PYPROJECT)
DEFAULT_PYTHON: str = PYTHON_VERSIONS[-1]

# ----------------------------
# Settings
# ----------------------------
nox.options.sessions = ["tests", "check"]
nox.options.reuse_existing_virtualenvs = True


# ----------------------------
# Helper Functions
# ----------------------------
def get_opt_deps(
    group: str,
    pyproject: dict[str, Any] = PYPROJECT,
) -> list[str]:
    """Fetch dependencies for a given group from pyproject.toml."""
    if "optional-dependencies" not in pyproject["project"]:
        raise KeyError("Missing 'optional-dependencies' in pyproject.toml")
    opt_deps = pyproject["project"]["optional-dependencies"]
    if group not in opt_deps:
        raise KeyError(f"Missing group '{group}' in 'optional-dependencies' in pyproject.toml")
    return opt_deps[group]


def load_dotenv(path: Path = Path(".env")) -> dict[str, str]:
    """Load simple .env file (KEY=VALUE) into a dict"""
    if not str(path).endswith(".env"):
        raise ValueError(f"Provided path must end with '.env': {path}")

    env: dict[str, str] = {}
    if not path.exists():
        return env

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


# ----------------------------
# Dependency constants
# ----------------------------
TEST_DEPS = get_opt_deps("test")
TYPE_DEPS = get_opt_deps("type")


# ----------------------------
# Dependency constants
# ----------------------------
@nox.session(python=PYTHON_VERSIONS)
def develop(session):
    session.env.update(load_dotenv())
    session.run("python", "-m", "pip", "install", "--upgrade", "pip")
    session.install("-e", ".", *TEST_DEPS, *TYPE_DEPS, "nox")


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    session.install("-e", ".", *TEST_DEPS)
    session.run("pytest", *session.posargs, external=True)


@nox.session
def lint(session: nox.Session) -> None:
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", external=True)


@nox.session
def typecheck(session: nox.Session) -> None:
    session.install("-e", ".", "mypy", *TEST_DEPS, *TYPE_DEPS)
    session.run("mypy", "--install-types", "--non-interactive", *session.posargs, external=True)


@nox.session(python=DEFAULT_PYTHON)
def check(session: nox.Session) -> None:
    session.notify("lint")
    session.notify("typecheck")


@nox.session(python=DEFAULT_PYTHON)
def changelog(session: nox.Session) -> None:
    session.install("towncrier")
    session.run("towncrier", "build", "--version", session.posargs[0], "--yes")


@nox.session(python=DEFAULT_PYTHON)
def bump2version(session):
    """Bump project version via update_version.py"""
    session.install("tomlkit")

    if not session.posargs:
        session.error("Usage: nox -s bump2version -- <new_version>")

    new_version = session.posargs[0]

    session.run("python", "scripts/bump2version.py", new_version)
