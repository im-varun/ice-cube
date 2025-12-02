import os
import sys

ROOT_DIR_NAME = "ice-cube"
curr_path = os.path.dirname(__file__)
idx = curr_path.find(ROOT_DIR_NAME) + len(ROOT_DIR_NAME)
ROOT_PATH = curr_path[:idx]
sys.path.insert(0, os.path.join(ROOT_PATH, "lib"))

from dotenv import load_dotenv
from textual.app import App
from textual.binding import Binding

from controllers.query_controller import QueryController
from database.query_engine import QueryEngine
from ui.interfaces import ControllerInterface, UIRequest
from ui.screens import AnalyticsScreen, HomeScreen, SearchScreen


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
        Binding("q", "quit", "Quit", show=True),
        Binding("h", "app.push_screen('home')", "Home", show=True),
        Binding("s", "app.push_screen('search')", "Search", show=True),
        Binding("a", "app.push_screen('analytics')", "Analytics", show=True),
        Binding("r", "restart", "Restart", show=True),
    ]

    # MODES = {"home": HomeScreen}
    SCREENS = {"home": HomeScreen, "search": SearchScreen, "analytics": AnalyticsScreen}

    def __init__(self, controller: ControllerInterface, refresh_duration: int = 1):
        """
        Initialize app with controller.

        Args:
            controller: controller instance for dependency injection.
        """
        super().__init__()
        self.controller = controller
        self.refresh_duration = refresh_duration

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

    def action_restart(self) -> None:
        """An action to restart the application."""
        request = UIRequest(action="refresh", payload={})
        self.notify(f"Repopulating Database.\nQueries are locked for {self.refresh_duration} sec")
        response = self.controller.handle_request(request).message
        self.notify("Database Repopulated!")

        # TODO: Varun please update the below message to a appropriate message
        self.notify(str(response))


def main():
    """Entry point for the application"""

    load_dotenv()

    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    wait_time = int(os.getenv("DB_REPOPULATION_TIME"))

    if not all([server, database, user, password]):
        print("Warning: Database credentials not found in .env file")
        exit(0)

    query_engine = QueryEngine(server, database, user, password)
    controller = QueryController(query_engine)
    app = IceCubeApp(controller=controller, refresh_duration=wait_time)
    app.run()


if __name__ == "__main__":
    main()
