import os
import sys

import pymssql

from utils import load_config


def setup_db() -> None:
    """
    Set up the database by dropping any existing tables and re-populating the data.
    """
    db_config = load_config("./config/db.config")

    server = db_config["db"]["server"]
    database = db_config["db"]["database"]
    user = db_config["db"]["user"]
    password = db_config["db"]["password"]

    conn = pymssql.connect(server=server, user=user, password=password, database=database)
    cursor = conn.cursor()

    print("[INFO] Dropping any existing database tables...")
    _drop(conn, cursor)

    print("[INFO] Re-populating the database with data...")
    _populate(conn, cursor)

    print("[INFO] Database setup complete")

    cursor.close()
    conn.close()


def _drop(conn: pymssql.Connection, cursor: pymssql.Cursor) -> None:
    """
    Drop existing database tables using the drop SQL script.

    Args:
        conn (pymssql.Connection): The database connection.
        cursor (pymssql.Cursor): The database cursor.
    """
    drop_sql_file = "./sql/drop.sql"

    print("[INFO] Executing drop SQL script...")
    _execute_sql_file(conn, cursor, drop_sql_file)
    print("[INFO] Drop SQL script execution complete")


def _populate(conn: pymssql.Connection, cursor: pymssql.Cursor) -> None:
    """
    Populate the database using the schema and populate SQL scripts.

    Args:
        conn (pymssql.Connection): The database connection.
        cursor (pymssql.Cursor): The database cursor.
    """
    schema_sql_file = "./sql/schema.sql"
    populate_sql_file = "./sql/populate.sql"

    print("[INFO] Executing schema SQL script...")
    _execute_sql_file(conn, cursor, schema_sql_file)
    print("[INFO] Schema SQL script execution complete")

    print("[INFO] Executing populate SQL script with batching...")
    _execute_sql_file(conn, cursor, populate_sql_file, with_batching=True)
    print("[INFO] Populate SQL script execution complete")


def _execute_sql_file(
    conn: pymssql.Connection, cursor: pymssql.Cursor, sql_file: str, with_batching: bool = False
) -> None:
    """
    Execute SQL statements from a file, optionally using batching.

    Args:
        conn (pymssql.Connection): The database connection.
        cursor (pymssql.Cursor): The database cursor.
        sql_file (str): The path to the SQL file.
        with_batching (bool): Whether to execute SQL statements in batches.
    """
    try:
        if with_batching:
            batch = []
            batch_counter = 0

            BATCH_LIMIT = 10000

            with open(sql_file, "r") as file:
                for line in file:
                    batch.append(line)

                    if len(batch) >= BATCH_LIMIT:
                        batch_counter += 1

                        sql_statements = "".join(batch)

                        print(f"[INFO] Executing batch {batch_counter} of SQL statements...")
                        cursor.execute(sql_statements)
                        conn.commit()
                        print(f"[INFO] Batch {batch_counter} execution complete")

                        batch = []

            if batch:
                batch_counter += 1

                sql_statements = "".join(batch)

                print(f"[INFO] Executing final batch {batch_counter} of SQL statements...")
                cursor.execute(sql_statements)
                conn.commit()
                print(f"[INFO] Final batch {batch_counter} execution complete")

        else:
            with open(sql_file, "r") as file:
                sql_statements = file.read()
                cursor.execute(sql_statements)
                conn.commit()

    except Exception as e:
        if conn:
            conn.rollback()

        print(f"[Error] {e}")

        sys.exit(1)


def _check_paths() -> None:
    paths = {
        "SQL Drop script": "./sql/drop.sql",
        "SQL Schema script": "./sql/schema.sql",
        "SQL Populate script": "./sql/populate.sql",
    }

    for name, path in paths.items():
        if not os.path.isfile(path):
            print(f"[Error] {name} path '{path}' is invalid or does not exist")
            print("[INFO] Exiting the setup script...")
            sys.exit(1)


if __name__ == "__main__":
    _check_paths()
    setup_db()
