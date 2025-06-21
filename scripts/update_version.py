"""Update the version in pyproject.toml using tomli + tomli-w (TOML v1.0 compliant)"""

import logging
import sys

import tomli
import tomli_w

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

ARG_COUNT = 2
PYPROJECT = "pyproject.toml"


def main():
    if len(sys.argv) != ARG_COUNT:
        logger.error("Usage: python update_version.py <version>")
        sys.exit(1)

    new_version = sys.argv[1]

    try:
        with open(PYPROJECT, "rb") as f:
            data = tomli.load(f)
    except FileNotFoundError:
        logger.error("pyproject.toml not found.")
        sys.exit(1)

    if "project" not in data or "version" not in data["project"]:
        logger.error("[project].version not found in pyproject.toml")
        sys.exit(1)

    data["project"]["version"] = new_version

    with open(PYPROJECT, "w", encoding="utf-8") as f:
        f.write(tomli_w.dumps(data))

    logger.info(f"Updated version to {new_version}")


if __name__ == "__main__":
    main()
