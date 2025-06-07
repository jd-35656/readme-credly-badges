"Exceptions Module"


class ReadmeCredlyError(Exception):
    """Exception raised for errors in the Readme Credly module."""


class PageLoadError(ReadmeCredlyError):
    """Exception raised when the Credly page fails to load."""


class BadgeNotFoundError(ReadmeCredlyError):
    """Exception raised when the Credly page is not found."""


class PageTimeoutError(ReadmeCredlyError):
    """Exception raised when the Credly page times out."""


class BadgeExtractionError(ReadmeCredlyError):
    """Exception raised when there is an error extracting badge information."""
