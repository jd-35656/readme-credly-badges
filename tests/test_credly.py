"Credly Tests"

from unittest.mock import MagicMock, patch

import pytest

from src.credly import Credly
from src.exceptions import (
    BadgeExtractionError,
    BadgeNotFoundError,
    PageLoadError,
    PageTimeoutError,
    ReadmeCredlyError,
)


@pytest.fixture
def credly() -> Credly:
    """Fixture to create a Credly instance for testing."""
    return Credly("testuser")


def test_init_sets_values(credly: Credly) -> None:
    "Test that Credly instance initializes with correct values."
    assert credly.username == "testuser"
    assert credly.timeout == 60000
    assert credly.url == "https://www.credly.com/users/testuser"


def test_handle_popup_coockie_with_click(credly: Credly) -> None:
    "Test for handling coockie accepter"

    page = MagicMock()
    page.wait_for_selector.return_value = True
    credly._handle_cookie_popup(page)
    page.wait_for_selector.assert_called_with(
        'button:has-text("Accept")', timeout=credly.timeout
    )
    page.click.assert_called_with('button:has-text("Accept")')


def test_handle_popup_coockie_without_click(credly: Credly) -> None:
    "Test for handling coockie accepter without calls"

    page = MagicMock()
    page.wait_for_selector.side_effect = TimeoutError("no selector")
    credly._handle_cookie_popup(page)
    page.click.assert_not_called()


def test_get_badge_count(credly) -> None:
    "Test for getting badge count from the page"

    page = MagicMock()
    page.wait_for_selector.return_value = True

    mock_elemnt = MagicMock()
    mock_elemnt.text_content.return_value = "Badges (5)"
    page.query_selector.return_value = mock_elemnt

    count = credly._get_badge_count(page)

    assert count == 5
    page.query_selector.assert_called_with(
        "div.Typographystyles__Container-fredly__sc-1jldzrm-0:nth-child(1)"
    )


def test_get_badge_count_zero_badges(credly) -> None:
    "Test for getting badge count from the page"

    page = MagicMock()
    page.wait_for_selector.return_value = True

    mock_elemnt = MagicMock()
    mock_elemnt.text_content.return_value = "Badges (0)"
    page.query_selector.return_value = mock_elemnt

    with pytest.raises(BadgeNotFoundError):
        credly._get_badge_count(page)
    page.query_selector.assert_called_with(
        "div.Typographystyles__Container-fredly__sc-1jldzrm-0:nth-child(1)"
    )


def test_get_badge_count_no_badges(credly: Credly) -> None:
    "Test for getting badge count when no badges are present"

    page = MagicMock()
    page.wait_for_selector.return_value = True

    mock_elemnt = MagicMock()
    mock_elemnt.text_content.return_value = "No badges found"
    page.query_selector.return_value = mock_elemnt

    with pytest.raises(
        BadgeNotFoundError,
    ):
        credly._get_badge_count(page)

    page.query_selector.assert_called_with(
        "div.Typographystyles__Container-fredly__sc-1jldzrm-0:nth-child(1)"
    )


def test_get_badge_count_timeout(credly) -> None:
    "Test for getting badge count with timeout"

    # Ensure timeout is available
    credly.timeout = 1000

    page = MagicMock()
    # Simulate timeout from Playwright
    page.wait_for_selector.side_effect = TimeoutError(
        "Timeout while waiting for selector"
    )

    with pytest.raises(PageTimeoutError):
        credly._get_badge_count(page)

    page.wait_for_selector.assert_called_with(
        "div.Typographystyles__Container-fredly__sc-1jldzrm-0:nth-child(1)",
        timeout=credly.timeout,
    )


def test_expand_all_badges(credly: Credly) -> None:
    "Test for expanding all badges on the page"

    page = MagicMock()
    page.wait_for_selector.return_value = True

    credly._expand_all_badges(page)

    page.wait_for_selector.assert_called_with(
        "button.Buttonstyles__StyledButton-fredly__sc-k2a0sj-4",
        timeout=credly.timeout,
    )
    page.click.assert_called_with(
        "button.Buttonstyles__StyledButton-fredly__sc-k2a0sj-4"
    )


def test_expand_all_badges_timeout(credly: Credly) -> None:
    "Test for expanding all badges with timeout"

    page = MagicMock()
    # Simulate timeout from Playwright
    page.wait_for_selector.side_effect = TimeoutError(
        "Timeout while waiting for selector"
    )

    with pytest.raises(
        PageTimeoutError,
    ):
        credly._expand_all_badges(page)

    page.wait_for_selector.assert_called_with(
        "button.Buttonstyles__StyledButton-fredly__sc-k2a0sj-4",
        timeout=credly.timeout,
    )
    page.click.assert_not_called()


def test_extract_nth_badge_info_success(credly: Credly) -> None:
    n = 3
    page = MagicMock()
    page.url = "https://profile.url/users/username"

    # Mock wait_for_selector (just succeeds)
    page.wait_for_selector.return_value = True

    # Mock query_selector on page returns badge_element mock
    badge_element = MagicMock()
    page.query_selector.return_value = badge_element

    # badge_element.query_selector returns mocks for title and img elements
    title_element = MagicMock()
    title_element.text_content.return_value = " Badge Title "
    img_element = MagicMock()
    img_element.get_attribute.return_value = " https://image.url/badge.png "

    badge_element.query_selector.side_effect = lambda sel: {
        "div.settings__skills-profile__edit-skills-profile__badge-card__organization-name-two-lines": title_element,
        "img.settings__skills-profile__edit-skills-profile__badge-card__badge-image": img_element,
    }[sel]

    # badge_element.click just mocked (no return)
    badge_element.click.return_value = None

    # Mock wait_for_function that waits for URL change
    page.wait_for_function.side_effect = [True, True]

    # Simulate URL change after click
    page.url = "https://profile.url/badges/12345"

    # Mock go_back returns None
    page.go_back.return_value = None

    result = credly._extract_nth_badge_info(page, n)

    assert result == {
        "url": "https://profile.url/badges/12345",
        "title": "Badge Title",
        "image": "https://image.url/badge.png",
    }

    # Check that methods were called as expected
    page.wait_for_selector.assert_called_with(
        f"div.settings__skills-profile__edit-skills-profile__badge-list__list-item:nth-child({n})",
        timeout=credly.timeout,
    )
    page.query_selector.assert_called_with(
        f"div.settings__skills-profile__edit-skills-profile__badge-list__list-item:nth-child({n})"
    )
    badge_element.query_selector.assert_any_call(
        "div.settings__skills-profile__edit-skills-profile__badge-card__organization-name-two-lines"
    )
    badge_element.query_selector.assert_any_call(
        "img.settings__skills-profile__edit-skills-profile__badge-card__badge-image"
    )
    badge_element.click.assert_called_once()
    page.go_back.assert_called_once()


def test_extract_nth_badge_info_badge_element_not_found(
    credly: Credly,
) -> None:
    n = 1
    page = MagicMock()
    page.wait_for_selector.return_value = True
    page.query_selector.return_value = None

    with pytest.raises(BadgeNotFoundError):
        credly._extract_nth_badge_info(page, n)


def test_extract_nth_badge_info_missing_title_element(credly: Credly) -> None:
    n = 2
    page = MagicMock()
    page.wait_for_selector.return_value = True
    badge_element = MagicMock()
    page.query_selector.return_value = badge_element

    # title element missing
    badge_element.query_selector.side_effect = lambda sel: (
        None if "organization-name" in sel else MagicMock()
    )

    with pytest.raises(AttributeError):
        # Because title_element.text_content() will raise
        credly._extract_nth_badge_info(page, n)


def test_extract_nth_badge_info_missing_img_element(credly: Credly) -> None:
    n = 2
    page = MagicMock()
    page.wait_for_selector.return_value = True
    badge_element = MagicMock()
    page.query_selector.return_value = badge_element

    # img element missing
    def query_selector_mock(sel):
        if "organization-name" in sel:
            mock = MagicMock()
            mock.text_content.return_value = "Some Title"
            return mock
        return None

    badge_element.query_selector.side_effect = query_selector_mock

    with pytest.raises(AttributeError):
        credly._extract_nth_badge_info(page, n)


def test_extract_nth_badge_info_empty_fields(credly: Credly) -> None:
    n = 1
    page = MagicMock()
    page.wait_for_selector.return_value = True

    badge_element = MagicMock()
    page.query_selector.return_value = badge_element

    # Return empty strings after strip
    title_element = MagicMock()
    title_element.text_content.return_value = "  "
    img_element = MagicMock()
    img_element.get_attribute.return_value = "  "

    badge_element.query_selector.side_effect = lambda sel: {
        "div.settings__skills-profile__edit-skills-profile__badge-card__organization-name-two-lines": title_element,
        "img.settings__skills-profile__edit-skills-profile__badge-card__badge-image": img_element,
    }[sel]

    badge_element.click.return_value = None

    page.wait_for_function.side_effect = [True, True]
    page.url = "   "  # empty badge url

    page.go_back.return_value = None

    with pytest.raises(
        BadgeExtractionError,
    ):
        credly._extract_nth_badge_info(page, n)


def test_extract_nth_badge_info_timeout_waiting_for_selector(
    credly: Credly,
) -> None:
    n = 1
    page = MagicMock()
    page.wait_for_selector.side_effect = TimeoutError("Timeout waiting for selector")

    with pytest.raises(PageTimeoutError):
        credly._extract_nth_badge_info(page, n)


def test_extract_nth_badge_info_timeout_waiting_for_url_change(
    credly: Credly,
) -> None:
    n = 1
    page = MagicMock()
    page.url = "https://profile.url/users/username"
    page.wait_for_selector.return_value = True

    badge_element = MagicMock()
    page.query_selector.return_value = badge_element

    title_element = MagicMock()
    title_element.text_content.return_value = "Title"
    img_element = MagicMock()
    img_element.get_attribute.return_value = "https://image.url"

    badge_element.query_selector.side_effect = lambda sel: {
        "div.settings__skills-profile__edit-skills-profile__badge-card__organization-name-two-lines": title_element,
        "img.settings__skills-profile__edit-skills-profile__badge-card__badge-image": img_element,
    }[sel]

    badge_element.click.return_value = None

    # First wait_for_function raises TimeoutError (URL change wait)
    page.wait_for_function.side_effect = TimeoutError("Timeout waiting for URL change")

    with pytest.raises(PageTimeoutError):
        credly._extract_nth_badge_info(page, n)


def test_extract_nth_badge_info_timeout_waiting_for_go_back(
    credly: Credly,
) -> None:
    n = 1
    page = MagicMock()
    page.url = "https://profile.url/users/username"
    page.wait_for_selector.return_value = True

    badge_element = MagicMock()
    page.query_selector.return_value = badge_element

    title_element = MagicMock()
    title_element.text_content.return_value = "Title"
    img_element = MagicMock()
    img_element.get_attribute.return_value = "https://image.url"

    badge_element.query_selector.side_effect = lambda sel: {
        "div.settings__skills-profile__edit-skills-profile__badge-card__organization-name-two-lines": title_element,
        "img.settings__skills-profile__edit-skills-profile__badge-card__badge-image": img_element,
    }[sel]

    badge_element.click.return_value = None
    page.wait_for_function.side_effect = [
        True,
        TimeoutError("Timeout waiting for go back"),
    ]

    page.go_back.return_value = None

    with pytest.raises(PageTimeoutError):
        credly._extract_nth_badge_info(page, n)


# Helper to setup mocks for the playwright environment
def setup_playwright_mocks(mock_sync_playwright):
    mock_playwright = MagicMock()
    mock_browser = MagicMock()
    mock_page = MagicMock()
    mock_response = MagicMock(status=200)

    mock_sync_playwright.return_value = mock_playwright
    mock_playwright.__enter__.return_value = mock_playwright
    mock_playwright.__exit__.return_value = None
    mock_playwright.chromium.launch.return_value = mock_browser
    mock_browser.new_page.return_value = mock_page
    mock_page.goto.return_value = mock_response

    return mock_playwright, mock_browser, mock_page, mock_response


@patch("src.credly.sync_playwright")
@patch.object(Credly, "_handle_cookie_popup")
@patch.object(Credly, "_get_badge_count", return_value=2)
@patch.object(Credly, "_expand_all_badges")
@patch.object(
    Credly,
    "_extract_nth_badge_info",
    side_effect=[
        {"url": "url1", "title": "title1", "image": "img1"},
        {"url": "url2", "title": "title2", "image": "img2"},
    ],
)
def test_fetch_badges_success(
    mock_extract,
    mock_expand,
    mock_get_count,
    mock_handle_cookie,
    mock_sync_playwright,
    credly: Credly,
):
    mock_playwright, mock_browser, mock_page, mock_response = setup_playwright_mocks(
        mock_sync_playwright
    )

    badges = credly.fetch_badges()

    # Validate returned badges
    assert len(badges) == 2
    assert badges[0]["title"] == "title1"
    assert badges[1]["title"] == "title2"

    # Assert methods called expected number of times
    mock_handle_cookie.assert_called_once_with(mock_page)
    mock_get_count.assert_called_once_with(mock_page)
    assert mock_expand.call_count == 2
    assert mock_extract.call_count == 2

    # Browser closed
    mock_browser.close.assert_called_once()


@patch("src.credly.sync_playwright")
def test_fetch_badges_page_load_failure(mock_sync_playwright, credly: Credly):
    mock_playwright = MagicMock()
    mock_browser = MagicMock()
    mock_page = MagicMock()
    # Simulate page.goto returning None or bad status
    mock_page.goto.return_value = None
    mock_sync_playwright.return_value = mock_playwright
    mock_playwright.__enter__.return_value = mock_playwright
    mock_playwright.__exit__.return_value = None
    mock_playwright.chromium.launch.return_value = mock_browser
    mock_browser.new_page.return_value = mock_page

    with pytest.raises(PageLoadError):
        credly.fetch_badges()

    mock_browser.close.assert_called_once()


@patch("src.credly.sync_playwright")
@patch.object(Credly, "_handle_cookie_popup")
@patch.object(
    Credly,
    "_get_badge_count",
    side_effect=ReadmeCredlyError("Some internal error"),
)
def test_fetch_badges_internal_error_propagates(
    mock_get_count, mock_handle_cookie, mock_sync_playwright, credly: Credly
):
    mock_playwright, mock_browser, mock_page, mock_response = setup_playwright_mocks(
        mock_sync_playwright
    )

    with pytest.raises(ReadmeCredlyError, match="Some internal error"):
        credly.fetch_badges()

    mock_browser.close.assert_called_once()
    mock_handle_cookie.assert_called_once_with(mock_page)
    mock_get_count.assert_called_once_with(mock_page)


@patch("src.credly.sync_playwright")
@patch.object(Credly, "_handle_cookie_popup")
@patch.object(Credly, "_get_badge_count", return_value=1)
@patch.object(Credly, "_expand_all_badges")
@patch.object(
    Credly,
    "_extract_nth_badge_info",
    return_value={"url": "url", "title": "title", "image": "image"},
)
def test_fetch_badges_browser_close_even_on_exception(
    mock_extract,
    mock_expand,
    mock_get_count,
    mock_handle_cookie,
    mock_sync_playwright,
    credly: Credly,
):
    mock_playwright, mock_browser, mock_page, mock_response = setup_playwright_mocks(
        mock_sync_playwright
    )

    # Make _extract_nth_badge_info raise an exception mid-loop
    mock_extract.side_effect = Exception("Fail!")

    with pytest.raises(Exception):
        credly.fetch_badges()

    mock_browser.close.assert_called_once()
