"""Module for testing the logger functionality."""
import unittest
from logger import format_log_entry


class TestLogger(unittest.TestCase):
    """Test case class for logger functions."""

    def test_format_log_entry(self):
        """Test the format_log_entry function."""
        # Förbered (Arrange)
        time = "2023-10-15 12:00:00"
        category = "info"
        message = "Testmeddelande"

        # Kör (Act)
        result = format_log_entry(time, category, message)

        # Kontrollera (Assert)
        self.assertEqual(
            result, "[2023-10-15 12:00:00] [INFO] - Testmeddelande\n"
        )


if __name__ == "__main__":
    unittest.main()