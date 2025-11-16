"""
IceCube - NHL Analytics DBMS
Main Application Entry Point
"""

import os
import sys

# Add lib to path for Textual imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))

from screens.home_screen import HomeScreen
from screens.query_screen import QueryScreen
from textual.app import App
from textual.binding import Binding


class IceCubeApp(App):
    """IceCube NHL Analytics Application"""

    CSS_PATH = "styles/theme.tcss"

    TITLE = "Ice Cube - 2019-2020 Season"
    SUB_TITLE = "NHL Database Management System"

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("h", "show_home", "Home"),
        Binding("c", "custom_query", "Custom Query"),
        Binding("escape", "back", "Back"),
    ]

    def on_mount(self) -> None:
        """Initialize the application"""
        self.push_screen(HomeScreen())

    def action_show_home(self) -> None:
        """Show home screen"""
        self.push_screen(HomeScreen())

    def action_custom_query(self) -> None:
        """Show custom query screen"""
        self.push_screen(QueryScreen())

    def action_back(self) -> None:
        """Go back to previous screen"""
        if len(self.screen_stack) > 1:
            self.pop_screen()


def main():
    """Run the IceCube application"""
    app = IceCubeApp()
    app.run()


if __name__ == "__main__":
    main()
