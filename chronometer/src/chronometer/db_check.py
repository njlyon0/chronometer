# Import `os` from the standard library to read environment variables
import os

# Import `psycopg` (Postgres driver)
import psycopg


# Connect to Postgres and print its version
def main() -> None:
    # Credentials come from `.env`; host defaults to `db` (the compose service name)
    with psycopg.connect(
        host=os.environ.get("DB_HOST", "db"),
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        dbname=os.environ["POSTGRES_DB"],
    ) as conn:
        # Ask the server for its version string
        row = conn.execute("SELECT version()").fetchone()
        # Print it (a successful print means the connection worked)
        print(row[0] if row else "No version returned")


# Allow running as `python -m chronometer.db_check`
if __name__ == "__main__":
    main()
