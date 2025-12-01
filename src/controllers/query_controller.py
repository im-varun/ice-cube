# src/controllers/query_controller.py
from typing import Any

from controllers import data_formatter
from database.query_engine import QueryEngine
from query_registry import Query
from ui.interfaces import ControllerInterface, UIRequest, UIResponse


def debug(data):
    import os

    DIR = os.path.dirname(__file__).split("ice-cube")[0]
    with open(DIR + "out.txt", "a") as f:
        f.write(str(data))


class QueryController(ControllerInterface):
    def __init__(self, query_engine: QueryEngine):
        self.query_engine = query_engine

    def handle_request(self, request: UIRequest) -> UIResponse:
        """
        Route requests from UI to appropriate database functions.

        Args:
            request: UIRequest object with action and payload

        Returns:
            UIResponse with success status, data, and message
        """
        action = request.action
        payload = request.payload or {}

        try:
            # Route to appropriate query method based on action
            if action == "custom":
                result = self._handle_custom_query(payload)
            elif action == Query.HEAD_TO_HEAD.value.id:
                result = self._handle_head_to_head(payload)
            elif action == Query.REVENGE_GAME_EFFECT.value.id:
                result = self._handle_revenge_game_effect()
            elif action == Query.HOME_RINK_ADVANTAGE.value.id:
                result = self._handle_home_rink_advantage()
            elif action == Query.BIRTHDAY_CURSE.value.id:
                result = self._handle_birthday_curse()
            elif action == Query.MOST_PENALIZED_TEAMS.value.id:
                result = self._handle_most_penalized()
            elif action == Query.PLAY_TYPES.value.id:
                result = self._handle_common_play_types()
            elif action == Query.TOP_SHOOTING_TEAMS.value.id:
                result = self._handle_top_shooting_teams()
            elif action == Query.MOST_ASSISTS.value.id:
                result = self._handle_most_assists()
            elif action == Query.LONGEST_GAMES.value.id:
                result = self._handle_longest_games()
            elif action == Query.LONGEST_AVG_SHIFT.value.id:
                result = self._handle_longest_avg_shift()
            elif action == Query.TOP_SCORING_PLAYERS.value.id:
                result = self._handle_top_scoring_players(payload)
            elif action == Query.LONE_WOLFS.value.id:
                result = self._handle_score_not_assist(payload)
            elif action == "refresh":
                result = self._handle_refresh_db()
            else:
                return UIResponse(success=False, message=f"Unknown action: {action}")

            # Check if query returned error code
            if result == 500:
                return UIResponse(success=False, message="Database error occurred")

            if not result:
                return UIResponse(success=False, message=f"Failed to execute {action}")

            return UIResponse(success=True, data=result, message=f"Successfully executed {action}")

        except Exception as e:
            return UIResponse(success=False, message=f"Error: {str(e)}")

    def _handle_custom_query(self, payload: dict[str, Any]) -> list[dict[str, Any]] | int:
        """Execute a custom SQL query"""
        query = payload.get("query", "")
        return self.query_engine.execute_query(query)

    def _handle_head_to_head(self, payload: dict[str, Any]) -> list[dict[str, Any]] | int:
        """Execute head-to-head player comparison"""
        player1_name = f"{payload.get('Player_1')} ".split(" ", 1)
        player2_name = f"{payload.get('Player_2')} ".split(" ", 1)
        result = self.query_engine.execute_headtohead(
            player1_firstname=player1_name[0],
            player1_lastname=player1_name[1],
            player2_firstname=player2_name[0],
            player2_lastname=player2_name[1],
        )
        return data_formatter.format_head_to_head(result)

    def _handle_revenge_game_effect(self) -> list[dict[str, Any]] | int:
        """Execute revenge game effect query"""
        result = self.query_engine.execute_revengegameeffect()
        return data_formatter.format_revenge_game_effect(result)

    def _handle_home_rink_advantage(self) -> list[dict[str, Any]] | int:
        """Execute home rink advantage query"""
        result = self.query_engine.execute_homerinksideadvantage()
        return data_formatter.format_home_rink_advantage(result)

    def _handle_birthday_curse(self) -> list[dict[str, Any]] | int:
        """Execute birthday curse analysis query"""
        result = self.query_engine.execute_birthdaycurseanalysis()
        return data_formatter.format_birthday_curse(result)

    def _handle_most_penalized(self) -> list[dict[str, Any]] | int:
        """Get most penalized players"""
        result = self.query_engine.execute_mostpenalizedplayers()
        return data_formatter.format_most_penalized(result)

    def _handle_common_play_types(self) -> list[dict[str, Any]] | int:
        """Get most common play types"""
        result = self.query_engine.execute_mostcommonplaytypes()
        return data_formatter.format_common_play_types(result)

    def _handle_top_shooting_teams(self) -> list[dict[str, Any]] | int:
        """Get top shooting teams"""
        result = self.query_engine.execute_topshootingteams()
        return data_formatter.format_top_shooting_teams(result)

    def _handle_most_assists(self) -> list[dict[str, Any]] | int:
        """Get players with most assists"""
        result = self.query_engine.execute_playerswithmostassists()
        return data_formatter.format_most_assists(result)

    def _handle_longest_games(self) -> list[dict[str, Any]] | int:
        """Get longest games"""
        result = self.query_engine.execute_longestgames()
        return data_formatter.format_longest_games(result)

    def _handle_longest_avg_shift(self) -> list[dict[str, Any]] | int:
        """Get players with longest average shift"""
        result = self.query_engine.execute_playerswithlongestavgshift()
        return data_formatter.format_longest_avg_shift(result)

    def _handle_top_scoring_players(self, payload: dict[str, Any]) -> list[dict[str, Any]] | int:
        """Get top scoring players with filters"""
        result = self.query_engine.execute_topscoringplayers(
            penalty_threshold=payload.get("penalty_threshold", 10),
            minimum_goals=payload.get("minimum_goals", 5),
            limit_rows=payload.get("limit_rows", 10),
        )
        return data_formatter.format_top_scoring_players(result)

    def _handle_score_not_assist(self, payload: dict[str, Any]) -> list[dict[str, Any]] | int:
        """Get players who score but don't assist"""
        result = self.query_engine.execute_playerswhoscorebutnotassist(
            minimum_goals=payload.get("minimum_goals", 5), limit_rows=payload.get("limit_rows", 10)
        )
        return data_formatter.format_score_not_assist(result)

    def _handle_refresh_db(self) -> None | int:
        """Refresh the database"""
        return self.query_engine.execute_refreshdb()
