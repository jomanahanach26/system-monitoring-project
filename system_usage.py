"""Läser av hur mycket av datorns cpu, ram-minne och disk som används."""

import os

import psutil


def get_root_directory():
    """Returnerar root directory för operativsystemet: C:\\ på Windows o / på Mac och Linux."""
    # os.name är "nt" på Windows
    if os.name == "nt":
        return "C:\\"
    return "/"


class SystemUsage:
    """Hämtar nuvarande användning av cpu, ram-minne och disk i procent."""

    def __init__(self):
        """Sparar vilken mapp diskanvändningen ska mätas för."""
        self.root_directory = get_root_directory()

    def get_cpu_usage(self):
        """Returnerar cpu-användningen i procent, mätt under en sekund."""
        return psutil.cpu_percent(interval=1)

    def get_ram_usage(self):
        """Returnerar ram-minnesanvändningen i procent."""
        return psutil.virtual_memory().percent

    def get_disk_usage(self):
        """Returnerar diskanvändningen i procent för root directory."""
        return psutil.disk_usage(self.root_directory).percent

    def get_all_usage(self):
        """Returnerar användningen för alla kategorier, med samma namn som larmens kategorier."""
        return {
            "cpu": self.get_cpu_usage(),
            "ram": self.get_ram_usage(),
            "disk": self.get_disk_usage(),
        }
