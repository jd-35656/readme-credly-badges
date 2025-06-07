"Extract Credly badges from a user's profile page using Playwright." ""

import logging
import re
from typing import Dict, List

from playwright.sync_api import Page, sync_playwright

from src.exceptions import (
    BadgeExtractionError,
    BadgeNotFoundError,
    PageLoadError,
    PageTimeoutError,
    ReadmeCredlyError,
)

logger = logging.getLogger(__name__)


class Credly:
    "Class to handle Credly badge extraction for a user profile."

    def __init__(self, username: str, timeout: int = 60000) -> None:
        self.username = username
        self.timeout = timeout
        self.url = f"https://www.credly.com/users/{self.username}"

    def fetch_badges(self) -> List[Dict[str, str]]:
        "Load the Credly page for the user."

        badges = []
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                response = page.goto(
                    self.url,
                    wait_until="domcontentloaded",
                    timeout=self.timeout,
                )

                if not response or response.status != 200:
                    raise PageLoadError("Failed to load the page.")

                # Handle cookie popup
                self._handle_cookie_popup(page)

                count = self._get_badge_count(page)

                for i in range(1, count + 1):
                    self._expand_all_badges(page)
                    badge_info = self._extract_nth_badge_info(page, i)

                    badges.append(badge_info)
            except ReadmeCredlyError as e:
                logger.error(f"Error fetching badges: {e}")
                raise e
            finally:
                # Close the browser
                browser.close()

            return badges

    def _handle_cookie_popup(self, page: Page) -> None:
        "Handle cookie popup if it appears"
        try:
            selector = 'button:has-text("Accept")'
            page.wait_for_selector(selector, timeout=self.timeout)
            page.click(selector)
        except TimeoutError:
            logger.info("No cookie popup to accept.")

    def _get_badge_count(self, page: Page) -> int:
        "Get the total number of badges displayed on the page."
        try:
            selector = (
                "div.Typographystyles__Container-fredly__sc-1jldzrm-0:nth-child(1)"
            )
            page.wait_for_selector(
                selector,
                timeout=self.timeout,
            )
            badge_count_text = page.query_selector(selector).text_content()

            match = re.search(r"\((\d+)\)", badge_count_text.strip())
            if not match:
                raise BadgeNotFoundError("Badge count not found in text.")

            count = int(match.group(1))
            if count <= 0:
                raise BadgeNotFoundError("No badges found for this user.")

            return count
        except TimeoutError as e:
            raise PageTimeoutError("Timeout while getting badge count.") from e

    def _expand_all_badges(self, page: Page) -> None:
        try:
            selector = "button.Buttonstyles__StyledButton-fredly__sc-k2a0sj-4"
            page.wait_for_selector(
                selector,
                timeout=self.timeout,
            )
            page.click(selector)
        except TimeoutError as e:
            raise PageTimeoutError(
                "Timeout while waiting for 'expand' button to load."
            ) from e

    def _extract_nth_badge_info(self, page: Page, n: int) -> Dict[str, str]:
        """Extract nth badge information from the page."""
        try:
            selector = f"div.settings__skills-profile__edit-skills-profile__badge-list__list-item:nth-child({n})"
            page.wait_for_selector(selector, timeout=self.timeout)
            badge_element = page.query_selector(selector)

            if not badge_element:
                raise BadgeNotFoundError(f"Badge element {n} not found on the page.")

            title_selector = "div.settings__skills-profile__edit-skills-profile__badge-card__organization-name-two-lines"
            img_selector = "img.settings__skills-profile__edit-skills-profile__badge-card__badge-image"

            title_element = badge_element.query_selector(title_selector)
            img_element = badge_element.query_selector(img_selector)

            title = title_element.text_content().strip()
            img_url = img_element.get_attribute("src").strip()

            # Click badge
            old_url = page.url
            badge_element.click()

            # Wait for badge detail URL
            page.wait_for_function(
                """(oldUrl) => window.location.href !== oldUrl && window.location.href.includes('/badges/')""",
                arg=old_url,
                timeout=self.timeout,
            )
            badge_url = page.url.strip()

            # Go back to profile
            page.go_back()
            page.wait_for_function(
                f"""() => window.location.href.includes('/users/{self.username}')""",
                timeout=self.timeout,
            )

            if not all([title, img_url, badge_url]):
                raise BadgeExtractionError(
                    f"Badge {n} information could not be extracted."
                )

            return {
                "url": badge_url,
                "title": title,
                "image": img_url,
            }

        except TimeoutError as e:
            raise PageTimeoutError(
                f"Timeout while waiting for badge {n} to load."
            ) from e
