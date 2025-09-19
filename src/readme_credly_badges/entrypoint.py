"""Entry Point for the application."""

import logging

from readme_credly_badges.adapter import Credly, GithubRepo
from readme_credly_badges.settings import (
    BADGE_SIZE,
    COMMIT_MESSAGE,
    CREDLY_USERNAME,
    GITHUB_API_URL,
    GITHUB_BRANCH,
    GITHUB_REPO,
    GITHUB_TOKEN,
    README_FILE,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def generate_new_readme_content(badges: list[dict[str, str]], old_readme_content: str) -> str:
    """
    Replace the Credly badges section in the old README content.
    Raises ValueError if the badge comment markers are not found.
    """
    start_comment = "<!-- START CREDLY BADGES -->"
    end_comment = "<!-- END CREDLY BADGES -->"

    if start_comment not in old_readme_content or end_comment not in old_readme_content:
        logger.error("Credly badge section markers not found in README.")
        raise ValueError("Credly badge section markers not found in README.")

    markdown_badges = "\n".join(
        f"[![{badge['name']}]({badge['image_url']})]({badge['url']})" for badge in badges
    ).replace(
        "https://images.credly.com/images/",
        f"https://images.credly.com/size/{BADGE_SIZE}/images/",
    )

    before = old_readme_content.split(start_comment)[0]
    after = old_readme_content.split(end_comment)[1]

    return f"{before}{start_comment}\n{markdown_badges}\n{end_comment}{after}"


def main() -> None:
    "Main function to update the README with Credly badges."
    logger.info("Starting the README update process with Credly badges.")
    if not (CREDLY_USERNAME and GITHUB_TOKEN and GITHUB_REPO):
        logger.error("Environment variables CREDLY_USERNAME, GITHUB_TOKEN, and GITHUB_REPO must be set.")
        raise ValueError("Environment variables CREDLY_USERNAME, GITHUB_TOKEN, and GITHUB_REPO must be set.")

    credly = Credly(username=CREDLY_USERNAME)
    github_repo = GithubRepo(
        commit_message=COMMIT_MESSAGE,
        gh_api_url=GITHUB_API_URL,
        gh_token=GITHUB_TOKEN,
        repository=GITHUB_REPO,
        branch=GITHUB_BRANCH,
        readme_filename=README_FILE,
    )
    badges = credly.fetch_badges()
    old_readme_content = github_repo.get_readme()
    new_readme_content = generate_new_readme_content(badges=badges, old_readme_content=old_readme_content)

    if new_readme_content.strip() != old_readme_content.strip():
        github_repo.save_readme(new_content=new_readme_content)
        logger.info("README updated with new Credly badges.")
    else:
        logger.info("README is already up to date.")


if __name__ == "__main__":
    main()
