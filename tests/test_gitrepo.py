"Test cases for the GithubRepo class in readme_credly_badges.adapter.readme_credly_badges.adapter/github_repo.py"

import base64
from unittest.mock import MagicMock, patch

import pytest
from github.GithubException import GithubException, UnknownObjectException

from readme_credly_badges.adapter import GithubRepo


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def mock_github(mock_repo):
    with patch("readme_credly_badges.adapter.github_repo.Github") as MockGithub:
        MockGithub.return_value.get_repo.return_value = mock_repo
        yield MockGithub, mock_repo


@pytest.fixture
def github_repo(mock_github):
    MockGithub, mock_repo = mock_github
    repo = GithubRepo(
        commit_message="commit",
        repository="test/repo",
        gh_token="token",
        gh_api_url="https://api.github.com",
        branch="main",  # Pass branch explicitly
        readme_filename="README.md",  # Pass README filename explicitly
    )
    return repo, mock_repo


def test_initialization_success(mock_github):
    MockGithub, mock_repo = mock_github

    repo = GithubRepo(
        commit_message="Init test",
        repository="user/repo",
        gh_token="fake-token",
        gh_api_url="https://api.github.com",
        branch="develop",
        readme_filename="README.md",
    )

    assert repo.repo == mock_repo
    assert repo.commit_message == "Init test"


def test_initialization_auth_failure():
    with patch("readme_credly_badges.adapter.github_repo.Github") as MockGithub:
        MockGithub.return_value.get_repo.side_effect = GithubException(401, {}, {})
        with pytest.raises(RuntimeError):
            GithubRepo(
                commit_message="fail",
                repository="user/repo",
                gh_token="bad-token",
                gh_api_url="https://api.github.com",
                branch="main",
                readme_filename="README.md",
            )


def test_get_readme_success(github_repo):
    repo, mock_repo = github_repo
    content_str = "Hello World!"
    encoded_content = base64.b64encode(content_str.encode("utf-8")).decode("utf-8")
    mock_file = MagicMock()
    mock_file.content = encoded_content
    mock_repo.get_contents.return_value = mock_file

    result = repo.get_readme()
    assert result == content_str
    mock_repo.get_contents.assert_called_once_with(repo.readme_filename, ref=repo.branch)


def test_get_readme_file_not_found(github_repo):
    repo, mock_repo = github_repo
    mock_repo.get_contents.side_effect = UnknownObjectException(404, {}, {})

    with pytest.raises(FileNotFoundError):
        repo.get_readme()
    mock_repo.get_contents.assert_called_once_with(repo.readme_filename, ref=repo.branch)


def test_get_readme_when_readme_is_directory(github_repo):
    repo, mock_repo = github_repo
    mock_repo.get_contents.return_value = [MagicMock(), MagicMock()]

    with pytest.raises(ValueError) as exc_info:
        repo.get_readme()

    assert f"{repo.readme_filename} is a directory" in str(exc_info.value)
    mock_repo.get_contents.assert_called_once_with(repo.readme_filename, ref=repo.branch)


def test_save_readme_success(github_repo):
    repo, mock_repo = github_repo
    mock_file = MagicMock()
    mock_file.sha = "fake-sha"
    mock_repo.get_contents.return_value = mock_file

    repo.save_readme("New Content")

    mock_repo.get_contents.assert_called_once_with(repo.readme_filename, ref=repo.branch)
    mock_repo.update_file.assert_called_once_with(
        path=repo.readme_filename,
        message=repo.commit_message,
        content="New Content",
        sha="fake-sha",
    )


def test_save_readme_file_not_found(github_repo):
    repo, mock_repo = github_repo
    mock_repo.get_contents.side_effect = UnknownObjectException(404, {}, {})

    with pytest.raises(FileNotFoundError):
        repo.save_readme("New Content")

    mock_repo.get_contents.assert_called_once_with(repo.readme_filename, ref=repo.branch)


def test_save_readme_when_readme_is_directory(github_repo):
    repo, mock_repo = github_repo
    mock_repo.get_contents.return_value = [MagicMock(), MagicMock()]

    with pytest.raises(ValueError) as exc_info:
        repo.save_readme("New Content")

    assert f"{repo.readme_filename} is a directory" in str(exc_info.value)
    mock_repo.get_contents.assert_called_once_with(repo.readme_filename, ref=repo.branch)
