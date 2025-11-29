import os
import sys

import pandas as pd

_CLEANED_DATA_DIR: str = "./data/clean/"
_SQL_DIR: str = "./sql/"


def csv_to_sql_pipeline() -> None:
    """
    Main pipeline function to convert CSV files to SQL insert statements.
    """
    _csv_to_sql("game.csv")
    _csv_to_sql("game_goalie_stats.csv")
    _csv_to_sql("game_goals.csv")
    _csv_to_sql("game_officials.csv")
    _csv_to_sql("game_penalties.csv")
    _csv_to_sql("game_plays.csv")
    _csv_to_sql("game_plays_players.csv")
    _csv_to_sql("game_scratches.csv")
    _csv_to_sql("game_shifts.csv")
    _csv_to_sql("game_skater_stats.csv")
    _csv_to_sql("game_teams_stats.csv")
    _csv_to_sql("player_info.csv")
    _csv_to_sql("team_info.csv")


def _csv_to_sql(filename: str) -> None:
    """
    Converts a single CSV file to SQL insert statements and appends them to a SQL file.

    Args:
        filename (str): The name of the CSV file to convert.
    """
    print(f"[INFO] Converting {filename} to SQL insert statements...")

    table_name = filename.replace(".csv", "")

    filepath = os.path.join(_CLEANED_DATA_DIR, filename)

    df = pd.read_csv(filepath, na_filter=False)

    sql_filepath = os.path.join(_SQL_DIR, "populate.sql")

    columns = df.columns.tolist()

    with open(sql_filepath, "a") as sql_file:
        for _, row in df.iterrows():
            values = ", ".join(_sql_safe_string(row[column]) for column in columns)
            sql_file.write(f"INSERT INTO {table_name} VALUES ({values});\n")

    print(f"[INFO] Finished converting {filename} to SQL insert statements")


def _sql_safe_string(value: str) -> str:
    """
    Converts a value to a SQL-safe string representation.

    Args:
        value (str): The value to convert.

    Returns:
        str: The SQL-safe string representation of the value.
    """
    if pd.isna(value) or value == "NULL":
        return "NULL"

    if isinstance(value, bool):
        return f"'{value}'"

    if isinstance(value, str):
        return f"'{value.replace("'", "''")}'"

    return str(value)


def _check_paths() -> None:
    paths = {"Cleaned data directory": _CLEANED_DATA_DIR, "SQL directory": _SQL_DIR}

    for name, path in paths.items():
        if not os.path.isdir(path):
            print(f"[Error] {name} path '{path}' is invalid or does not exist")
            print("[INFO] Exiting the script...")
            sys.exit(1)


if __name__ == "__main__":
    _check_paths()

    if os.path.isfile(os.path.join(_SQL_DIR, "populate.sql")):
        os.remove(os.path.join(_SQL_DIR, "populate.sql"))

    print("[INFO] Starting CSV to SQL pipeline...")
    csv_to_sql_pipeline()
    print("[INFO] CSV to SQL pipeline completed")

    print("[INFO] Exiting the script...")
