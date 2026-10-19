"""Längden på en monitorsession: antal varv eller antal sekunder, från 1 till oändligt."""

import math

# typerna av längd som användaren kan välja mellan
ITERATIONS = "iterations"
SECONDS = "seconds"

# ord som användaren kan skriva för en oändlig längd
INFINITE_WORDS = ("oändligt", "o")


def parse_length_type(choice: str):
    """Returnerar typen av längd utifrån användarens val: "1" för varv och "2" för sekunder.

    Returnerar None om valet är ogiltigt. (Pure function)
    """
    if choice.strip() == "1":
        return ITERATIONS
    if choice.strip() == "2":
        return SECONDS
    return None


def parse_length(text: str):
    """Returnerar längden som ett heltal från 1 och uppåt, eller math.inf för oändligt.

    Returnerar None om texten inte är en giltig längd. (Pure function)
    """
    cleaned_text = text.strip().lower()
    if cleaned_text in INFINITE_WORDS:
        return math.inf
    if cleaned_text.isdigit() and int(cleaned_text) >= 1:
        return int(cleaned_text)
    return None


class SessionLength:
    """Håller reda på hur länge en monitorsession ska pågå."""

    def __init__(self, length_type: str, length):
        """Sparar typen av längd (varv eller sekunder) och längden (heltal eller math.inf)."""
        self.length_type = length_type
        self.length = length

    def is_finished(self, iterations_done: int, seconds_passed: float):
        """Returnerar True när sessionen har pågått i så många varv eller sekunder som valts."""
        if self.length_type == ITERATIONS:
            return iterations_done >= self.length
        return seconds_passed >= self.length

    def __str__(self):
        """Returnerar en läsbar beskrivning av längden, till exempel "5 varv" eller "30 sekunder"."""
        if self.length_type == ITERATIONS:
            unit = "varv"
        else:
            unit = "sekunder"
        if self.length == math.inf:
            return f"oändligt antal {unit}"
        return f"{self.length} {unit}"
