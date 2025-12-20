"""
Tests for data_formatter - query result formatting utilities.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from controllers.data_formatter import (
    format_column_name,
    format_date,
    format_datetime,
    format_duration,
    format_game_id,
    format_time,
    transpose_single_result,
)


class TestFormatColumnName:
    """Tests for column name formatting."""

    def test_snake_case_to_title(self):
        """Should convert snake_case to Title Case."""
        assert format_column_name("player_name") == "Player Name"
        assert format_column_name("total_goals") == "Total Goals"

    def test_single_word(self):
        """Single words should be titlecased."""
        assert format_column_name("goals") == "Goals"

    def test_multiple_underscores(self):
        """Multiple underscores should all be replaced."""
        assert format_column_name("avg_shift_duration_seconds") == "Avg Shift Duration Seconds"


class TestFormatDate:
    """Tests for date formatting."""

    def test_standard_date_format(self):
        """Should format YYYY-MM-DD correctly."""
        assert format_date("2020-01-15") == "January 15, 2020"

    def test_empty_date(self):
        """Empty or None dates should return empty string."""
        assert format_date("") == ""
        assert format_date(None) == ""

    def test_invalid_date_returns_original(self):
        """Invalid dates should return original string."""
        assert format_date("not-a-date") == "not-a-date"


class TestFormatDatetime:
    """Tests for datetime formatting."""

    def test_standard_datetime(self):
        """Should format datetime correctly."""
        result = format_datetime("2020-01-15 19:30:00")
        assert "January 15, 2020" in result
        assert "07:30 PM" in result

    def test_empty_datetime(self):
        """Empty datetime returns empty string."""
        assert format_datetime("") == ""
        assert format_datetime(None) == ""


class TestFormatTime:
    """Tests for time formatting."""

    def test_standard_time(self):
        """Should convert 24h to 12h format."""
        assert format_time("19:30:00") == "07:30 PM"

    def test_morning_time(self):
        """Morning times should show AM."""
        assert format_time("09:15:00") == "09:15 AM"

    def test_empty_time(self):
        """Empty time returns empty string."""
        assert format_time("") == ""
        assert format_time(None) == ""


class TestFormatGameId:
    """Tests for game ID formatting."""

    def test_playoff_game_id(self):
        """Playoff game IDs should format correctly."""
        result = format_game_id(2019030121)
        assert "2019" in result
        assert "Playoffs" in result
        assert "121" in result

    def test_regular_season_game_id(self):
        """Regular season game IDs should format correctly."""
        result = format_game_id(2019020001)
        assert "2019" in result
        assert "Regular Season" in result

    def test_none_game_id(self):
        """None game IDs should return empty string."""
        assert format_game_id(None) == ""


class TestFormatDuration:
    """Tests for duration formatting."""

    def test_hours_minutes_seconds(self):
        """Should format full duration correctly."""
        result = format_duration(10000)  # 2h 46m 40s
        assert "2 hrs" in result
        assert "46 mins" in result
        assert "40 secs" in result

    def test_minutes_only(self):
        """Minutes without hours should work."""
        result = format_duration(120)  # 2 minutes
        assert "2 mins" in result
        assert "hrs" not in result

    def test_seconds_only(self):
        """Small durations should show seconds."""
        result = format_duration(45)
        assert "45 secs" in result

    def test_none_duration(self):
        """None should return '0 mins'."""
        assert format_duration(None) == "0 mins"


class TestTransposeSingleResult:
    """Tests for result transposition."""

    def test_basic_transpose(self):
        """Should transpose dict to Field/Value rows."""
        data = {"goals": 50, "assists": 67}
        result = transpose_single_result(data)
        assert len(result) == 2
        assert any(r["Field"] == "Goals" for r in result)

    def test_empty_data(self):
        """Empty data should return 'No results' message."""
        result = transpose_single_result({})
        assert "No Result" in str(result)

    def test_field_name_formatting(self):
        """Field names should be formatted."""
        data = {"player_name": "Sidney Crosby"}
        result = transpose_single_result(data)
        assert result[0]["Field"] == "Player Name"


class TestQueryFormatters:
    """Tests for query-specific formatters."""

    def test_format_head_to_head_error(self):
        """Error results should return helpful message."""
        from controllers.data_formatter import format_head_to_head

        result = format_head_to_head(500)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_format_revenge_game_error(self):
        """Error results should be handled."""
        from controllers.data_formatter import format_revenge_game_effect

        result = format_revenge_game_effect(500)
        assert "Error" in str(result)

    def test_format_home_rink_error(self):
        """Error results should be handled."""
        from controllers.data_formatter import format_home_rink_advantage

        result = format_home_rink_advantage([])
        assert "Error" in str(result)

    def test_format_birthday_curse_error(self):
        """Error results should be handled."""
        from controllers.data_formatter import format_birthday_curse

        result = format_birthday_curse(500)
        assert "Error" in str(result)

    def test_format_most_penalized_error(self):
        """Error results should be handled."""
        from controllers.data_formatter import format_most_penalized

        result = format_most_penalized([])
        assert "Error" in str(result)

    def test_format_common_play_types_error(self):
        """Error results should be handled."""
        from controllers.data_formatter import format_common_play_types

        result = format_common_play_types(500)
        assert "Error" in str(result)

    def test_format_top_shooting_teams_error(self):
        """Error results should be handled."""
        from controllers.data_formatter import format_top_shooting_teams

        result = format_top_shooting_teams([])
        assert "Error" in str(result)

    def test_format_longest_games_error(self):
        """Error results should be handled."""
        from controllers.data_formatter import format_longest_games

        result = format_longest_games(500)
        assert "Error" in str(result)

    def test_format_longest_avg_shift_error(self):
        """Error results should be handled."""
        from controllers.data_formatter import format_longest_avg_shift

        result = format_longest_avg_shift([])
        assert "Error" in str(result)

    def test_format_most_assists_error(self):
        """Error results should be handled."""
        from controllers.data_formatter import format_most_assists

        result = format_most_assists(500)
        assert "Error" in str(result)

    def test_format_top_scoring_players_error(self):
        """Error results should be handled."""
        from controllers.data_formatter import format_top_scoring_players

        result = format_top_scoring_players([])
        assert "Error" in str(result)

    def test_format_score_not_assist_error(self):
        """Error results should be handled."""
        from controllers.data_formatter import format_score_not_assist

        result = format_score_not_assist(500)
        assert "Error" in str(result)
