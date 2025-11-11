"""
Models Module - Data Models and Schemas
=======================================

Defines data structures representing database entities.

Files:
------
player.py
    Player model with attributes:
    - player_id, name, position, team_id
    - jersey_number, birthdate, height, weight
    Methods: from_dict(), to_dict(), validate()

team.py
    Team model with attributes:
    - team_id, name, city, arena_name
    - division, conference, founded_year
    Methods: from_dict(), to_dict(), validate()

game.py
    Game model with attributes:
    - game_id, date, home_team_id, away_team_id
    - home_score, away_score, overtime, shootout
    - duration, attendance
    Methods: from_dict(), to_dict(), validate()

Guidelines:
----------
- Use dataclasses or pydantic for models
- Include validation methods
- Provide serialization (to/from dict)
- Document all fields with type hints
- Handle None/null values appropriately
- Include helper methods for common operations

Owner: Database Developer (Varun Mulchandani)
"""

from .player import Player
from .team import Team
from .game import Game

__all__ = [
    "Player",
    "Team",
    "Game",
]
