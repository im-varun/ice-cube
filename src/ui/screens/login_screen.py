"""
Login Screen - Database connection and authentication
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Static


class LoginScreen(Screen):
    """Database connection screen"""

    BINDINGS = [
        Binding("escape", "quit", "Quit", show=True),
        Binding("ctrl+enter", "connect", "Connect"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the login screen layout"""
        yield Header()

        with Container(classes="content-area"):
            with Center():
                with Vertical():
                    # Title and logo
                    yield Static(
                        """
                        ❄️  ICE CUBE

                        NHL Database Management System
                        2019-2020 Season Analytics
                        """,
                        classes="content-title",
                    )

                    # Connection form
                    with Container(classes="stats-panel"):
                        yield Static("Database Connection", classes="content-title")

                        yield Static("Database Host:", classes="stat-label")
                        host_input = Input(placeholder="localhost", id="host-input")
                        host_input.styles.margin = (0, 0, 1, 0)
                        yield host_input

                        yield Static("Port:", classes="stat-label")
                        port_input = Input(placeholder="5432", id="port-input")
                        port_input.styles.margin = (0, 0, 1, 0)
                        yield port_input

                        yield Static("Database Name:", classes="stat-label")
                        db_input = Input(placeholder="nhl_2019_2020", id="database-input")
                        db_input.styles.margin = (0, 0, 1, 0)
                        yield db_input

                        yield Static("Username:", classes="stat-label")
                        user_input = Input(placeholder="postgres", id="username-input")
                        user_input.styles.margin = (0, 0, 1, 0)
                        yield user_input

                        yield Static("Password:", classes="stat-label")
                        pass_input = Input(
                            placeholder="••••••••", password=True, id="password-input"
                        )
                        pass_input.styles.margin = (0, 0, 2, 0)
                        yield pass_input

                        # Buttons
                        with Center():
                            yield Button("Connect to Database", variant="success", id="connect-btn")
                            yield Button(
                                "Connect as Guest (Demo Mode)", variant="primary", id="guest-btn"
                            )

                    # Connection info
                    with Container(classes="stats-panel"):
                        yield Static("Connection Options", classes="content-title")
                        yield Static(
                            """
                            🔌 Standard Connection:
                            Enter your PostgreSQL database credentials to connect
                            to your NHL 2019-2020 season database.

                            👤 Guest Mode (Demo):
                            Try IceCube with sample data without database setup.
                            Perfect for testing and demonstrations.

                            ⚙️ Requirements:
                            • PostgreSQL 12+ or compatible database
                            • NHL 2019-2020 dataset loaded
                            • Network access to database server

                            💡 Tip: Use Ctrl+Enter to quickly connect
                            """,
                            classes="content-subtitle",
                        )

                    # Status message area
                    yield Static("", id="status-message", classes="content-subtitle")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press"""
        if event.button.id == "connect-btn":
            self.action_connect()
        elif event.button.id == "guest-btn":
            self.connect_guest_mode()

    def action_connect(self) -> None:
        """Connect to database with provided credentials"""
        _ = self.query_one("#host-input", Input).value or "localhost"
        _ = self.query_one("#port-input", Input).value or "5432"
        _ = self.query_one("#database-input", Input).value or "nhl_2019_2020"
        _ = self.query_one("#username-input", Input).value or "postgres"
        _ = self.query_one("#password-input", Input).value

        status = self.query_one("#status-message", Static)

        # TODO: Replace with actual database connection
        # This is a placeholder - integrate with your database controller
        try:
            # Example connection code:
            # from database.connection import DatabaseConnection
            # db = DatabaseConnection(host, port, database, username, password)
            # if db.connect():
            #     self.app.push_screen(HomeScreen())
            # else:
            #     status.update("❌ Connection failed. Please check credentials.")

            # For now, simulate successful connection
            status.update("✅ Connected successfully!")
            self.notify("Database connected successfully!")

            # Navigate to home screen
            from screens.home_screen import HomeScreen

            self.app.push_screen(HomeScreen())

        except Exception as e:
            status.update(f"❌ Connection failed: {str(e)}")
            self.notify(f"Connection error: {str(e)}", severity="error")

    def connect_guest_mode(self) -> None:
        """Connect in guest mode with demo data"""
        status = self.query_one("#status-message", Static)
        status.update("🎮 Launching demo mode with sample data...")

        self.notify("Connected in guest mode with sample data!")

        # Navigate to home screen in demo mode
        from screens.home_screen import HomeScreen

        self.app.push_screen(HomeScreen())

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in input fields"""
        if event.input.id == "password-input":
            self.action_connect()
