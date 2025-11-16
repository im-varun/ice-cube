"""
Complete test runner for IceCube UI
Run from src/ui directory: python test_all.py
"""

import os
import sys

# Add lib to path for Textual imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))

from screens.analytics_screen import AnalyticsScreen

# Import all screens
from screens.home_screen import HomeScreen
from screens.login_screen import LoginScreen
from screens.query_screen import QueryScreen
from screens.results_screen import ResultsScreen
from textual.app import App
from textual.binding import Binding


class TestIceCubeApp(App):
    """Test application for IceCube UI"""

    CSS_PATH = ["styles/theme.tcss", "styles/components.tcss"]
    TITLE = "Ice Cube - 2019-2020 Season [TEST MODE]"

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("1", "test_login", "1: Login"),
        Binding("2", "test_home", "2: Home"),
        Binding("3", "test_query", "3: Query"),
        Binding("4", "test_results", "4: Results"),
        Binding("5", "test_analytics", "5: Analytics"),
        Binding("escape", "back", "Back"),
    ]

    def on_mount(self) -> None:
        """Start with home screen"""
        self.push_screen(HomeScreen())

    def action_test_login(self) -> None:
        """Test login screen"""
        self.push_screen(LoginScreen())

    def action_test_home(self) -> None:
        """Test home screen"""
        self.push_screen(HomeScreen())

    def action_test_query(self) -> None:
        """Test query screen"""
        self.push_screen(QueryScreen())

    def action_test_results(self) -> None:
        """Test results screen"""
        self.push_screen(ResultsScreen("goal_scorers"))

    def action_test_analytics(self) -> None:
        """Test analytics screen"""
        self.push_screen(AnalyticsScreen())

    def action_back(self) -> None:
        """Go back"""
        if len(self.screen_stack) > 1:
            self.pop_screen()


if __name__ == "__main__":
    print("🧪 Starting IceCube UI Test...")
    print("📋 Available screens:")
    print("  [1] Login Screen")
    print("  [2] Home Screen")
    print("  [3] Query Screen")
    print("  [4] Results Screen")
    print("  [5] Analytics Screen")
    print("  [Q] Quit")
    print("  [Esc] Go Back")
    print("\n🚀 Launching application...\n")

    app = TestIceCubeApp()
    app.run()
