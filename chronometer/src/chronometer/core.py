# Import `dataclass` decorator and `date` class from standard library
from dataclasses import dataclass
from datetime import date


# Define a Person class (with a hint for the dev that `name` should be a string)
@dataclass(frozen=True)
class Person:
    name: str


# Define the Project class (with a hint for the dev that `name` should be a string)
@dataclass(frozen=True)
class Project:
    name: str


# Define WeeklyHours class (with a hint that hours should be a float)
@dataclass(frozen=True)
class WeeklyHours:
    person: Person
    project: Project
    week_of: date
    hours: float

    # Fail to create a WeeklyHours object if `hours` are negative or `week_of` date isn't a Monday.
    # (Called automatically at the end of the `__init__` that `@dataclass` generates)
    def __post_init__(self) -> None:
        # Throw an error for negative time
        if self.hours < 0:
            raise ValueError(f"hours must be non-negative, got {self.hours}")
        # Throw an error for non-Monday week dates
        if self.week_of.weekday() != 0:
            raise ValueError(f"week_of must be a Monday, got {self.week_of:%A}")


# Define the `add_hours()` function
def add_hours(
    # Give an unenforced type hint for each parameter
    records: list[WeeklyHours],
    person: Person,
    project: Project,
    week_of: date,
    hours: float,
) -> list[WeeklyHours]:
    # Build one new `WeeklyHours` record (this triggers the `__post_init__` checks)
    record = WeeklyHours(person=person, project=project, week_of=week_of, hours=hours)
    # Return all of the extant records and add the newest record as a new list that is flat and has everything (new and old)
    return [*records, record]


# Define the `total_by_project` function that sums hours spent on each project
def total_by_project(records: list[WeeklyHours]) -> dict[str, float]:
    # Create a dictionary to store subsequent results
    totals: dict[str, float] = {}
    # Loop across each record in the full set of records
    for record in records:
        # Grab the project name from a given record
        name = record.project.name
        # Add the hours of a given record for a given project to the running total of the hours for that project
        totals[name] = totals.get(name, 0.0) + record.hours
    # Return the dictionary with each project's total time allocation
    return totals
