from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class QueryInfo:
    """Query metadata for UI/controller mapping."""

    id: str  # Controller function ID
    title: str  # UI display title
    description: str  # UI description
    needs_payload: bool  # Input based query or not
    payload_labels: list[str] | None  # Labels for the user input fields of query


class Query(Enum):
    """Type-safe query identifiers for NHL analytics."""

    HEAD_TO_HEAD = QueryInfo(
        id="head_to_head",
        title="Head to Head Duel",
        description="""
        Head-to-head performance stats between 2 players
        Every fan have argued that their fav skater is the G.O.A.T (Greatest of All Time)
        Lets keep aside personal sentiments and find it using data
        Use the search option and look for player_info tables to find players to compete with
        eg- Try competing
        Ron Hainsey VS Bobby Ryan
        """,
        needs_payload=True,
        payload_labels=["Player 1", "Player 2"],
    )

    REVENGE_GAME_EFFECT = QueryInfo(
        id="revenge_game_effect",
        title="Revenge Game Effect",
        description="""
        Tracks players facing their former teams and measures if they exhibit elevated performance
        ("revenge game" phenomenon), showing goals, assists, and intensity metrics.

        Use Case:
        Broadcasters can highlight storylines for games.
        Fantasy sports players can exploit this trend.
        Team management can assess emotional factors in trades.
        """,
        needs_payload=False,
        payload_labels=None,
    )

    HOME_RINK_ADVANTAGE = QueryInfo(
        id="home_rink_advantage",
        title="Home Rink Advantage",
        description="""
        Analyzes whether starting on a specific rink side (defending a particular end first)
        correlates with winning, revealing potential psychological or strategic advantages.

        Use Case:
        Coaches can use this for strategic decisions during coin tosses.
        Arena designers might consider sight-line advantages.
        Betting analysts can factor this into predictions.
        """,
        needs_payload=False,
        payload_labels=None,
    )

    BIRTHDAY_CURSE = QueryInfo(
        id="birthday_curse",
        title="Birthday Curse Analysis",
        description="""
        Identifies players who have played games on their birthday and analyzes their performance
        to see if there's a birthday curse or birthday boost effect.

        Use Case:
        Sports psychologists and coaches can use this to understand
        if playing on birthdays affects player performance.
        Media outlets can create engaging birthday related stories.
        Teams might consider this for lineup decisions.
        """,
        needs_payload=False,
        payload_labels=None,
    )

    LONE_WOLFS = QueryInfo(
        id="score_not_assist",
        title="Lone Wolfs",
        description="""
        This query finds hockey players who score goals but have zero assists,
        highlighting pure finishers.
        It focuses on players who contribute only by shooting, not by playmaking.\n
        Parameters
        Minimum goals: try with 5 goals,
        but you can raise or lower it depending on how strict you want the filter to be.\n
        Example Use Case
        With minimum of 5 goals, Jesper Boqvist shows up with 6 goals and 0 assists
        a rare type of player who finishes plays but never sets them up.
        This can help coaches identify players who may need to improve passing skills
        or help teams looking for a one-dimensional shooter.
        """,
        needs_payload=True,
        payload_labels=["minimum goals", "max results"],
    )

    TOP_SCORING_PLAYERS = QueryInfo(
        id="top_scoring",
        title="Top Scoring Players",
        description="""
        This query ranks players by their total offensive production (goals + assists).
        It highlights players who contribute heavily to scoring while also staying disciplined.

        Parameters
        Penalty Threshold: The maximum number of penalties a player can have
            eg- 30 means only players with fewer than 30 penalties are shown,
            helping filter for disciplined players.
        Minimum Goals: The minimum number of goals a player must score to qualify.
            eg- 10 ensures the list focuses on players who are strong and consistent goal scorers.

        Result Interpretation
        The query found 349 disciplined goal scorers who produce a lot of offense
        without taking too many penalties.
        The top result is Leon Draisaitl, with 123 goals under the set penalty limit.
        This helps identify clean offensive players, those who score often
        but don't hurt the team by sitting in the penalty box.
        It's useful for contract evaluations, fantasy leagues,
        and coaches looking for productive yet disciplined players.
        """,
        needs_payload=True,
        payload_labels=["penalty threshold", "minimum goals", "max results"],
    )

    LONGEST_AVG_SHIFT = QueryInfo(
        id="longest_avg_shift",
        title="Longest Average Shifts",
        description="Players with longest average time-on-ice per shift",
        needs_payload=False,
        payload_labels=None,
    )

    MOST_PENALIZED_PLAYERS = QueryInfo(
        id="penalized_teams",
        title="Most Penalized Players",
        description="Players with highest total penalty minutes per season",
        needs_payload=False,
        payload_labels=None,
    )

    LONGEST_GAMES = QueryInfo(
        id="longest_games",
        title="Longest Games",
        description="Games ranked by total elapsed time including overtime",
        needs_payload=False,
        payload_labels=None,
    )

    MOST_ASSISTS = QueryInfo(
        id="most_assists",
        title="Players with Most Assists",
        description="Players with highest assist totals across seasons",
        needs_payload=False,
        payload_labels=None,
    )

    PLAY_TYPES = QueryInfo(
        id="play_types",
        title="Most Common Play Types",
        description="Frequency analysis of shot attempts by play type (tip-ins, wrist shots, etc.)",
        needs_payload=False,
        payload_labels=None,
    )

    TOP_SHOOTING_TEAMS = QueryInfo(
        id="top_shooting_teams",
        title="Top Shooting Teams",
        description="Teams ranked by shooting percentage and shot volume",
        needs_payload=False,
        payload_labels=None,
    )

    @classmethod
    def from_id(cls, query_id: str) -> "Query":
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
    def list_queries(cls) -> list["Query"]:
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
