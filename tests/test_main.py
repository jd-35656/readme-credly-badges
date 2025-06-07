import logging
from unittest.mock import MagicMock, patch

import pytest

import src.main as main_module


def test_generate_new_readme_content_success():
    old_readme = (
        "Header\n"
        "<!-- START CREDLY BADGES -->\n"
        "old badges\n"
        "<!-- END CREDLY BADGES -->\n"
        "Footer\n"
    )
    badges = [
        {"name": "Badge1", "image_url": "image1.png", "url": "http://url1"},
        {"name": "Badge2", "image_url": "image2.png", "url": "http://url2"},
    ]

    expected_new_badges = (
        "[![Badge1](image1.png)](http://url1)\n" "[![Badge2](image2.png)](http://url2)"
    )

    new_content = main_module.generate_new_readme_content(badges, old_readme)
    assert "<!-- START CREDLY BADGES -->" in new_content
    assert "<!-- END CREDLY BADGES -->" in new_content
    assert expected_new_badges in new_content
    assert new_content.startswith("Header")
    assert new_content.endswith("Footer\n")


def test_generate_new_readme_content_raises_if_markers_missing():
    old_readme = "No badge markers here."

    with pytest.raises(ValueError):
        main_module.generate_new_readme_content([], old_readme)


@patch("src.main.Credly")
@patch("src.main.GithubRepo")
def test_main_happy_path(mock_githubrepo_cls, mock_credly_cls, caplog):
    caplog.set_level(logging.INFO)
    # Mock environment variables in settings module
    with patch.multiple(
        "src.main",
        CREDLY_USERNAME="user",
        GITHUB_TOKEN="token",
        GITHUB_REPO="repo",
        GITHUB_API_URL="https://api.github.com",
        GITHUB_BRANCH="main",
        README_FILE="README.md",
        COMMIT_MESSAGE="commit message",
    ):
        # Mock Credly instance and badges
        mock_credly = MagicMock()
        mock_credly.fetch_badges.return_value = [
            {
                "name": "Test Badge",
                "image_url": "img.png",
                "url": "http://badge.url",
            }
        ]
        mock_credly_cls.return_value = mock_credly

        # Mock GithubRepo instance and README contents
        mock_repo = MagicMock()
        old_readme_content = "Intro\n<!-- START CREDLY BADGES -->\nold\n<!-- END CREDLY BADGES -->\nOutro"
        mock_repo.get_readme.return_value = old_readme_content
        mock_githubrepo_cls.return_value = mock_repo

        # Run main
        main_module.main()

        # Check methods called as expected
        mock_credly.fetch_badges.assert_called_once()
        mock_repo.get_readme.assert_called_once()
        mock_repo.save_readme.assert_called_once()

        # The new README content saved should contain the badge markdown
        saved_content = mock_repo.save_readme.call_args[1]["new_content"]
        assert "![Test Badge](img.png)" in saved_content

        # Logging info that README updated
        assert "README updated with new Credly badges." in caplog.text


@patch("src.main.Credly")
@patch("src.main.GithubRepo")
def test_main_no_update_needed(mock_githubrepo_cls, mock_credly_cls, caplog):
    caplog.set_level(logging.INFO)
    with patch.multiple(
        "src.main",
        CREDLY_USERNAME="user",
        GITHUB_TOKEN="token",
        GITHUB_REPO="repo",
        GITHUB_API_URL="https://api.github.com",
        GITHUB_BRANCH="main",
        README_FILE="README.md",
        COMMIT_MESSAGE="commit message",
    ):
        mock_credly = MagicMock()
        badges = [{"name": "Badge", "image_url": "img.png", "url": "http://url"}]
        mock_credly.fetch_badges.return_value = badges
        mock_credly_cls.return_value = mock_credly

        badge_markdown = "[![Badge](img.png)](http://url)"
        readme_content = f"Start\n<!-- START CREDLY BADGES -->\n{badge_markdown}\n<!-- END CREDLY BADGES -->\nEnd"

        mock_repo = MagicMock()
        mock_repo.get_readme.return_value = readme_content
        mock_githubrepo_cls.return_value = mock_repo

        main_module.main()

        mock_repo.save_readme.assert_not_called()
        assert "README is already up to date." in caplog.text


def test_main_missing_env_vars(monkeypatch):
    # Clear env vars to simulate missing variables
    with patch.multiple(
        "src.main",
        CREDLY_USERNAME=None,
        GITHUB_TOKEN=None,
        GITHUB_REPO=None,
    ):
        with pytest.raises(ValueError):
            main_module.main()
