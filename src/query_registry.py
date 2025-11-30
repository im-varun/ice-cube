from dataclasses import dataclass
from typing import ClassVar
from enum import Enum

@dataclass(frozen=True)
class QueryInfo:
    """Query metadata for UI/controller mapping."""
    id: str              # Controller function ID
    title: str           # UI display title
    description: str     # UI description
    needs_payload: bool  # Input based query or not

class Query(Enum):
    """Type-safe query identifiers for NHL analytics."""
    
    TOP_SCORING_PLAYERS = QueryInfo(
        id="top_scoring",
        title="Top Scoring Players",
        description="Players ranked by highest combined goals + assists",
        needs_payload=True
    )

    MOST_PENALIZED_TEAMS = QueryInfo(
        id="penalized_teams", 
        title="Most Penalized Teams",
        description="Teams with highest total penalty minutes per season",
        needs_payload=False
    )

    LONGEST_GAMES = QueryInfo(
        id="longest_games",
        title="Longest Games", 
        description="Games ranked by total elapsed time including overtime",
        needs_payload=False
    )

    MOST_ASSISTS = QueryInfo(
        id="most_assists",
        title="Players with Most Assists",
        description="Players with highest assist totals across seasons",
        needs_payload=False
    )
    
    HEAD_TO_HEAD = QueryInfo(
        id="head_to_head",
        title="Head to Head Duel",
        description="Head-to-head performance stats between selected players",
        needs_payload=True
    )
    
    PLAY_TYPES = QueryInfo(
        id="play_types",
        title="Most Common Play Types",
        description="Frequency analysis of shot attempts by play type (tip-ins, wrist shots, etc.)",
        needs_payload=False
    )
    
    REVENGE_GAME_EFFECT = QueryInfo(
        id="revenge_game_effect",
        title="Revenge Game Effect", 
        description="Performance analysis of players vs. former teams",
        needs_payload=False
    )
    
    HOME_RINK_ADVANTAGE = QueryInfo(
        id="home_rink_advantage",
        title="Home Rink Advantage",
        description="Team performance metrics by home vs. away venue",
        needs_payload=False
    )
    
    BIRTHDAY_CURSE = QueryInfo(
        id="birthday_curse",
        title="Birthday Curse Analysis",
        description="Analysis of player performance on birthdays",
        needs_payload=False
    )
    
    TOP_SHOOTING_TEAMS = QueryInfo(
        id="top_shooting_teams",
        title="Top Shooting Teams",
        description="Teams ranked by shooting percentage and shot volume",
        needs_payload=False
    )

    LONGEST_AVG_SHIFT = QueryInfo(
        id="longest_avg_shift",
        title="Longest Average Shifts",
        description="Players with longest average time-on-ice per shift",
        needs_payload=False
    )

    LONE_WOLFS = QueryInfo(
        id="score_not_assist",
        title="Lone Wolfs",
        description="Players who score goals but rarely assist (goal-scorers only)",
        needs_payload=True
    )

    @classmethod
    def from_id(cls, query_id: str) -> 'Query':
        """Convert controller ID string to Query enum member."""
        for query in cls:
            if query.value.id == query_id:
                return query
        raise ValueError(f"Unknown query ID: {query_id}")

    @classmethod
    def get_info(cls, query_id: str) -> QueryInfo:
        """Get full QueryInfo by controller ID for UI display."""
        for query in cls:
            if query.value.id == query_id:
                return query.value
        raise ValueError(f"Unknown query ID: {query_id}")
    
    @classmethod
    def list_queries(cls) -> list['Query']:
        """Get all available queries."""
        return [member for member in cls if isinstance(member.value, QueryInfo)]
    
    @classmethod
    def titles(cls) -> list[str]:
        """Get all query titles for UI."""
        return [q.value.title for q in cls.list_queries()]

if __name__ == "__main__":
    print(Query.PLAY_TYPES.value.title)  # Direct access works
    for query_info in Query.list_queries():
        print(query_info.value.title, query_info.value.id)
