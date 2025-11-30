"""
Central registry for query definitions to ensure consistency between UI and Controller.
"""

# QUERIES = [ <UI label for query>, <controller id> ]
# Make sure to update controllers/query_controller.py if changing any controller id
QUERIES = [
    ("Top Scoring Players", "top_scoring"),
    ("Most Penalized Teams", "penalized_teams"),
    ("Longest Games", "longest_games"),
    ("Players with Most Assists", "most_assists"),
    ("Head to Head Duel", "head_to_head"),
    ("Most Common Play Types", "play_types"),
    ("Revenge Game Effect", "revenge_game_effect"),
    ("Home Rink Advantage", "home_rink_advantage"),
    ("Birthday Curse", "birthday_curse"),
    ("Top Shooting Teams", "top_shooting_teams"),
    ("Longest Average Shifts", "longest_avg_shift"),
    ("Lone Wolfs", "score_not_assist")
]

# Map for easy lookup by ID
QUERY_MAP = {qid: title for title, qid in QUERIES}
