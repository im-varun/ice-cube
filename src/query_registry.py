"""
Central registry for query definitions to ensure consistency between UI and Controller.
"""

QUERIES = [
    ("Top Scoring Players", "top_scoring"),
    ("Most Penalized Teams", "penalized_teams"),
    ("Goalie Save % Leaders", "goalie_leaders"),
    ("Game Scoring Trends", "scoring_trends"),
    ("Longest Games", "longest_games"),
    ("Players with Most Assists", "most_assists"),
    ("Head to Head Duel", "head_to_head"),
    ("Messi or Ronaldo?", "messi_ronaldo"),
    ("Player Point Dist.", "point_dist"),
    ("Probability Queries", "probability"),
    ("Team Power Play", "power_play"),
    ("Most Common Play Types", "play_types"),
    ("Revenge Game Effect", "revenge_game_effect"),
    ("Home Rink Advantage", "home_rink_advantage"),
    ("Birthday Curse", "birthday_curse"),
]

# Map for easy lookup by ID
QUERY_MAP = {qid: title for title, qid in QUERIES}
