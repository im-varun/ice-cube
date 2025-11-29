import os
import sys
import warnings

import pandas as pd

_RAW_DATA_DIR: str = "./data/raw/"
_CLEANED_DATA_DIR: str = "./data/clean/"

_game_ids_removed: set = set()
_play_ids_removed: set = set()

_SEASONS_TO_REMOVE: list = [
    "2000-2001",
    "2001-2002",
    "2002-2003",
    "2003-2004",
    "2004-2005",
    "2005-2006",
    "2006-2007",
    "2007-2008",
    "2008-2009",
    "2009-2010",
    "2010-2011",
    "2011-2012",
    "2012-2013",
    "2013-2014",
    "2014-2015",
    "2015-2016",
    "2016-2017",
    "2017-2018",
    "2018-2019",
]

warnings.simplefilter(action="ignore", category=pd.errors.DtypeWarning)


def cleaning_pipeline() -> None:
    """
    Main data cleaning pipeline that processes all raw CSV files and saves cleaned versions.
    """
    _clean_game_csv()
    _clean_team_info_csv()
    _clean_player_info_csv()
    _clean_game_officials_csv()
    _clean_game_plays_csv()
    _clean_game_goals_csv()
    _clean_game_penalties_csv()
    _clean_game_plays_players_csv()
    _clean_game_shifts_csv()
    _clean_game_teams_stats_csv()
    _clean_game_skater_stats_csv()
    _clean_game_goalie_stats_csv()
    _clean_game_scratches_csv()


def _clean_game_csv() -> None:
    """
    Cleans the game.csv file by formatting seasons, removing unwanted columns,
    and filtering out specific seasons.
    """
    print("[INFO] Cleaning game.csv...")

    global _game_ids_removed

    filename = "game.csv"

    raw_filepath = os.path.join(_RAW_DATA_DIR, filename)

    df = pd.read_csv(raw_filepath)

    df["season"] = df["season"].astype(str).apply(lambda x: f"{x[:4]}-{x[4:]}")

    drop_columns = [
        "venue_link",
        "venue_time_zone_id",
        "venue_time_zone_offset",
        "venue_time_zone_tz",
    ]
    df = df.drop(columns=drop_columns)

    game_ids_to_remove = df.loc[df["season"].isin(_SEASONS_TO_REMOVE), "game_id"].tolist()
    _game_ids_removed.update(game_ids_to_remove)

    df = df[~df["season"].isin(_SEASONS_TO_REMOVE)]

    df["date_time_GMT"] = df["date_time_GMT"].astype(str).str.replace("T", " ").str.replace("Z", "")

    df = df.drop_duplicates()

    cleaned_filepath = os.path.join(_CLEANED_DATA_DIR, filename)
    df.to_csv(cleaned_filepath, index=False, na_rep="NULL")

    print("[INFO] Finished cleaning game.csv")
    print(f"[INFO] Saved cleaned file to {cleaned_filepath}")


def _clean_team_info_csv() -> None:
    """
    Cleans the team_info.csv file by removing unwanted columns and duplicates.
    """
    print("[INFO] Cleaning team_info.csv...")

    filename = "team_info.csv"

    raw_filepath = os.path.join(_RAW_DATA_DIR, filename)

    df = pd.read_csv(raw_filepath)

    drop_columns = ["franchiseId", "link"]
    df = df.drop(columns=drop_columns)

    df = df.drop_duplicates()

    cleaned_filepath = os.path.join(_CLEANED_DATA_DIR, filename)
    df.to_csv(cleaned_filepath, index=False, na_rep="NULL")

    print("[INFO] Finished cleaning team_info.csv")
    print(f"[INFO] Saved cleaned file to {cleaned_filepath}")


def _clean_player_info_csv() -> None:
    """
    Cleans the player_info.csv file by removing unwanted columns, formatting dates,
    handling missing values, and removing duplicates.
    """
    print("[INFO] Cleaning player_info.csv...")

    filename = "player_info.csv"

    raw_filepath = os.path.join(_RAW_DATA_DIR, filename)

    df = pd.read_csv(raw_filepath)

    drop_columns = ["height_cm"]
    df = df.drop(columns=drop_columns)

    df["birthDate"] = df["birthDate"].astype(str).str.replace("T", " ").str.replace("Z", "")

    df["weight"] = df["weight"].fillna(0).astype(int)

    df = df.drop_duplicates()

    cleaned_filepath = os.path.join(_CLEANED_DATA_DIR, filename)
    df.to_csv(cleaned_filepath, index=False, na_rep="NULL")

    print("[INFO] Finished cleaning player_info.csv")
    print(f"[INFO] Saved cleaned file to {cleaned_filepath}")


def _clean_game_scratches_csv() -> None:
    """
    Cleans the game_scratches.csv file by removing entries related to removed games
    and duplicates.
    """
    print("[INFO] Cleaning game_scratches.csv...")

    filename = "game_scratches.csv"

    raw_filepath = os.path.join(_RAW_DATA_DIR, filename)

    df = pd.read_csv(raw_filepath)

    df = df[~df["game_id"].isin(_game_ids_removed)]

    df = df.drop_duplicates()

    cleaned_filepath = os.path.join(_CLEANED_DATA_DIR, filename)
    df.to_csv(cleaned_filepath, index=False, na_rep="NULL")

    print("[INFO] Finished cleaning game_scratches.csv")
    print(f"[INFO] Saved cleaned file to {cleaned_filepath}")


def _clean_game_officials_csv() -> None:
    """
    Cleans the game_officials.csv file by removing entries related to removed games
    and duplicates.
    """
    print("[INFO] Cleaning game_officials.csv...")

    filename = "game_officials.csv"

    raw_filepath = os.path.join(_RAW_DATA_DIR, filename)

    df = pd.read_csv(raw_filepath)

    df = df[~df["game_id"].isin(_game_ids_removed)]

    df = df.drop_duplicates()

    cleaned_filepath = os.path.join(_CLEANED_DATA_DIR, filename)
    df.to_csv(cleaned_filepath, index=False, na_rep="NULL")

    print("[INFO] Finished cleaning game_officials.csv")
    print(f"[INFO] Saved cleaned file to {cleaned_filepath}")


def _clean_game_plays_csv() -> None:
    """
    Cleans the game_plays.csv file by removing entries related to removed games,
    handling missing values, formatting dateTime, and removing duplicates.
    """
    print("[INFO] Cleaning game_plays.csv...")

    global _play_ids_removed

    filename = "game_plays.csv"

    raw_filepath = os.path.join(_RAW_DATA_DIR, filename)

    df = pd.read_csv(raw_filepath)

    play_ids_to_remove = df.loc[df["game_id"].isin(_game_ids_removed), "play_id"].tolist()
    _play_ids_removed.update(play_ids_to_remove)

    df = df[~df["game_id"].isin(_game_ids_removed)]

    df["team_id_for"] = df["team_id_for"].fillna(0).astype(int)
    df["team_id_against"] = df["team_id_against"].fillna(0).astype(int)

    df["x"] = df["x"].fillna(0)
    df["y"] = df["y"].fillna(0)
    df["st_x"] = df["st_x"].fillna(0)
    df["st_y"] = df["st_y"].fillna(0)

    df["dateTime"] = df["dateTime"].astype(str).str.replace("T", " ").str.replace("Z", "")

    df = df.drop_duplicates()

    cleaned_filepath = os.path.join(_CLEANED_DATA_DIR, filename)
    df.to_csv(cleaned_filepath, index=False, na_rep="NULL")

    print("[INFO] Finished cleaning game_plays.csv")
    print(f"[INFO] Saved cleaned file to {cleaned_filepath}")


def _clean_game_goals_csv() -> None:
    """
    Cleans the game_goals.csv file by removing entries related to removed plays,
    removing duplicates, and adding a unique identifier for each goal.
    """
    print("[INFO] Cleaning game_goals.csv...")

    filename = "game_goals.csv"

    raw_filepath = os.path.join(_RAW_DATA_DIR, filename)

    df = pd.read_csv(raw_filepath)

    df = df[~df["play_id"].isin(_play_ids_removed)]

    df = df.drop_duplicates()

    df.insert(0, "game_goal_id", range(1, len(df) + 1))

    cleaned_filepath = os.path.join(_CLEANED_DATA_DIR, filename)
    df.to_csv(cleaned_filepath, index=False, na_rep="NULL")

    print("[INFO] Finished cleaning game_goals.csv")
    print(f"[INFO] Saved cleaned file to {cleaned_filepath}")


def _clean_game_penalties_csv() -> None:
    """
    Cleans the game_penalties.csv file by removing entries related to removed plays
    and duplicates.
    """
    print("[INFO] Cleaning game_penalties.csv...")

    filename = "game_penalties.csv"

    raw_filepath = os.path.join(_RAW_DATA_DIR, filename)

    df = pd.read_csv(raw_filepath)

    df = df[~df["play_id"].isin(_play_ids_removed)]

    df = df.drop_duplicates()

    cleaned_filepath = os.path.join(_CLEANED_DATA_DIR, filename)
    df.to_csv(cleaned_filepath, index=False, na_rep="NULL")

    print("[INFO] Finished cleaning game_penalties.csv")
    print(f"[INFO] Saved cleaned file to {cleaned_filepath}")


def _clean_game_plays_players_csv() -> None:
    """
    Cleans the game_plays_players.csv file by removing entries related to removed plays
    and duplicates.
    """
    print("[INFO] Cleaning game_plays_players.csv...")

    filename = "game_plays_players.csv"

    raw_filepath = os.path.join(_RAW_DATA_DIR, filename)

    df = pd.read_csv(raw_filepath)

    df = df[~df["game_id"].isin(_game_ids_removed)]

    df = df.drop_duplicates()

    cleaned_filepath = os.path.join(_CLEANED_DATA_DIR, filename)
    df.to_csv(cleaned_filepath, index=False, na_rep="NULL")

    print("[INFO] Finished cleaning game_plays_players.csv")
    print(f"[INFO] Saved cleaned file to {cleaned_filepath}")


def _clean_game_shifts_csv() -> None:
    """
    Cleans the game_shifts.csv file by removing entries related to removed games,
    handling missing shift_end values, and removing duplicates.
    """
    print("[INFO] Cleaning game_shifts.csv...")

    filename = "game_shifts.csv"

    raw_filepath = os.path.join(_RAW_DATA_DIR, filename)

    df = pd.read_csv(raw_filepath)

    df = df[~df["game_id"].isin(_game_ids_removed)]

    df["shift_end"] = df.apply(
        lambda row: row["shift_start"] + 1 if pd.isna(row["shift_end"]) else row["shift_end"],
        axis=1,
    )
    df["shift_end"] = df["shift_end"].astype(int)

    df = df.drop_duplicates()

    cleaned_filepath = os.path.join(_CLEANED_DATA_DIR, filename)
    df.to_csv(cleaned_filepath, index=False, na_rep="NULL")

    print("[INFO] Finished cleaning game_shifts.csv")
    print(f"[INFO] Saved cleaned file to {cleaned_filepath}")


def _clean_game_teams_stats_csv() -> None:
    """
    Cleans the game_teams_stats.csv file by removing entries related to removed games
    and duplicates.
    """
    print("[INFO] Cleaning game_teams_stats.csv...")

    filename = "game_teams_stats.csv"

    raw_filepath = os.path.join(_RAW_DATA_DIR, filename)

    df = pd.read_csv(raw_filepath)

    df = df[~df["game_id"].isin(_game_ids_removed)]

    df = df.drop_duplicates()

    cleaned_filepath = os.path.join(_CLEANED_DATA_DIR, filename)
    df.to_csv(cleaned_filepath, index=False, na_rep="NULL")

    print("[INFO] Finished cleaning game_teams_stats.csv")
    print(f"[INFO] Saved cleaned file to {cleaned_filepath}")


def _clean_game_skater_stats_csv() -> None:
    """
    Cleans the game_skater_stats.csv file by removing entries related to removed games
    and duplicates.
    """
    print("[INFO] Cleaning game_skater_stats.csv...")

    filename = "game_skater_stats.csv"

    raw_filepath = os.path.join(_RAW_DATA_DIR, filename)

    df = pd.read_csv(raw_filepath)

    df = df[~df["game_id"].isin(_game_ids_removed)]

    df = df.drop_duplicates()

    cleaned_filepath = os.path.join(_CLEANED_DATA_DIR, filename)
    df.to_csv(cleaned_filepath, index=False, na_rep="NULL")

    print("[INFO] Finished cleaning game_skater_stats.csv")
    print(f"[INFO] Saved cleaned file to {cleaned_filepath}")


def _clean_game_goalie_stats_csv() -> None:
    """
    Cleans the game_goalie_stats.csv file by removing entries related to removed games
    and duplicates.
    """
    print("[INFO] Cleaning game_goalie_stats.csv...")

    filename = "game_goalie_stats.csv"

    raw_filepath = os.path.join(_RAW_DATA_DIR, filename)

    df = pd.read_csv(raw_filepath)

    df = df[~df["game_id"].isin(_game_ids_removed)]

    df = df.drop_duplicates()

    cleaned_filepath = os.path.join(_CLEANED_DATA_DIR, filename)
    df.to_csv(cleaned_filepath, index=False, na_rep="NULL")

    print("[INFO] Finished cleaning game_goalie_stats.csv")
    print(f"[INFO] Saved cleaned file to {cleaned_filepath}")


def _check_paths() -> None:
    paths = {"Raw data directory": _RAW_DATA_DIR, "Cleaned data directory": _CLEANED_DATA_DIR}

    for name, path in paths.items():
        if not os.path.isdir(path):
            print(f"[Error] {name} path '{path}' is invalid or does not exist")

            if name == "Cleaned data directory":
                print(f"[INFO] Creating cleaned data directory at '{path}'")
                os.makedirs(path)
                print(f"[INFO] Created cleaned data directory at '{path}'")

            else:
                print("[INFO] Exiting the script...")
                sys.exit(1)


if __name__ == "__main__":
    _check_paths()

    print("[INFO] Starting data cleaning pipeline...")
    cleaning_pipeline()
    print("[INFO] Data cleaning pipeline completed")

    print("[INFO] Exiting the script...")
