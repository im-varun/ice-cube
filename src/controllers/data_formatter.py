# src/controllers/data_formatter.py
from datetime import datetime
from typing import Any


def format_column_name(column_name: str) -> str:
    """
    Convert column name from snake_case to Title Case without underscores.

    Args:
        column_name: Column name in snake_case format

    Returns:
        Formatted column name in Title Case with spaces
    """
    return column_name.replace("_", " ").title()


def format_date(date_str: str | None) -> str:
    """
    Convert date string to readable format.

    Args:
        date_str: Date string in format "YYYY-MM-DD"

    Returns:
        Formatted date string like "Month DD, YYYY" or original if parsing fails
    """
    if not date_str:
        return ""
    try:
        for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y"]:  # Multiple formats
            date_obj = datetime.strptime(str(date_str), fmt)
            return date_obj.strftime("%B %d, %Y")
    except (ValueError, TypeError):
        pass
    return str(date_str)


def format_datetime(datetime_str: str | None) -> str:
    """
    Convert datetime string to readable format.

    Args:
        datetime_str: Datetime string in format "YYYY-MM-DD HH:MM:SS"

    Returns:
        Formatted datetime string like "Month DD, YYYY at HH:MM AM/PM" or original if parsing fails
    """
    if not datetime_str:
        return ""
    try:
        for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M"]:  # Multiple formats
            dt_obj = datetime.strptime(str(datetime_str), fmt)
            return dt_obj.strftime("%B %d, %Y at %I:%M %p")
    except (ValueError, TypeError):
        pass
    return str(datetime_str)


def format_time(time_str: str | None) -> str:
    """
    Convert time string to readable format.

    Args:
        time_str: Time string in formats like "HH:MM:SS", "HH:MM", or "HHMMSS"

    Returns:
        Formatted time string like "HH:MM AM/PM" or original if parsing fails
    """
    if not time_str:
        return ""

    try:
        if isinstance(time_str, str):
            # Try common time formats
            for fmt in ["%H:%M:%S", "%H:%M", "%H%M%S"]:
                try:
                    time_obj = datetime.strptime(str(time_str), fmt)
                    return time_obj.strftime("%I:%M %p")
                except ValueError:
                    continue
    except (ValueError, TypeError):
        pass

    return str(time_str)


def format_game_id(game_id: int | None) -> str:
    """
    Format game ID to a readable date format.
    Game IDs are in format: YYYYSSGGG where:
    - YYYY = season year
    - SS = season type (02 = regular, 03 = playoffs)
    - GGG = game number

    Args:
        game_id: Game ID as integer (e.g., 2019030121)

    Returns:
        Formatted string like "2019 Playoffs Game 121" or original if invalid
    """
    if game_id is None:
        return ""

    try:
        game_id_str = str(game_id)
        if len(game_id_str) >= 10:
            year = game_id_str[:4]
            season_type = game_id_str[4:6]
            game_num = game_id_str[6:].lstrip("0") or "0"

            season_name = "Playoffs" if season_type == "03" else "Regular Season"
            return f"{year} {season_name} Game {game_num}"
    except (ValueError, TypeError):
        pass

    return str(game_id)


def format_duration(seconds: int | float | None) -> str:
    """
    Convert seconds to readable time format in words.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string like "2 hrs 46 mins 40 secs" or "46 mins 40 secs"
    """
    if seconds is None:
        return "0 mins"

    try:
        total_seconds = int(seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60

        parts = []
        if hours > 0:
            parts.append(f"{hours} hrs")
        if minutes > 0:
            parts.append(f"{minutes} mins")
        if secs > 0 or not parts:  # Show secs if no other parts, or always show secs
            parts.append(f"{secs} secs")

        return " ".join(parts)
    except (ValueError, TypeError):
        return str(seconds)


def transpose_single_result(
    data: dict[str, Any], field_names: list[str] | None = None
) -> list[dict[str, Any]]:
    """
    Convert single row result into multiple rows for vertical table display.

    Args:
        data: Single result dictionary
        field_names: Optional list of field names to include (if None, uses all fields)

    Returns:
        List of dictionaries where each dict represents a row with 'Field' and 'Value' columns
    """
    if not data:
        return [{"No Result": "No results found"}]

    result = []
    fields = field_names if field_names else data.keys()

    for field in fields:
        if field in data:
            # Convert field name from snake_case to Title Case
            display_name = format_column_name(field)
            result.append({"Field": display_name, "Value": data[field]})

    return result


def format_head_to_head(result: list[dict[str, Any]] | int) -> list[dict[str, Any]]:
    """
    Format head-to-head player comparison query results.

    Transforms the result from a single row with p1_* and p2_* columns
    into multiple rows with stats as rows and players as columns.

    Args:
        result: Query result from execute_headtohead

    Returns:
        List of dictionaries where each row is a stat with player values
    """
    if isinstance(result, int) or not result:
        return [
            {"No Result Found": "Please Recheck Player Spellings"},
            {"No Result Found": "Make Sure You Are Only Comparing 2 Skaters"},
        ]

    formatted_result = []
    data = result[0]

    # Extract stat names from p1_* keys
    stat_names = [key[3:] for key in data.keys() if key.startswith("p1_")]

    for stat in stat_names:
        player1_value = data.get(f"p1_{stat}")
        player2_value = data.get(f"p2_{stat}")
        formatted_result.append(
            {
                "Stats": format_column_name(stat),
                data.get("player_1"): player1_value,
                data.get("player_2"): player2_value,
            }
        )

    return formatted_result


def format_revenge_game_effect(result: list[dict[str, Any]] | int) -> list[dict[str, Any]]:
    """
    Format revenge game effect query results.

    Returns transposed view with Field and Value columns.
    """
    if isinstance(result, int) or not result:
        return [{"Error": "No results found"}]

    # Transpose single result
    formatted = result

    # Remove underscores from column names
    return [{format_column_name(k): v for k, v in row.items()} for row in formatted]


def format_home_rink_advantage(result: list[dict[str, Any]] | int) -> list[dict[str, Any]]:
    """
    Format home rink advantage query results.

    Returns transposed view with Field and Value columns.
    """
    if isinstance(result, int) or not result:
        return [{"Error": "No results found"}]

    data = result[0].copy()

    # Format percentage if present
    if "avg_faceoff_pct" in data and data["avg_faceoff_pct"] is not None:
        data["avg_faceoff_pct"] = f"{data['avg_faceoff_pct']:.1f}%"

    # formatted = transpose_single_result(data)
    formatted = result

    # Remove underscores from column names
    return [{format_column_name(k): v for k, v in row.items()} for row in formatted]


def format_birthday_curse(result: list[dict[str, Any]] | int) -> list[dict[str, Any]]:
    """
    Format birthday curse analysis query results.

    Returns transposed view with formatted dates.
    """
    if isinstance(result, int) or not result:
        return [{"Error": "No results found"}]

    formatted = []
    for row in result:
        data = row.copy()  # copy to modify safely
        if "birthDate" in data:
            data["Birth Date"] = format_date(data.pop("birthDate"))
        if "game_date" in data:
            data["Game Date"] = format_datetime(data.pop("game_date"))
        formatted.append(data)

    # Remove underscores from column names
    return [{format_column_name(k): v for k, v in row.items()} for row in formatted]


def format_most_penalized(result: list[dict[str, Any]] | int) -> list[dict[str, Any]]:
    """
    Format most penalized players query results.

    Returns list with formatted column names
    """
    if isinstance(result, int) or not result:
        return [{"Error": "No results found"}]

    # Remove underscores from column names
    return [{format_column_name(k): v for k, v in row.items()} for row in result]


def format_common_play_types(result: list[dict[str, Any]] | int) -> list[dict[str, Any]]:
    """
    Format most common play types query results.

    Returns list with formatted column names
    """
    if isinstance(result, int) or not result:
        return [{"Error": "No results found"}]

    # Remove underscores from column names
    return [{format_column_name(k): v for k, v in row.items()} for row in result]


def format_top_shooting_teams(result: list[dict[str, Any]] | int) -> list[dict[str, Any]]:
    """
    Format top shooting teams query results.

    Returns list with formatted column names
    """
    if isinstance(result, int) or not result:
        return [{"Error": "No results found"}]

    # Remove underscores from column names
    return [{format_column_name(k): v for k, v in row.items()} for row in result]


def format_longest_games(result: list[dict[str, Any]] | int) -> list[dict[str, Any]]:
    """
    Format longest games query results.

    Formats game_id and removes underscores from column names
    """
    if isinstance(result, int) or not result:
        return [{"Error": "No results found"}]

    formatted_result = []

    for row in result:
        formatted_row = {}
        for key, value in row.items():
            # Format game_id if present
            if key == "game_id":
                formatted_row["Game"] = format_game_id(value)
            else:
                formatted_row[format_column_name(key)] = value
        formatted_result.append(formatted_row)

    return formatted_result


def format_longest_avg_shift(result: list[dict[str, Any]] | int) -> list[dict[str, Any]]:
    """
    Format longest average shift query results.

    Converts duration fields from seconds to readable time format and removes underscores.
    """
    if isinstance(result, int) or not result:
        return [{"Error": "No results found"}]

    formatted_result = []

    for row in result:
        formatted_row = {}

        for key, value in row.items():
            # Format duration fields
            if key == "avg_shift_duration_seconds":
                formatted_row["Avg Shift Duration"] = format_duration(value)
            elif key == "longest_shift_seconds":
                formatted_row["Longest Shift"] = format_duration(value)
            elif key == "total_ice_time_seconds":
                formatted_row["Total Ice Time"] = format_duration(value)
            else:
                formatted_row[format_column_name(key)] = value

        formatted_result.append(formatted_row)

    return formatted_result


def format_most_assists(result: list[dict[str, Any]] | int) -> list[dict[str, Any]]:
    """
    Format most assists query results.

    Returns list with formatted column names
    """
    if isinstance(result, int) or not result:
        return [{"Error": "No results found"}]

    # Remove underscores from column names
    return [{format_column_name(k): v for k, v in row.items()} for row in result]


def format_top_scoring_players(result: list[dict[str, Any]] | int) -> list[dict[str, Any]]:
    """
    Format top scoring players query results.

    Returns list with formatted column names
    """
    if isinstance(result, int) or not result:
        return [{"Error": "No results found"}]

    # Remove underscores from column names
    return [{format_column_name(k): v for k, v in row.items()} for row in result]


def format_score_not_assist(result: list[dict[str, Any]] | int) -> list[dict[str, Any]]:
    """
    Format score but not assist query results.

    Returns list with formatted column names
    """
    if isinstance(result, int) or not result:
        return [{"Error": "No results found"}]

    # Remove underscores from column names
    return [{format_column_name(k): v for k, v in row.items()} for row in result]
