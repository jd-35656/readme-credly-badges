import os

START_COMMENT = "<!-- START CREDLY BADGES -->"
END_COMMENT = "<!-- END CREDLY BADGES -->"

CREDLY_USERNAME = os.getenv("CREDLY_USERNAME")
BADGE_SIZE = os.getenv("BADGE_SIZE", "150x150")
BADGE_SORT_BY = os.getenv("BADGE_SORT_BY", "issued")

GITHUB_API_URL = os.getenv("GITHUB_API_URL", "https://api.github.com")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")
README_FILE = os.getenv("README_FILE", "README.md")

COMMIT_MESSAGE = os.getenv("COMMIT_MESSAGE", "Update README files with Credly badges.")
