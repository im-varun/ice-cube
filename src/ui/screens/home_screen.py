"""
Home Screen - Main dashboard with pre-defined queries
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Static
from widgets.query_card import QueryCard


class HomeScreen(Screen):
    """Main home screen with query selection"""

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("c", "custom_query", "Custom Query"),
        Binding("h", "show_help", "Help"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the home screen layout"""
        yield Header()

        with Horizontal():
            # Sidebar with pre-defined queries
            with Vertical(classes="sidebar"):
                yield Static("PRE-DEFINED QUERIES", classes="sidebar-title")

                yield QueryCard("🏆 Top Scoring Players", "top_scoring", icon="🏆")

                yield QueryCard("⚠ Most Penalized Teams", "penalized_teams", icon="⚠")

                yield QueryCard("🛡 Goalie Save % Leaders", "goalie_leaders", icon="🛡")

                yield QueryCard("⚡ Game Scoring Trends", "scoring_trends", icon="⚡")

                yield QueryCard("⏱ Longest Games", "longest_games", icon="⏱")

                yield QueryCard("🌟 Players with Most Assists", "most_assists", icon="🌟")

                yield QueryCard("⚔ Head to Head Duel", "head_to_head", icon="⚔")

                yield QueryCard("🎯 Messi or Ronaldo?", "messi_ronaldo", icon="🎯")

                yield QueryCard("📊 Player Point Dist.", "point_dist", icon="📊")

                yield QueryCard("% Probability Queries", "probability", icon="%")

                yield QueryCard("⚡ Team Power Play", "power_play", icon="⚡")

                yield QueryCard("🎲 Most Common Play Types", "play_types", icon="🎲")

                yield QueryCard("🏒 Top 10 Goal Scorers", "goal_scorers", icon="🏒")

            # Main content area
            with VerticalScroll(classes="content-area"):
                yield Static("Welcome to IceCube", classes="content-title")
                yield Static(
                    "Select a query from the sidebar to begin analysis", classes="content-subtitle"
                )

                # Welcome message
                with Container():
                    yield Static(
                        """
                        ❄️  IceCube - NHL Analytics Database

                        A crystalline database management system for NHL analytics.
                        Built for the 2019-2020 season.

                        Features:
                        • Pre-defined analytical queries
                        • Custom SQL query runner
                        • Real-time statistics
                        • Player comparisons
                        • Team analytics

                        Navigate using:
                        • [C] Custom Query
                        • [H] Help
                        • [Q] Quit

                        "You miss 100% of the queries you don't run."
                        — Wayne Gretzky, probably
                        """,
                        classes="stats-panel",
                    )

        yield Footer()

    def on_query_card_selected(self, event: QueryCard.Selected) -> None:
        """Handle query card selection"""
        query_id = event.query_id

        # Import here to avoid circular imports
        from screens.results_screen import ResultsScreen

        # Navigate to results screen with query ID
        self.app.push_screen(ResultsScreen(query_id))

    def action_custom_query(self) -> None:
        """Show custom query screen"""
        from screens.query_screen import QueryScreen

        self.app.push_screen(QueryScreen())

    def action_show_help(self) -> None:
        """Show help dialog"""
        self.app.push_screen(HelpScreen())


class HelpScreen(Screen):
    """Help information screen"""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("q", "dismiss", "Close"),
    ]

    def compose(self) -> ComposeResult:
        with Container():
            yield Static("IceCube Help", classes="content-title")
            yield Static(
                """
                Keyboard Shortcuts:

                [Q] Quit        - Exit the application
                [C] Custom Query - Open SQL query runner
                [H] Help        - Show this help screen
                [Esc] Back      - Return to previous screen

                Navigation:
                • Use arrow keys to navigate
                • Use Tab to switch between elements
                • Press Enter to select

                Query Runner:
                • Ctrl+E - Execute query
                • Ctrl+L - Clear query

                For more information, visit the documentation.
                """,
                classes="stats-panel",
            )
            yield Button("Close", variant="primary", id="close-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press"""
        self.dismiss()

    def action_dismiss(self) -> None:
        """Dismiss the help screen"""
        self.app.pop_screen()
