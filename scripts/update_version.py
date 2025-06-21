"""Update the version in pyproject.toml"""

import logging
import sys

import toml

# Configure logger
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

ARG_COUNT = 2


def main():
    if len(sys.argv) != ARG_COUNT:
        logger.error("Usage: python update_version.py <version>")
        sys.exit(1)

    new_version = sys.argv[1]

    try:
        with open("pyproject.toml", encoding="utf-8") as f:
            data = toml.load(f)
    except FileNotFoundError:
        logger.error("pyproject.toml not found.")
        sys.exit(1)

    if "project" not in data or "version" not in data["project"]:
        logger.error("project.version not found in pyproject.toml")
        sys.exit(1)

    data["project"]["version"] = new_version

    with open("pyproject.toml", "w", encoding="utf-8") as f:
        toml.dump(data, f)

    logger.info(f"Updated version to {new_version}")


if __name__ == "__main__":
    main()
