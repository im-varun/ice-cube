"""
Results Screen - Display query results with various visualizations
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Static


class ResultsScreen(Screen):
    """Results display screen"""

    BINDINGS = [
        Binding("escape", "back", "Back", show=True),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self, query_id: str):
        super().__init__()
        self.query_id = query_id

    def compose(self) -> ComposeResult:
        """Compose the results screen layout"""
        yield Header()

        with Horizontal():
            # Sidebar
            with Vertical(classes="sidebar"):
                yield Static("PRE-DEFINED QUERIES", classes="sidebar-title")

                from widgets.query_card import QueryCard

                queries = [
                    ("🏒 Top 10 Goal Scorers", "goal_scorers"),
                    ("⚠ Most Penalized Teams", "penalized_teams"),
                    ("🛡 Goalie Save % Leaders", "goalie_leaders"),
                    ("⚡ Team Power Play", "power_play"),
                    ("📊 Player Point Dist.", "point_dist"),
                    ("⚡ Game Scoring Trends", "scoring_trends"),
                    ("🌟 Players with Most Assists", "most_assists"),
                    ("⏱ Longest Games", "longest_games"),
                    ("⚔ Head to Head Duel", "head_to_head"),
                    ("🎯 Messi or Ronaldo?", "messi_ronaldo"),
                    ("% Probability Queries", "probability"),
                    ("🎲 Most Common Play Types", "play_types"),
                ]

                for title, qid in queries:
                    yield QueryCard(title, qid, selected=(qid == self.query_id))

            # Main content area
            with VerticalScroll(classes="content-area"):
                # Render content based on query_id
                if self.query_id == "goal_scorers":
                    yield from self._render_goal_scorers()
                elif self.query_id == "longest_games":
                    yield from self._render_longest_games()
                elif self.query_id == "head_to_head":
                    yield from self._render_head_to_head()
                elif self.query_id == "messi_ronaldo":
                    yield from self._render_messi_ronaldo()
                elif self.query_id == "probability":
                    yield from self._render_probability()
                elif self.query_id == "play_types":
                    yield from self._render_play_types()
                elif self.query_id == "scoring_trends":
                    yield from self._render_scoring_trends()
                elif self.query_id == "most_assists":
                    yield from self._render_most_assists()
                elif self.query_id == "top_scoring":
                    yield from self._render_top_scoring()
                else:
                    yield Static(f"Query: {self.query_id}", classes="content-title")
                    yield Static("Results would be displayed here", classes="content-subtitle")

        yield Footer()

    def _render_goal_scorers(self) -> ComposeResult:
        """Render top goal scorers"""
        yield Static("Top 10 Goal Scorers", classes="content-title")
        yield Static(
            "Regular season statistics for the 2019-2020 season.", classes="content-subtitle"
        )

        # Stats cards
        with Horizontal():
            with Container(classes="stats-panel"):
                yield Static("TOTAL GOALS (SEASON)", classes="stat-label")
                yield Static("6,838", classes="stat-value-large")

            with Container(classes="stats-panel"):
                yield Static("AVG GOALS / GAME", classes="stat-label")
                yield Static("6.28", classes="stat-value-large")

            with Container(classes="stats-panel"):
                yield Static("LEAGUE LEADER (GOALS)", classes="stat-label")
                yield Static("48", classes="stat-value-large")

            with Container(classes="stats-panel"):
                yield Static("# OF HAT TRICKS", classes="stat-label")
                yield Static("52", classes="stat-value-large")

        # Data table
        table = DataTable()
        table.add_columns("RANK", "PLAYER", "TEAM", "GOALS")

        # Sample data - replace with actual query results
        players = [
            ("1", "A. Ovechkin", "WSH", "48"),
            ("1", "D. Pastrnak", "BOS", "48"),
            ("3", "A. Matthews", "TOR", "47"),
            ("4", "L. Draisaitl", "EDM", "43"),
            ("5", "M. Zibanejad", "NYR", "41"),
            ("6", "N. MacKinnon", "COL", "35"),
            ("7", "K. Connor", "WPG", "38"),
            ("8", "J. Eichel", "BUF", "36"),
        ]

        for rank, player, team, goals in players:
            table.add_row(rank, player, team, goals)

        yield table

        # Chart area
        with Container(classes="stats-panel"):
            yield Static("GOALS PER MONTH (PEAK)", classes="stat-label")
            yield Static("1,205 December", classes="stat-value")
            yield Static(
                """
                📊 [Chart visualization would go here]
                Peak scoring month: December with +5.2% increase
                """,
                classes="content-subtitle",
            )

    def _render_longest_games(self) -> ComposeResult:
        """Render longest games"""
        yield Static("Longest Games", classes="content-title")
        yield Static(
            "Games from the 2019-2020 season ranked by total time played, including overtime.",
            classes="content-subtitle",
        )

        # Maximum game time display
        with Container(classes="stats-panel"):
            yield Static("MAXIMUM GAME TIME", classes="stat-label")
            yield Static("150:27", classes="stat-value-large")

        # Games list
        games = [
            ("1", "TBL @ CBJ | Aug 11, 2020", "150:27", True),
            ("2", "CAR @ BOS | Aug 12, 2020", "139:39", False),
            ("3", "DAL @ TBL | Sep 25, 2020", "130:57", False),
            ("4", "VAN @ STL | Aug 21, 2020", "125:40", False),
            ("5", "NYI @ PHI | Sep 03, 2020", "122:03", False),
            ("6", "CGY @ DAL | Aug 16, 2020", "121:52", False),
            ("7", "TOR @ CBJ | Aug 07, 2020", "119:10", False),
        ]

        for rank, game, time, is_top in games:
            style = "highlight-orange" if is_top else ""
            with Container(classes="stats-panel " + style):
                yield Static(f"{rank}. {game}", classes="stat-label")
                yield Static(time, classes="stat-value")

    def _render_head_to_head(self) -> ComposeResult:
        """Render head-to-head comparison"""
        yield Static("Head to Head Duel Tracker", classes="content-title")
        yield Static(
            "Select two players to compare their 2019-2020 season statistics.",
            classes="content-subtitle",
        )

        # Player selection inputs
        with Horizontal():
            with Container(classes="vs-card"):
                yield Static("Player 1", classes="stat-label")
                yield Static("👤 Leon Draisaitl", classes="highlight-cyan")

            yield Static(" VS ", classes="vs-divider")

            with Container(classes="vs-card"):
                yield Static("Player 2", classes="stat-label")
                yield Static("👤 Connor McDavid", classes="highlight-orange")

        # Comparison table
        yield Static("COMPARISON", classes="content-title")

        table = DataTable()
        table.add_columns("LEON DRAISAITL", "STAT", "CONNOR MCDAVID")

        stats = [
            ("110", "POINTS", "97"),
            ("43", "GOALS", "45"),
            ("67", "ASSISTS", "52"),
            ("+15", "PLUS/MINUS", "+18"),
            ("18", "PIM", "12"),
            ("16", "PPG", "14"),
            ("6", "GWG", "7"),
        ]

        for stat1, label, stat2 in stats:
            table.add_row(stat1, label, stat2)

        yield table

    def _render_messi_ronaldo(self) -> ComposeResult:
        """Render Messi vs Ronaldo playful comparison"""
        yield Static("Messi or Ronaldo? - Head to Head Duel Tracker", classes="content-title")
        yield Static(
            "A playful, non-NHL query comparing two hockey legends in an alternate universe.",
            classes="content-subtitle",
        )

        with Horizontal():
            # Player 1 - "Ronaldo" (McDavid)
            with Container(classes="vs-card"):
                yield Static("PLAYER 1", classes="stat-label")
                yield Static('C. "RONALDO" MCDAVID', classes="highlight-cyan")
                yield Static("DUEL SCORE", classes="stat-label")
                yield Static("88", classes="stat-value-large")

            yield Static(" VS ", classes="vs-divider")

            # Player 2 - "Messi" (Crosby) - Winner
            with Container(classes="vs-card vs-card-winner"):
                yield Static("PLAYER 2", classes="stat-label")
                yield Static('S. "MESSI" CROSBY', classes="highlight-orange")
                yield Static("⭐ WINNER", classes="penalty-indicator")
                yield Static("DUEL SCORE", classes="stat-label")
                yield Static("92", classes="stat-value-large")

        # Breakdown
        yield Static("BREAKDOWN", classes="content-title")

        table = DataTable()
        table.add_columns("METRIC", "RONALDO", "MESSI")

        breakdown = [
            ("Goals", "45", "48"),
            ("Assists", "68", "60"),
            ("Power Play Points", "31", "25"),
            ("Faceoff %", "48.5%", "55.2%"),
            ("+/- Rating", "+12", "+18"),
        ]

        for metric, ron, mes in breakdown:
            table.add_row(metric, ron, mes)

        yield table

    def _render_probability(self) -> ComposeResult:
        """Render probability analysis"""
        yield Static("Probability Queries", classes="content-title")
        yield Static(
            "Calculated probabilities based on player and team performance data.",
            classes="content-subtitle",
        )

        with Container(classes="stats-panel"):
            yield Static("PROB. OF MCDAVID SCORING NEXT", classes="stat-label")
            yield Static("87.4%", classes="stat-value-large")
            yield Static(
                "Based on current game state & season performance", classes="content-subtitle"
            )

        yield Static("ANALYSIS DETAILS", classes="content-title")
        yield Static(
            """
            The probability calculation leverages a Bayesian inference model, considering
            multiple factors. The model is continuously updated with real-time game data to
            provide the most accurate predictions possible.

            Key input variables for this prediction include:
            - Player's historical scoring rate: 0.69 G/GP
            - Team's current power play status: ACTIVE
            - Time on ice in current period: 04:32
            - Shots on goal this game: 5
            """,
            classes="stats-panel",
        )

    def _render_play_types(self) -> ComposeResult:
        """Render most common play types"""
        yield Static("Most Common Play Types", classes="content-title")
        yield Static(
            "A ranked list of the most frequently occurring play types "
            "during the 2019-2020 NHL season.",
        )

        plays = [
            ("1", "Shot", "45,892", True),
            ("2", "Faceoff", "32,110", False),
            ("3", "Hit", "28,543", False),
            ("4", "Blocked Shot", "21,056", False),
            ("5", "Giveaway", "15,789", False),
            ("6", "Missed Shot", "14,981", False),
            ("7", "Takeaway", "12,345", False),
            ("8", "Penalty", "8,765", False),
            ("9", "Stoppage", "5,432", False),
        ]

        for rank, play_type, count, is_top in plays:
            style = "highlight-orange" if is_top else ""
            with Container(classes="stats-panel"):
                yield Static(f"{rank}. {play_type}", classes="stat-label " + style)
                yield Static(f"{count} Occurrences", classes="stat-value " + style)

    def _render_scoring_trends(self) -> ComposeResult:
        """Render game scoring trends"""
        yield Static("Game Scoring Trends", classes="content-title")
        yield Static(
            "Analysis of the average goals per game throughout the 2019-2020 NHL season.",
            classes="content-subtitle",
        )

        with Container(classes="chart-container"):
            yield Static("Season High: 6.45", classes="stat-label")
            yield Static(
                """
                📈 [Sparkline chart visualization]

                Oct 2019 ─────────────── Jan 2020 ─────────────── Mar 2020
                """,
                classes="content-subtitle",
            )

        yield Static("Markdown Analysis", classes="content-title")
        yield Static(
            """
            The sparkline above visualizes the trend of the average goals scored per game across
            the 2019-2020 season. Data is aggregated on a weekly basis from October 2019 to March
            2020.

            Season Average: 6.02 G/GP
            Peak Scoring: A significant spike is observed in late-February, reaching a season-
            high of 6.45 G/GP, likely driven by trade deadline dynamics and playoff pushes.
            General Trend: Scoring shows natural ebbs and flows, with a slight dip post-holidays
            before ramping up towards the end of the regular season.

            This query demonstrates the league's offensive rhythm over the season, providing a
            high-level overview of scoring volatility.
            """,
            classes="stats-panel",
        )

    def _render_most_assists(self) -> ComposeResult:
        """Render players with most assists"""
        yield Static("Players with Most Assists", classes="content-title")
        yield Static(
            "Leaderboard of players ranked by total assists in the 2019-2020 season.",
            classes="content-subtitle",
        )

        table = DataTable()
        table.add_columns("RANK", "PLAYER", "TEAM", "ASSISTS")

        players = [
            ("1", "Leon Draisaitl", "EDM", "67"),
            ("2", "Connor McDavid", "EDM", "63"),
            ("3", "John Carlson", "WSH", "60"),
            ("4", "Brad Marchand", "BOS", "59"),
            ("5", "Artemi Panarin", "NYR", "59"),
            ("6", "Nathan MacKinnon", "COL", "58"),
            ("7", "David Pastrnak", "BOS", "57"),
            ("8", "Jack Eichel", "BUF", "54"),
            ("9", "Nikita Kucherov", "TBL", "52"),
            ("10", "Jonathan Huberdeau", "FLA", "51"),
        ]

        for rank, player, team, assists in players:
            table.add_row(rank, player, team, assists)

        yield table

    def _render_top_scoring(self) -> ComposeResult:
        """Render top scoring players"""
        yield Static("Top Scoring Players", classes="content-title")
        yield Static(
            "Players from the 2019-2020 season ranked by total points (Goals + Assists). "
            "(*) indicates a penalty-prone player.",
            classes="content-subtitle",
        )

        table = DataTable()
        table.add_columns("#", "PLAYER", "TEAM", "POINTS")

        players = [
            ("1", "Leon Draisaitl (EDM)", "EDM", "110 PTS"),
            ("2", "Connor McDavid (EDM)", "EDM", "97 PTS"),
            ("3", "David Pastrnak (BOS)", "BOS", "95 PTS"),
            ("4", "Artemi Panarin (NYR)", "NYR", "95 PTS"),
            ("5", "Nathan MacKinnon (COL)", "COL", "93 PTS"),
            ("6", "⚠ Brad Marchand (BOS)", "BOS", "87 PTS *"),
            ("7", "Jack Eichel (BUF)", "BUF", "82 PTS"),
            ("8", "Kevin Fiala (MIN)", "MIN", "81 PTS"),
            ("9", "Patrick Kane (CHI)", "CHI", "80 PTS"),
            ("10", "⚠ Evgeni Malkin (PIT)", "PIT", "79 PTS *"),
            ("11", "Auston Matthews (TOR)", "TOR", "78 PTS"),
            ("12", "Nikita Kucherov (TBL)", "TBL", "77 PTS"),
        ]

        for num, player, team, points in players:
            table.add_row(num, player, team, points)

        yield table

    def on_query_card_selected(self, event) -> None:
        """Handle query card selection"""
        # Pop current screen and push new results screen
        self.app.pop_screen()
        self.app.push_screen(ResultsScreen(event.query_id))

    def action_back(self) -> None:
        """Go back to home screen"""
        self.app.pop_screen()
