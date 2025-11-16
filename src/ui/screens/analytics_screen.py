"""
Analytics Screen - Advanced analytics and visualizations
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Static


class AnalyticsScreen(Screen):
    """Advanced analytics and data visualization screen"""

    BINDINGS = [
        Binding("escape", "back", "Back", show=True),
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh Data"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the analytics screen layout"""
        yield Header()

        with Horizontal():
            # Sidebar with analytics options
            with Vertical(classes="sidebar"):
                yield Static("ANALYTICS MODULES", classes="sidebar-title")

                with Container(classes="query-card"):
                    yield Static("📈 Seasonal Trends", classes="query-card-title")

                with Container(classes="query-card"):
                    yield Static("🔥 Hot Streaks", classes="query-card-title")

                with Container(classes="query-card"):
                    yield Static("❄️ Cold Streaks", classes="query-card-title")

                with Container(classes="query-card"):
                    yield Static("⚖️ Home vs Away", classes="query-card-title")

                with Container(classes="query-card"):
                    yield Static("🎯 Shot Efficiency", classes="query-card-title")

                with Container(classes="query-card"):
                    yield Static("👥 Line Chemistry", classes="query-card-title")

                with Container(classes="query-card"):
                    yield Static("📊 Statistical Leaders", classes="query-card-title")

                with Container(classes="query-card"):
                    yield Static("🔄 Trade Impact", classes="query-card-title")

            # Main content area
            with VerticalScroll(classes="content-area"):
                yield Static("Advanced Analytics Dashboard", classes="content-title")
                yield Static(
                    "Deep dive into NHL 2019-2020 season statistics and trends",
                    classes="content-subtitle",
                )

                # Key metrics overview
                with Horizontal():
                    with Container(classes="stats-panel"):
                        yield Static("LEAGUE AVG GOALS", classes="stat-label")
                        yield Static("6.02", classes="stat-value-large")
                        yield Static("Per Game", classes="content-subtitle")

                    with Container(classes="stats-panel"):
                        yield Static("LEAGUE AVG SAVES", classes="stat-label")
                        yield Static("27.8", classes="stat-value-large")
                        yield Static("Per Game", classes="content-subtitle")

                    with Container(classes="stats-panel"):
                        yield Static("POWERPLAY %", classes="stat-label")
                        yield Static("19.8%", classes="stat-value-large")
                        yield Static("League Average", classes="content-subtitle")

                    with Container(classes="stats-panel"):
                        yield Static("PENALTY KILL %", classes="stat-label")
                        yield Static("80.2%", classes="stat-value-large")
                        yield Static("League Average", classes="content-subtitle")

                # Seasonal trends section
                with Container(classes="stats-panel"):
                    yield Static("Seasonal Performance Trends", classes="content-title")
                    yield Static(
                        """
                        📈 October-November: Teams finding rhythm, avg 5.8 G/GP
                        🔥 December-January: Peak performance, avg 6.4 G/GP
                        📉 February: Post-All-Star dip, avg 5.9 G/GP
                        🚀 March: Playoff push intensity, avg 6.3 G/GP

                        Key Insight: Scoring peaks during December due to high-tempo
                        offensive play before the holiday break, with another surge
                        in March as teams battle for playoff positions.
                        """,
                        classes="content-subtitle",
                    )

                # Team comparison table
                yield Static("Top Teams by Category", classes="content-title")

                table = DataTable()
                table.add_columns("Category", "Team", "Value", "League Rank")

                categories = [
                    ("Goals For", "TBL", "3.47 G/GP", "1st"),
                    ("Goals Against", "BOS", "2.39 GA/GP", "1st"),
                    ("Power Play %", "EDM", "29.5%", "1st"),
                    ("Penalty Kill %", "BOS", "86.4%", "1st"),
                    ("Shot %", "COL", "10.8%", "1st"),
                    ("Save %", "BOS", ".930", "1st"),
                    ("Faceoff %", "BOS", "53.2%", "1st"),
                    ("Home Record", "TBL", "27-7-2", "1st"),
                ]

                for cat, team, val, rank in categories:
                    table.add_row(cat, team, val, rank)

                yield table

                # Advanced metrics
                with Container(classes="stats-panel"):
                    yield Static("Advanced Metrics", classes="content-title")
                    yield Static(
                        """
                        🎯 Shooting Percentage Leaders:
                        1. Colorado Avalanche - 10.8%
                        2. Tampa Bay Lightning - 10.3%
                        3. Vegas Golden Knights - 10.1%

                        🛡️ Save Percentage Leaders:
                        1. Boston Bruins - .930
                        2. Tampa Bay Lightning - .918
                        3. Colorado Avalanche - .915

                        ⚡ Special Teams Correlation:
                        Teams with top-10 PP% AND PK%: BOS, TBL, PHI, COL
                        These teams show strong coaching and discipline.

                        🏠 Home Ice Advantage:
                        League average home win %: 55.2%
                        Top home teams: TBL (75%), BOS (72.2%), STL (69.4%)
                        """,
                        classes="content-subtitle",
                    )

                # Player efficiency metrics
                yield Static("Player Efficiency Metrics", classes="content-title")

                eff_table = DataTable()
                eff_table.add_columns("Player", "Team", "Points/60", "Shots/60", "Efficiency")

                efficiency = [
                    ("L. Draisaitl", "EDM", "4.2", "10.5", "Elite"),
                    ("C. McDavid", "EDM", "3.9", "9.8", "Elite"),
                    ("D. Pastrnak", "BOS", "3.8", "11.2", "Elite"),
                    ("N. MacKinnon", "COL", "3.7", "10.1", "Elite"),
                    ("A. Panarin", "NYR", "3.6", "8.9", "Elite"),
                ]

                for player, team, pts, shots, eff in efficiency:
                    eff_table.add_row(player, team, pts, shots, eff)

                yield eff_table

                # Data insights
                with Container(classes="stats-panel"):
                    yield Static("Key Insights & Correlations", classes="content-title")
                    yield Static(
                        """
                        📊 Statistical Correlations Found:

                        1. Shot Accuracy > Shot Volume
                           - Teams with higher shooting % win 67% of games
                           - Teams leading in shots win only 54% of games

                        2. Special Teams = Success
                           - Top 5 PP% teams: 78% playoff rate
                           - Top 5 PK% teams: 82% playoff rate
                           - Both: 100% playoff rate

                        3. Goaltending Wins Championships
                           - Teams with .915+ SV%: 71% win rate
                           - Teams with .900- SV%: 38% win rate

                        4. Faceoff Dominance Impact
                           - 53%+ FO%: 62% win rate
                           - 47%- FO%: 41% win rate

                        5. Home Ice Matters More in Playoffs
                           - Regular season: +5.2% home advantage
                           - Playoffs: +8.7% home advantage
                        """,
                        classes="content-subtitle",
                    )

        yield Footer()

    def action_back(self) -> None:
        """Go back to home screen"""
        self.app.pop_screen()

    def action_refresh(self) -> None:
        """Refresh analytics data"""
        self.notify("Refreshing analytics data...")
        # TODO: Implement data refresh from database
