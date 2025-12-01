import os
import sys

ROOT_DIR_NAME = "ice-cube"
curr_path = os.path.dirname(__file__)
idx = curr_path.find(ROOT_DIR_NAME) + len(ROOT_DIR_NAME)
ROOT_PATH = curr_path[:idx]
sys.path.insert(0, os.path.join(ROOT_PATH, "lib"))

from textual.app import App
from textual.binding import Binding
from dotenv import load_dotenv

from controllers.query_controller import QueryController
from database.query_engine import QueryEngine
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

    CSS_PATH = ["./ui/styles/theme.tcss", "./ui/styles/components.tcss"]

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", show=True),
        Binding("ctrl+h", "home", "Home", show=False),
    ]

    MODES = {"home": HomeScreen}

    def __init__(self, controller: ControllerInterface):
        """
        Initialize app with controller.

        Args:
            controller: controller instance for dependency injection.
        """
        super().__init__()
        self.controller = controller
        self.db_connected = True

    def _create_mock_controller(self):
        """Create mock controller for development without database"""
        from ui.mocks.mock_controller import MockController

        return MockController()

    def on_mount(self) -> None:
        """Show HomeScreen directly on startup"""
        self.push_screen(HomeScreen())

    def action_home(self) -> None:
        """Navigate to home screen"""
        self.switch_screen(HomeScreen())

    def set_db_status(self, connected: bool) -> None:
        """Update database connection status"""
        self.db_connected = connected


def main():
    """Entry point for the application"""

    load_dotenv()

    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([server, database, user, password]):
        print("Warning: Database credentials not found in .env file")
        exit(0)

    query_engine = QueryEngine(server, database, user, password)
    controller = QueryController(query_engine)
    app = IceCubeApp(controller=controller)
    app.run()


if __name__ == "__main__":
    main()
