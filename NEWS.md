## Version 0.7.0 - Continuous Integration

- Adds CI for testing and formatting
- Adds pre-commit lint hook
- Adds `just lint` recipe (preventative shorthand for pre-commit check)

## Version 0.6.0 - Just

- Adds `justfile` to simplify command line interactions

## Version 0.5.0 - CSV Import Command

- Adds ability to pass CSV of people/project/week/hours for integration into database
- Validates every CSV row and reports bad rows by line number
- Wraps the import in a transaction (all rows save, or none do)
- Adds `--dry-run` flag to preview an import without saving
- Updates existing rows if person/project/week found in CSV (instead of making duplicates)

## Version 0.4.0 - Django

- Adds Django app scaffolding (`app/manage.py`, `app/config/`, & `app/tracker/`)
- Adds constraint that `WeeklyHours` needs to be unique combinations of person/project/week
- Registers Django admin

## Version 0.3.0 - Queries

- Adds `docker-compose.yml` with `app` and `db` services
- Allows connection to named Postgres volume via local `.env`
- Requires successful healthcheck for connection to `db`

## Version 0.2.0 - Containers

- Containerizes with Docker
  - Supports a `build` and `test` command

## Version 0.1.0 - Bare Bones

- Includes only plain Python and unit tests
