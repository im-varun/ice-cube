# src/controllers/query_controller.py
from database.query_engine import QueryEngine
from ui.interfaces import ControllerInterface, UIRequest, UIResponse
from typing import Any
from query_registry import QUERIES


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
            # Route to appropriate query method based on action
            if action == "execute_custom_query":
                result = self._handle_custom_query(payload)
            elif action == "head_to_head":
                result = self._handle_head_to_head(payload)
            elif action == "revenge_game_effect":
                result = self._handle_revenge_game_effect()
            elif action == "home_rink_advantage":
                result = self._handle_home_rink_advantage()
            elif action == "birthday_curse":
                result = self._handle_birthday_curse()
            elif action == "penalized_teams":
                result = self._handle_most_penalized()
            elif action == "play_types":
                result = self._handle_common_play_types()
            elif action == "top_shooting_teams":
                result = self._handle_top_shooting_teams()
            elif action == "most_assists":
                result = self._handle_most_assists()
            elif action == "longest_games":
                result = self._handle_longest_games()
            elif action == "longest_avg_shift":
                result = self._handle_longest_avg_shift()
            elif action == "top_scoring":
                result = self._handle_top_scoring_players(payload)
            elif action == "score_not_assist":
                result = self._handle_score_not_assist(payload)
            elif action == "refresh_db":
                result = self._handle_refresh_db()
            else:
                return UIResponse(
                    success=False,
                    message=f"Unknown action: {action}"
                )
            
            # Check if query returned error code
            if result == 500:
                return UIResponse(
                    success=False,
                    message="Database error occurred"
                )
            
            return UIResponse(
                success=True,
                data=result,
                message=f"Successfully executed {action}"
            )
            
        except Exception as e:
            return UIResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
    
    def _handle_custom_query(self, payload: dict[str, Any]) -> list[dict[str, Any]] | int:
        """Execute a custom SQL query"""
        query = payload.get("query", "")
        return self.query_engine.execute_query(query)
    
    def _handle_head_to_head(self, payload: dict[str, Any]) -> list[dict[str, Any]] | int:
        """Execute head-to-head player comparison"""
        return self.query_engine.execute_headtohead(
            player1_firstname=payload.get("player1_firstname"),
            player1_lastname=payload.get("player1_lastname"),
            player2_firstname=payload.get("player2_firstname"),
            player2_lastname=payload.get("player2_lastname")
        )
    
    def _handle_revenge_game_effect(self) -> list[dict[str, Any]] | int:
        """Execute revenge game effect query"""
        return self.query_engine.execute_revengegameeffect()
    
    def _handle_home_rink_advantage(self) -> list[dict[str, Any]] | int:
        """Execute home rink advantage query"""
        return self.query_engine.execute_homerinksideadvantage()
    
    def _handle_birthday_curse(self) -> list[dict[str, Any]] | int:
        """Execute birthday curse analysis query"""
        return self.query_engine.execute_birthdaycurseanalysis()
    
    def _handle_most_penalized(self) -> list[dict[str, Any]] | int:
        """Get most penalized players"""
        return self.query_engine.execute_mostpenalizedplayers()
    
    def _handle_common_play_types(self) -> list[dict[str, Any]] | int:
        """Get most common play types"""
        return self.query_engine.execute_mostcommonplaytypes()
    
    def _handle_top_shooting_teams(self) -> list[dict[str, Any]] | int:
        """Get top shooting teams"""
        return self.query_engine.execute_topshootingteams()
    
    def _handle_most_assists(self) -> list[dict[str, Any]] | int:
        """Get players with most assists"""
        return self.query_engine.execute_playerswithmostassists()
    
    def _handle_longest_games(self) -> list[dict[str, Any]] | int:
        """Get longest games"""
        return self.query_engine.execute_longestgames()
    
    def _handle_longest_avg_shift(self) -> list[dict[str, Any]] | int:
        """Get players with longest average shift"""
        return self.query_engine.execute_playerswithlongestavgshift()
    
    def _handle_top_scoring_players(self, payload: dict[str, Any]) -> list[dict[str, Any]] | int:
        """Get top scoring players with filters"""
        return self.query_engine.execute_topscoringplayers(
            penalty_threshold=payload.get("penalty_threshold", 10),
            minimum_goals=payload.get("minimum_goals", 5),
            limit_rows=payload.get("limit_rows", 10)
        )
    
    def _handle_score_not_assist(self, payload: dict[str, Any]) -> list[dict[str, Any]] | int:
        """Get players who score but don't assist"""
        return self.query_engine.execute_playerswhoscorebutnotassist(
            minimum_goals=payload.get("minimum_goals", 5),
            limit_rows=payload.get("limit_rows", 10)
        )
    
    def _handle_refresh_db(self) -> None | int:
        """Refresh the database"""
        return self.query_engine.execute_refreshdb()
