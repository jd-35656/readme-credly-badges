import os

START_COMMENT = "<!-- START CREDLY BADGES -->"
END_COMMENT = "<!-- END CREDLY BADGES -->"

CREDLY_USERNAME = os.getenv("INPUT_CREDLY_USERNAME")
BADGE_SIZE = os.getenv("INPUT_BADGE_SIZE", "150x150")

GITHUB_API_URL = os.getenv("INPUT_GITHUB_API_URL", "https://api.github.com")
GITHUB_TOKEN = os.getenv("INPUT_GITHUB_TOKEN")
GITHUB_REPO = os.getenv("INPUT_GITHUB_REPO")
GITHUB_BRANCH = os.getenv("INPUT_GITHUB_BRANCH", "main")
README_FILE = os.getenv("INPUT_README_FILE", "README.md")

COMMIT_MESSAGE = os.getenv(
    "INPUT_COMMIT_MESSAGE", "Update README files with Credly badges."
)
