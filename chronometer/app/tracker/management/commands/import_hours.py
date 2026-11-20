# Load standard library stuff
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

# Load third party packages
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction

# Load code from this app
from chronometer import core
from tracker.models import Person, Project, WeeklyHours

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
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report what would change; write nothing",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        with options["path"].open(newline="") as f:
            reader = csv.DictReader(f)
            # Separate malformed vs. good rows of the given CSV
            good, bad = [], []
            for row in reader:
                try:
                    good.append(parse_row(row))
                except ValueError as e:
                    bad.append((reader.line_num, str(e)))
            # Grab each good row and add it to the database (rolling back on a dry run)
            created_count = updated_count = 0
            with transaction.atomic():
                for r in good:
                    person, _ = Person.objects.get_or_create(name=r["person"])
                    project, _ = Project.objects.get_or_create(name=r["project"])
                    _, created = WeeklyHours.objects.update_or_create(
                        person=person,
                        project=project,
                        week_of=r["week_of"],
                        defaults={"hours": r["hours"]},
                    )
                    if created: 
                        created_count += 1
                    else: 
                        updated_count += 1
                if options["dry_run"]:
                    transaction.set_rollback(True)
            # Report the results
            if options["dry_run"]:
                self.stdout.write(self.style.WARNING("DRY RUN — no changes saved"))
            self.stdout.write(
                f"{created_count} created, {updated_count} updated, {len(bad)} bad rows"
            )
            for line, message in bad:
                self.stderr.write(self.style.ERROR(f"line {line}: {message}"))
