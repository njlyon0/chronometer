# Load needed libraries
import csv
from pathlib import Path
from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from datetime import date
from decimal import Decimal, InvalidOperation
from chronometer import core

# Columns that every row must have
REQUIRED = ("person", "project", "week_of", "hours")


# Clean one CSV row, or raise ValueError with a message a person can read
def parse_row(row: dict[str, Any]) -> dict[str, Any]:
    # Strip whitespace (a short row gives None for missing columns, so use `or ""`)
    values = {key: (row.get(key) or "").strip() for key in REQUIRED}

    # Find all empty fields, not only the first one
    missing = [key for key, value in values.items() if not value]
    if missing:
        raise ValueError(f"missing value for {', '.join(missing)}")

    # Parse the date
    try:
        week_of = date.fromisoformat(values["week_of"])
    except ValueError:
        raise ValueError(
            f"week_of must be a YYYY-MM-DD date, got {values['week_of']!r}"
        ) from None

    # Parse the hours (Decimal, because the model uses DecimalField)
    try:
        hours = Decimal(values["hours"])
    except InvalidOperation:
        raise ValueError(f"hours must be a number, got {values['hours']!r}") from None
    if not hours.is_finite():
        raise ValueError(f"hours must be a number, got {values['hours']!r}")

    # Reuse the Monday and non-negative checks in core.WeeklyHours.__post_init__
    core.WeeklyHours(
        person=core.Person(values["person"]),
        project=core.Project(values["project"]),
        week_of=week_of,
        hours=hours,
    )

    return {
        "person": values["person"],
        "project": values["project"],
        "week_of": week_of,
        "hours": hours,
    }


# Define command for reading CSVs
class Command(BaseCommand):
    help = "Import weekly hours from a CSV file"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("path", type=Path)

    def handle(self, *args: Any, **options: Any) -> None:
        with options["path"].open(newline="") as f:
            reader = csv.DictReader(f)
            # Don't stop when bad rows are encountered in the CSV
            good, bad = [], []
            for row in reader:
                try:
                    good.append(parse_row(row))
                except ValueError as e:
                    bad.append((reader.line_num, str(e)))
