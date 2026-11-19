# Load needed libraries
import csv
from pathlib import Path
from typing import Any
from django.core.management.base import BaseCommand, CommandParser

# Define command for reading CSVs
class Command(BaseCommand):
    help = "Import weekly hours from a CSV file"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("path", type=Path)

    def handle(self, *args: Any, **options: Any) -> None:
        with options["path"].open(newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.stdout.write(str(row))

