"""
Analytics Screen - 12 pre-defined queries in ONE full-height column
No scrolling in sidebar, only results scroll
"""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Static
from ..widgets.query_card import QueryCard


class AnalyticsScreen(Screen):
    """Results screen with 12 queries in a single, full-height column"""

    BINDINGS = [
        ("escape", "back", "Back"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, query_id: str):
        super().__init__()
        self.query_id = query_id

    def compose(self) -> ComposeResult:
        yield Header()

        # ────────────────────────────────────────────────────────────────
        # MAIN LAYOUT
        # ────────────────────────────────────────────────────────────────
        with Horizontal():
            with Vertical(classes="sidebar"):
                yield Static("PRE-DEFINED QUERIES", classes="sidebar-title")

                # 12 queries – one per line, full width
                queries = [
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
                ]

                # ONE QueryCard per row – no Grid, no scroll
                for title, qid in queries:
                    yield QueryCard(title, qid)

            # ── RIGHT CONTENT: Title + scrollable table only ───────────
            with Vertical(classes="content-area"):
                # Dynamic title
                title_map = {qid: title for title, qid in queries}
                yield Static(title_map.get(self.query_id, "Query Results"), classes="content-title")

                # Scrollable results container
                with ScrollableContainer():
                    table = DataTable()
                    table.add_columns("#", "PLAYER", "TEAM", "POINTS")
                    table.add_rows(
                        [
                            ("1", "Leon Draisaitl", "EDM", "110 PTS"),
                            ("2", "Connor McDavid", "EDM", "97 PTS"),
                            ("3", "David Pastrnak", "BOS", "95 PTS"),
                            ("4", "Artemi Panarin", "NYR", "95 PTS"),
                            ("5", "Nathan MacKinnon", "COL", "93 PTS"),
                            ("6", "Brad Marchand", "BOS", "87 PTS"),
                            ("7", "Jack Eichel", "BUF", "82 PTS"),
                            ("8", "Kevin Fiala", "MIN", "81 PTS"),
                            ("9", "Patrick Kane", "CHI", "80 PTS"),
                            ("10", "Evgeni Malkin", "PIT", "79 PTS"),
                            ("11", "Auston Matthews", "TOR", "78 PTS"),
                            ("12", "Nikita Kucherov", "TBL", "77 PTS"),
                        ]
                    )
                    yield table

        yield Footer()

    # ────────────────────────────────────────────────────────────────
    # Navigation
    # ────────────────────────────────────────────────────────────────
    def on_query_card_selected(self, event: QueryCard.Selected) -> None:
        """Switch to new result when a sidebar query is clicked"""
        self.app.push_screen(AnalyticsScreen(event.query_id))

    def action_back(self) -> None:
        """Return to Home Screen"""
        self.app.pop_screen()
