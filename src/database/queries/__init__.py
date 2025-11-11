"""
Queries Module - Predefined Query Implementations
=================================================

Contains organized, reusable query functions for common operations.

Files:
------
player_queries.py
    Player-related queries:
    - get_player_by_id()
    - get_player_stats()
    - get_top_scorers()
    - get_players_with_most_assists()
    - get_players_longest_shifts()
    - get_pure_goal_scorers() (score but never assist)

team_queries.py
    Team-related queries:
    - get_team_by_id()
    - get_team_roster()
    - get_highest_scoring_teams()
    - get_team_season_stats()
    - get_home_vs_away_performance()

game_queries.py
    Game-related queries:
    - get_game_by_id()
    - get_longest_games()
    - get_games_by_team()
    - get_game_scoring_trends()
    - get_most_common_play_types()

analytics_queries.py
    Advanced analytics queries:
    - head_to_head_duel_tracker()
    - revenge_game_effect()
    - home_rink_advantage()
    - birthday_curse_analysis()
    - scoring_trends_by_period()

Guidelines:
----------
- Each function returns QueryResponse
- Use query_builder for safe SQL construction
- Include comprehensive docstrings
- Handle edge cases (no results, invalid params)
- Log query execution for debugging
- Use type hints for all parameters

Owner: Database Developer (Varun Mulchandani)
"""

from .analytics_queries import (
    head_to_head_duel,
    revenge_game_effect,
)
from .game_queries import (
    get_game_by_id,
    get_longest_games,
)
from .player_queries import (
    get_player_by_id,
    get_player_stats,
    get_top_scorers,
)
from .team_queries import (
    get_highest_scoring_teams,
    get_team_by_id,
)

__all__ = [
    # Player queries
    "get_player_by_id",
    "get_player_stats",
    "get_top_scorers",
    # Team queries
    "get_team_by_id",
    "get_highest_scoring_teams",
    # Game queries
    "get_game_by_id",
    "get_longest_games",
    # Analytics queries
    "head_to_head_duel",
    "revenge_game_effect",
]
