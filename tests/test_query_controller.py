"""
Tests for QueryController - business logic layer.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from controllers.query_controller import QueryController
from ui.interfaces import UIRequest


class MockQueryEngine:
    """Mock query engine for testing without database."""

    def execute_headtohead(self, **kwargs):
        return [
            {
                "player_1": "Connor McDavid",
                "player_2": "Sidney Crosby",
                "p1_goals": 50,
                "p2_goals": 35,
                "p1_assists": 67,
                "p2_assists": 60,
            }
        ]

    def execute_birthdaycurseanalysis(self):
        return [{"player": "Test Player", "birthday_goals": 1}]

    def execute_revengegameeffect(self):
        return [{"effect": "positive", "games": 10}]

    def execute_homerinksideadvantage(self):
        return [{"advantage": 5.5, "avg_faceoff_pct": 52.3}]

    def execute_mostpenalizedplayers(self):
        return [{"player": "Test", "penalty_minutes": 200}]

    def execute_mostcommonplaytypes(self):
        return [{"play_type": "Wrist Shot", "count": 1000}]

    def execute_topshootingteams(self):
        return [{"team": "Test Team", "shots": 3000}]

    def execute_playerswithmostassists(self):
        return [{"player": "Test", "assists": 100}]

    def execute_longestgames(self):
        return [{"game_id": 2019030121, "duration": 200}]

    def execute_playerswithlongestavgshift(self):
        return [{"player": "Test", "avg_shift_duration_seconds": 60}]

    def execute_topscoringplayers(self, **kwargs):
        return [{"player": "Test", "goals": 50}]

    def execute_playerswhoscorebutnotassist(self, **kwargs):
        return [{"player": "Test", "goals": 10, "assists": 0}]

    def execute_query(self, query):
        return [{"result": "test"}]

    def execute_refreshdb(self):
        return None


class TestQueryControllerInit:
    """Tests for QueryController initialization."""

    def test_controller_init(self):
        """Controller should initialize with query engine."""
        engine = MockQueryEngine()
        controller = QueryController(engine)
        assert controller.query_engine == engine
        assert controller.firewall is not None


class TestQueryControllerSecurity:
    """Tests for SQL injection protection in controller."""

    def test_blocks_sql_injection(self):
        """Should block SQL injection attempts."""
        controller = QueryController(MockQueryEngine())
        request = UIRequest(
            action="custom",
            payload={"query": "SELECT * FROM users; DROP TABLE users"},
        )
        response = controller.handle_request(request)
        assert response.success is False
        assert "SQL injection" in response.message

    def test_allows_safe_payload(self):
        """Should allow safe payloads through."""
        controller = QueryController(MockQueryEngine())
        request = UIRequest(
            action="birthday_curse",
            payload={},
        )
        response = controller.handle_request(request)
        assert response.success is True


class TestQueryControllerRouting:
    """Tests for request routing to correct handlers."""

    def test_routes_head_to_head(self):
        """Should route head_to_head action correctly."""
        controller = QueryController(MockQueryEngine())
        request = UIRequest(
            action="head_to_head",
            payload={"Player_1": "Connor McDavid", "Player_2": "Sidney Crosby"},
        )
        response = controller.handle_request(request)
        assert response.success is True
        assert response.data is not None

    def test_routes_birthday_curse(self):
        """Should route birthday_curse action."""
        controller = QueryController(MockQueryEngine())
        request = UIRequest(action="birthday_curse", payload={})
        response = controller.handle_request(request)
        assert response.success is True

    def test_routes_revenge_game(self):
        """Should route revenge_game_effect action."""
        controller = QueryController(MockQueryEngine())
        request = UIRequest(action="revenge_game_effect", payload={})
        response = controller.handle_request(request)
        assert response.success is True

    def test_routes_home_rink(self):
        """Should route home_rink_advantage action."""
        controller = QueryController(MockQueryEngine())
        request = UIRequest(action="home_rink_advantage", payload={})
        response = controller.handle_request(request)
        assert response.success is True

    def test_unknown_action_fails(self):
        """Unknown actions should return error."""
        controller = QueryController(MockQueryEngine())
        request = UIRequest(action="not_real_action", payload={})
        response = controller.handle_request(request)
        assert response.success is False
        assert "Unknown action" in response.message


class TestQueryControllerHelpers:
    """Tests for helper methods."""

    def test_to_pos_int_valid(self):
        """Should convert valid positive int."""
        controller = QueryController(MockQueryEngine())
        assert controller._to_pos_int("10", 5) == 10
        assert controller._to_pos_int(20, 5) == 20

    def test_to_pos_int_invalid_uses_default(self):
        """Should use default for invalid input."""
        controller = QueryController(MockQueryEngine())
        assert controller._to_pos_int("not-a-number", 5) == 5
        assert controller._to_pos_int(None, 10) == 10

    def test_to_pos_int_negative_uses_default(self):
        """Should use default for negative numbers."""
        controller = QueryController(MockQueryEngine())
        assert controller._to_pos_int(-5, 10) == 10


class TestQueryControllerCustomQuery:
    """Tests for custom query handling."""

    def test_custom_query_success(self):
        """Should execute custom query with valid params."""
        controller = QueryController(MockQueryEngine())
        request = UIRequest(
            action="custom",
            payload={
                "table": "player_info",
                "columns": ["firstName", "lastName"],
                "where": "",
                "limit": 10,
            },
        )
        response = controller.handle_request(request)
        assert response.success is True

    def test_custom_query_missing_table_fails(self):
        """Should fail without table name."""
        controller = QueryController(MockQueryEngine())
        request = UIRequest(
            action="custom",
            payload={"columns": ["firstName"], "where": "", "limit": 10},
        )
        response = controller.handle_request(request)
        assert response.success is False
