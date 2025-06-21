from unittest.mock import MagicMock, patch

import pytest
import requests

from readme_credly_badges.adapter import Credly

# Sample valid badge data
VALID_BADGE = {
    "id": "123456",
    "badge_template": {
        "name": "Python Pro",
        "image_url": "https://example.com/image.png",
    },
}

# Sample invalid badges (missing fields)
BADGES_WITH_MISSING_FIELDS = [
    {},
    {"id": "", "badge_template": {}},
    {"id": "789", "badge_template": {"name": "", "image_url": "img.png"}},
    {"id": "456", "badge_template": {"name": "DevOps", "image_url": ""}},
]


@patch("readme_credly_badges.adapter.credly.requests.get")
def test_fetch_valid_badges(mock_get):
    """Test that valid badges are returned correctly."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [VALID_BADGE]}
    mock_get.return_value = mock_response

    credly = Credly("testuser")
    badges = credly.fetch_badges()

    assert len(badges) == 1
    assert badges[0]["name"] == "Python Pro"
    assert badges[0]["url"] == "https://www.credly.com/badges/123456"
    assert badges[0]["image_url"] == "https://example.com/image.png"


@patch("readme_credly_badges.adapter.credly.requests.get")
def test_fetch_skips_incomplete_badges(mock_get):
    """Test that incomplete badges are skipped."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": BADGES_WITH_MISSING_FIELDS}
    mock_get.return_value = mock_response

    credly = Credly("testuser")
    badges = credly.fetch_badges()

    assert badges == []


@patch("readme_credly_badges.adapter.credly.requests.get")
def test_fetch_handles_http_error(mock_get):
    """Test that HTTP errors raise a ConnectionError."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("Boom!")
    mock_get.return_value = mock_response

    credly = Credly("testuser")
    with pytest.raises(ConnectionError):
        credly.fetch_badges()


@patch("readme_credly_badges.adapter.credly.requests.get")
def test_fetch_handles_network_error(mock_get):
    """Test that request exceptions raise a ConnectionError."""
    mock_get.side_effect = requests.exceptions.RequestException("Network down")

    credly = Credly("testuser")
    with pytest.raises(ConnectionError):
        credly.fetch_badges()


@patch("readme_credly_badges.adapter.credly.requests.get")
def test_fetch_handles_missing_data_key(mock_get):
    """Test fallback if 'data' key is missing."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    credly = Credly("testuser")
    badges = credly.fetch_badges()

    assert badges == []
