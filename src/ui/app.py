import os
import sys


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from textual.app import App
from textual.binding import Binding

from ui.interfaces import ControllerInterface
from ui.screens.home_screen import HomeScreen


class IceCubeApp(App):
    """
    ❄️ IceCube - Hockey Analytics Terminal UI

    Modular architecture for team collaboration:
    - Controllers handle business logic
    - Screens handle UI presentation
    - Database handles data operations

    No external dependencies needed - everything in lib/
    """

    CSS_PATH = ["styles/theme.tcss", "styles/components.tcss"]

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", show=True),
        Binding("ctrl+h", "home", "Home", show=False),
    ]

    def __init__(self, controller: ControllerInterface = None):
        """
        Initialize app with optional controller.

        Args:
            controller: Optional controller instance for dependency injection.
                        If None, will use mock controller for development.
        """
        super().__init__()
        self.controller = controller or self._create_mock_controller()
        self.db_connected = True

    def _create_mock_controller(self):
        """Create mock controller for development without database"""
        from ui.mocks.mock_controller import MockController

        return MockController()

    def on_mount(self) -> None:
        """Show HomeScreen directly on startup"""
        self.push_screen(HomeScreen(self.controller))

    def action_home(self) -> None:
        """Navigate to home screen"""
        self.switch_screen(HomeScreen(self.controller))

    def set_db_status(self, connected: bool) -> None:
        """Update database connection status"""
        self.db_connected = connected


def main():
    """Entry point for the application"""
    app = IceCubeApp()
    app.run()


if __name__ == "__main__":
    main()
