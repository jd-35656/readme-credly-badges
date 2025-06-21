"GitHub management module"

import base64
import logging

from github import Github, GithubException, UnknownObjectException

logger = logging.getLogger(__name__)


class GithubRepo:
    def __init__(
        self,
        commit_message: str,
        gh_api_url: str,
        gh_token: str,
        repository: str,
        branch: str,
        readme_filename: str,
    ):
        """Initialize the GitHub repository object."""
        self.commit_message = commit_message
        self.repository = repository
        self.branch = branch
        self.readme_filename = readme_filename

        try:
            logger.info(f"Connecting to GitHub repository {repository} on branch {branch} using API URL {gh_api_url}")
            gh = Github(
                base_url=gh_api_url,
                login_or_token=gh_token,
            )
            logger.info("Authentication successful.")

            self.repo = gh.get_repo(repository)
            logger.info(f"Repository {repository} accessed successfully.")
        except GithubException as e:
            logger.error(f"Failed to access repository {repository}: {e}")
            raise RuntimeError("Authentication failed.") from e

    def get_readme(self) -> str:
        """Fetch the specified README file's content."""
        try:
            logger.info(f"Fetching {self.readme_filename} from branch {self.branch} of repository {self.repository}")
            file_content = self.repo.get_contents(self.readme_filename, ref=self.branch)

            if isinstance(file_content, list):
                raise ValueError(f"{self.readme_filename} is a directory, expected a file.")

            return base64.b64decode(file_content.content).decode("utf-8")

        except UnknownObjectException as e:
            logger.error(f"Failed to find {self.readme_filename} in repository {self.repository}: {e}")
            raise FileNotFoundError(f"{self.readme_filename} not found in the repository.") from e

    def save_readme(self, new_content: str):
        """Update the specified README file with new content."""
        try:
            logger.info(f"Updating {self.readme_filename} in branch {self.branch} of repository {self.repository}")
            file_content = self.repo.get_contents(self.readme_filename, ref=self.branch)

            # Defensive check in case a list is returned
            if isinstance(file_content, list):
                raise ValueError(f"{self.readme_filename} is a directory, expected a single file.")

            self.repo.update_file(
                path=self.readme_filename,
                message=self.commit_message,
                content=new_content,
                sha=file_content.sha,
            )
            logger.info(f"{self.readme_filename} updated successfully in repository {self.repository}.")
        except UnknownObjectException as e:
            logger.error(f"Failed to find {self.readme_filename} in repository {self.repository}: {e}")
            raise FileNotFoundError(f"{self.readme_filename} not found in the repository.") from e
