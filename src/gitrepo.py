"GitHub management module"

import base64

from github import Github, GithubException, UnknownObjectException


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
            gh = Github(
                base_url=gh_api_url,
                login_or_token=gh_token,
            )
            self.repo = gh.get_repo(repository)
        except GithubException as e:
            raise RuntimeError("Authentication failed.") from e

    def get_readme(self) -> str:
        """Fetch the specified README file's content."""
        try:
            file_content = self.repo.get_contents(self.readme_filename, ref=self.branch)

            if isinstance(file_content, list):
                raise ValueError(
                    f"{self.readme_filename} is a directory, expected a file."
                )

            return base64.b64decode(file_content.content).decode("utf-8")

        except UnknownObjectException as e:
            raise FileNotFoundError(
                f"{self.readme_filename} not found in the repository."
            ) from e

    def save_readme(self, new_content: str):
        """Update the specified README file with new content."""
        try:
            file_content = self.repo.get_contents(self.readme_filename, ref=self.branch)

            # Defensive check in case a list is returned
            if isinstance(file_content, list):
                raise ValueError(
                    f"{self.readme_filename} is a directory, expected a single file."
                )

            self.repo.update_file(
                path=self.readme_filename,
                message=self.commit_message,
                content=new_content,
                sha=file_content.sha,
            )
        except UnknownObjectException as e:
            raise FileNotFoundError(
                f"{self.readme_filename} not found in the repository."
            ) from e
