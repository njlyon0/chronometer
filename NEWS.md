## Version 0.4.0 - Dev

This is the development version, changes will be listed below as they are made.

- Adds Django app scaffolding (`app/manage.py`, `app/config/`, & `app/tracker/`)


## Version 0.3.0 - Queries

- Adds `docker-compose.yml` with `app` and `db` services
- Allows connection to named Postgres volume via local `.env`
- Requires successful healthcheck for connection to `db`

## Version 0.2.0 - Containers

- Containerizes with Docker
  - Supports a `build` and `test` command

## Version 0.1.0 - Bare Bones

- Includes only plain Python and unit tests
