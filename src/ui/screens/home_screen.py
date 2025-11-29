"""
Home Screen – Stunning, Professional NHL Analytics Dashboard
Polished design with working navigation
100% Textual-compatible CSS
"""

import os
import sys

# Add lib/ directory for textual
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "lib"))
# Add parent directory to access shared
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, Grid
from textual.screen import Screen
from textual.widgets import Static, Footer, Header, Button
from textual.binding import Binding
from ui.interfaces import ControllerInterface, UIRequest


class HomeScreen(Screen):
    """Professional IceCube Home Screen with Working Navigation"""

    CSS = """
    HomeScreen {
        background: #050a15;
    }

    /* ══════════════════════════════════════════════════════════
       HERO SECTION - Top Banner
       ══════════════════════════════════════════════════════════ */

    .hero-container {
        height: auto;
        width: 100%;
        background: #0d2847;
        border: tall #00d4ff;
        padding: 3 4;
        margin-bottom: 2;
    }

    .hero-title {
        color: #00ffff;
        text-style: bold;
        text-align: center;
        margin-bottom: 1;
    }

    .hero-subtitle {
        color: #6b9bd1;
        text-align: center;
        margin-bottom: 1;
    }

    .hero-season {
        color: #00d4ff;
        text-align: center;
        text-style: bold italic;
        background: #0f1f3a;
        border: solid #1e4d7a;
        padding: 1 2;
        margin: 1 0;
        width: auto;
    }

    /* ══════════════════════════════════════════════════════════
       FEATURE BANNER
       ══════════════════════════════════════════════════════════ */

    .feature-banner {
        height: auto;
        background: #0a1525;
        border: solid #1a3050;
        padding: 2 3;
        margin: 2 8;
    }

    .feature-text {
        color: #8bb4e8;
        text-align: center;
        margin-bottom: 1;
    }

    .feature-highlight {
        color: #00ffff;
        text-style: bold;
        text-align: center;
    }

    /* ══════════════════════════════════════════════════════════
       ACTION CARDS SECTION
       ══════════════════════════════════════════════════════════ */

    .cards-container {
        width: 100%;
        height: auto;
        padding: 3 8;
    }

    .action-grid {
        layout: grid;
        grid-size: 2 1;
        grid-gutter: 4 2;
        height: auto;
        width: 100%;
    }

    .action-card {
        height: auto;
        min-height: 20;
        background: #0c1a2e;
        border: heavy #1e3a5f;
        padding: 3 3;
    }

    .action-card:hover {
        border: heavy #00ffff;
        background: #162d4a;
    }

    .card-content {
        height: auto;
        width: 100%;
        align: center middle;
    }

    .card-icon {
        color: #00d4ff;
        text-style: bold;
        text-align: center;
        margin-bottom: 2;
    }

    .card-title {
        color: #ffffff;
        text-style: bold;
        text-align: center;
        margin-bottom: 2;
    }

    .card-desc {
        color: #7a9bc5;
        text-align: center;
        margin-bottom: 2;
    }

    .card-badge {
        background: #00d4ff;
        color: #0a0f1c;
        padding: 1 2;
        text-style: bold;
        text-align: center;
        border: solid #00ffff;
        margin: 2 0;
        width: auto;
    }

    .card-button {
        width: 100%;
        margin-top: 2;
        background: #1e3a5f;
        color: #00ffff;
        border: solid #00d4ff;
    }

    .card-button:hover {
        background: #00d4ff;
        color: #0a0f1c;
        text-style: bold;
    }

    .card-keyinfo {
        color: #4a7ba7;
        text-align: center;
        margin-top: 1;
        text-style: italic;
    }

    /* ══════════════════════════════════════════════════════════
       STATS BAR
       ══════════════════════════════════════════════════════════ */

    .stats-bar {
        layout: horizontal;
        height: auto;
        background: #08131f;
        border: solid #1a2d45;
        margin: 3 8 2 8;
        padding: 2 2;
    }

    .stat-item {
        width: 1fr;
        text-align: center;
        color: #6b9bd1;
    }

    .stat-value {
        color: #00ffff;
        text-style: bold;
    }

    /* ══════════════════════════════════════════════════════════
       HEADER & FOOTER
       ══════════════════════════════════════════════════════════ */

    Footer {
        background: #0a1525;
        color: #6b9bd1;
    }

    Header {
        background: #0a1525;
        color: #00ffff;
    }
    """

    BINDINGS = [
        Binding("c", "custom_query", "Custom Query", show=True, priority=True),
        Binding("p", "predefined_queries", "Signature Queries", show=True, priority=True),
        Binding("d", "disconnect", "Disconnect", show=True),
        Binding("ctrl+q", "quit", "Quit", show=True),
    ]

    def __init__(self, controller: ControllerInterface):
        super().__init__()
        self.controller = controller

    def compose(self) -> ComposeResult:
        yield Header()

        # ══════════════════════════════════════════════════════════
        # HERO BANNER
        # ══════════════════════════════════════════════════════════
        with Container(classes="hero-container"):
            yield Static("❄️  I C E C U B E  ❄️", classes="hero-title")
            yield Static("A Crystalline Database Management System", classes="hero-subtitle")

        # ══════════════════════════════════════════════════════════
        # ACTION CARDS WITH BUTTONS
        # ══════════════════════════════════════════════════════════
        with Container(classes="cards-container"):
            with Grid(classes="action-grid"):
                # CARD 1: Custom Query
                with Container(classes="action-card"):
                    with Vertical(classes="card-content"):
                        yield Static("⚙️  SQL", classes="card-icon")
                        yield Static("Custom Query Engine", classes="card-title")
                        yield Static(
                            "Write any SQL query with full control.\nPowerful. Flexible. Limitless.",
                            classes="card-desc",
                        )
                        yield Button("Launch Custom Query", id="btn-custom", classes="card-button")

                # CARD 2: Pre-defined Queries
                with Container(classes="action-card"):
                    with Vertical(classes="card-content"):
                        yield Static("🎯  ANALYTICS", classes="card-icon")
                        yield Static("Signature Queries", classes="card-title")
                        yield Static(
                            "12 expert-crafted analytics.\nInstant insights. Zero setup.",
                            classes="card-desc",
                        )
                        yield Button(
                            "Explore Signature Queries", id="btn-predefined", classes="card-button"
                        )

        # ══════════════════════════════════════════════════════════
        # STATS BAR
        # ══════════════════════════════════════════════════════════
        with Horizontal(classes="stats-bar"):
            yield Static("Database: [stat-value]Connected[/]", classes="stat-item", markup=True)
            yield Static("Season: [stat-value]2019-2020[/]", classes="stat-item", markup=True)
            yield Static("Queries: [stat-value]12 Available[/]", classes="stat-item", markup=True)

        yield Footer()

    # ══════════════════════════════════════════════════════════
    # BUTTON HANDLERS
    # ══════════════════════════════════════════════════════════

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks"""
        if event.button.id == "btn-custom":
            self.action_custom_query()
        elif event.button.id == "btn-predefined":
            self.action_predefined_queries()

    # ══════════════════════════════════════════════════════════
    # NAVIGATION ACTIONS
    # ══════════════════════════════════════════════════════════

    def action_custom_query(self) -> None:
        """Launch Custom Query Engine"""
        try:
            from ui.screens.query_screen import QueryScreen

            self.notify("🔧 Launching Custom Query Engine...", severity="information")
            self.app.push_screen(QueryScreen(self.controller))
        except Exception as e:
            self.notify(f"Error loading Query Screen: {e}", severity="error")

    def action_predefined_queries(self) -> None:
        """Launch Signature Queries Dashboard"""
        try:
            from ui.screens.results_screen import ResultsScreen

            self.notify("📊 Loading Signature Queries...", severity="information")
            self.app.push_screen(ResultsScreen("top_scoring"))
        except Exception as e:
            self.notify(f"Error loading Results Screen: {e}", severity="error")

    def action_disconnect(self) -> None:
        """Disconnect from database"""
        request = UIRequest(action="disconnect_db", params={})
        response = self.controller.handle_request(request)
        if response.success:
            self.notify("❄️ Database disconnected successfully", severity="information")
            self.app.set_db_status(False)
            self.app.pop_screen()
        else:
            self.notify(f"⚠️ Disconnect failed: {response.message}", severity="error")
