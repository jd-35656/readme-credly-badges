"Demo Test"

from src.main import main


def test_main():
    """
    Test the main function of the application.
    """
    assert main() is True, "Main function should return True"
