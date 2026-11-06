# Import `date` class from standard library
from datetime import date

# Import `pytest`
import pytest

# Import chronometer classes and functions
from chronometer.core import Person, Project, WeeklyHours, add_hours, total_by_project


# Test that `add_hours()` only returns one new record
def test_add_hours_returns_list_with_new_record() -> None:
    # Assign acceptable values to each parameter
    person = Person("Ada")
    project = Project("Chronometer")
    week_of = date(2026, 11, 2)
    hours = 3.0
    # Invoke the `add_hours()` function with an empty starting list
    records = add_hours([], person, project, week_of, hours)
    # Assert that the `add_hours()` function returns exactly one record equal to a manually-made `WeeklyHours`
    assert records == [WeeklyHours(person, project, week_of, hours)]


# Test that `add_hours()` doesn't change the input list (the main point of [*records, record])
def test_add_hours_doesnt_change_input_list() -> None:
    # Assign acceptable values to each parameter
    person = Person("Ada")
    project = Project("Chronometer")
    week_of = date(2026, 11, 2)
    hr1 = 2
    hr2 = 4
    # Invoke `add_hours()` to assemble multiple records with a shared project
    record1 = add_hours([], person, project, week_of, hr1)
    records = add_hours(record1, person, project, week_of, hr2)
    # Test that the original record is unchanged
    assert records[0] == WeeklyHours(person, project, week_of, hr1)


# Test that negative hours raise ValueError
def test_add_hours_rejects_neg_hours() -> None:
    # Assign acceptable values to most parameters but make hours negative
    person = Person("Ada")
    project = Project("Chronometer")
    week_of = date(2026, 11, 2)
    hours = -3.0
    # Invoke `add_hours()` with `pytest.raises` as context manager to get expected error
    with pytest.raises(ValueError, match="non-negative"):
        add_hours([], person, project, week_of, hours)


# Test that on-Monday week_of raises ValueError
def test_add_hours_rejects_non_mondays() -> None:
    # Assign acceptable values to most parameters but use a date that's not a Monday
    person = Person("Ada")
    project = Project("Chronometer")
    week_of = date(2026, 11, 4)
    hours = 2.0
    # Invoke `add_hours()` with `pytest.raises` as context manager to get expected error
    with pytest.raises(ValueError, match="Monday"):
        add_hours([], person, project, week_of, hours)


# Test that zero hours are allowed (the edge case for < 0)
def test_add_hours_allows_zero_hours() -> None:
    # Assign acceptable values to each parameter and 0 to hours
    person = Person("Ada")
    project = Project("Chronometer")
    week_of = date(2026, 11, 2)
    hours = 0
    # Invoke the `add_hours()` function with an empty starting list
    add_hours([], person, project, week_of, hours)


# Test that `total_by_project()` adds up multiple records for the same project
def test_total_by_project_sums_multiple_records() -> None:
    # Assign acceptable values to each parameter
    person = Person("Ada")
    project = Project("Chronometer")
    week_of = date(2026, 11, 2)
    hr1 = 1.6
    hr2 = 1.5
    # Invoke `add_hours()` to assemble multiple records with a shared project
    record1 = add_hours([], person, project, week_of, hr1)
    records = add_hours(record1, person, project, week_of, hr2)
    # Invoke `total_by_project()`
    totals = total_by_project(records=records)
    # Expect total hours to be equal to the sum of `hr1` and `hr2`
    assert totals == {project.name: hr1 + hr2}


# Test that `total_by_project()` keeps different projects separate
def test_total_by_project_keeps_diff_projects_separate() -> None:
    # Assign acceptable values to each parameter
    person = Person("Ada")
    proj1 = Project("Chronometer")
    proj2 = Project("Tempo")
    week_of = date(2026, 11, 2)
    hours = 12
    # Invoke `add_hours()` to assemble multiple records
    record1 = add_hours([], person, proj1, week_of, hours)
    records = add_hours(record1, person, proj2, week_of, hours)
    # Invoke `total_by_project()`
    totals = total_by_project(records=records)
    # Expect multiple projects
    assert totals == {proj1.name: hours, proj2.name: hours}


# Test that `total_by_project()` doesn't mix up project's hours
def test_total_by_project_doesnt_break_project_hour_links() -> None:
    # Assign acceptable values to each parameter
    person = Person("Ada")
    proj1 = Project("Chronometer")
    proj2 = Project("Tempo")
    week_of = date(2026, 11, 2)
    hr1 = 5.0
    hr2 = 7.0
    # Invoke `add_hours()` to assemble multiple records
    record1 = add_hours([], person, proj1, week_of, hr1)
    records = add_hours(record1, person, proj2, week_of, hr2)
    # Invoke `total_by_project()`
    totals = total_by_project(records=records)
    # Expect that each project retains its corresponding hours
    assert totals == {proj1.name: hr1, proj2.name: hr2}


# Test that ``total_by_project([])` returns `{}`
def test_total_by_project_doesnt_invent_data() -> None:
    empty_totals = total_by_project(records=[])
    # Expect no records to produce an empty dictionary
    assert empty_totals == {}
