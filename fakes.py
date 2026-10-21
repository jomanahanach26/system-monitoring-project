"""Låtsasklasser som testerna använder i stället för de riktiga klasserna.

De gör att testerna går snabbt, alltid ger samma resultat och inte skapar några loggfiler.
"""


class FakeLogger:
    """Låtsas vara loggsystemets Logger och sparar logginläggen i en lista i stället för i en fil."""

    def __init__(self):
        """Inga logginlägg finns från början."""
        self.entries = []

    def write_log(self, category: str, message: str):
        """Sparar logginlägget som (kategori, meddelande) så att testerna kan kontrollera det."""
        self.entries.append((category, message))


class FakeSystemUsage:
    """Låtsas vara SystemUsage, så att användningen alltid är densamma och inget mäts på riktigt."""

    def __init__(self, interrupt_after_iterations):
        """Sparar efter hur många varv testet ska låtsas att användaren trycker Ctrl+C (None betyder aldrig)."""
        self.interrupt_after_iterations = interrupt_after_iterations
        self.iterations_measured = 0

    def get_all_usage(self):
        """Returnerar samma användning varje gång, eller skickar KeyboardInterrupt som Ctrl+C."""
        if self.iterations_measured == self.interrupt_after_iterations:
            raise KeyboardInterrupt
        self.iterations_measured += 1
        return {"cpu": 63.0, "ram": 70.0, "disk": 95.5}
