"Credly Module"

import logging
from typing import Dict, List

import requests

logger = logging.getLogger(__name__)


class Credly:
    """Class to handle Credly badge extraction for a user profile."""

    def __init__(self, username: str, timeout: int = 60) -> None:
        self.username = username
        self.timeout = timeout
        self.url = f"https://www.credly.com/users/{self.username}/badges.json"

    def fetch_badges(self) -> List[Dict[str, str]]:
        """Fetch badges for the user from the Credly .json endpoint, ensuring all required fields are present."""
        try:
            logger.info(f"Fetching badges for {self.username} from {self.url}")
            response = requests.get(self.url, timeout=self.timeout)
            logger.info(f"HTTP response status code: {response.status_code}")
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch badges for {self.username}: {e}")
            raise ConnectionError(f"Failed to fetch badges for {self.username}") from e

        badges = []
        data = response.json().get("data", [])

        for badge in data:
            badge_id = badge.get("id")
            badge_template = badge.get("badge_template", {})
            name = badge_template.get("name")
            image_url = badge_template.get("image_url")

            # Ensure none of the fields are empty or missing
            if not (badge_id and name and image_url):
                logger.warning(
                    f"Skipping incomplete badge: id={badge_id}, name={name}, image_url={image_url}"
                )
                continue

            logger.info(
                f"Found badge: id={badge_id}, name={name}, image_url={image_url}"
            )
            badges.append(
                {
                    "name": name.strip(),
                    "url": f"https://www.credly.com/badges/{badge_id.strip()}",
                    "image_url": image_url.strip(),
                }
            )

        return badges
