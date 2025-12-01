"""
Home Screen: NHL Dashboard
"""

import os
import sys

ROOT_DIR_NAME = "ice-cube"
curr_path = os.path.dirname(__file__)
idx = curr_path.find(ROOT_DIR_NAME) + len(ROOT_DIR_NAME)
ROOT_PATH = curr_path[:idx]
LIB_PATH = os.path.join(ROOT_PATH, "lib")
if LIB_PATH != sys.path[0]:
    print("inserting to the path")
    sys.path.insert(0, LIB_PATH)

from textual.app import ComposeResult
from textual.containers import Container, Grid, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Static

from ui.interfaces import UIRequest


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
        border: solid #00d4ff;
        padding: 3 5;
    }

    .hero-container:hover {
        border: solid #00ffff;
        background: #0f2e52;
    }

    .hero-title {
        color: #00ffff;
        text-style: bold;
        text-align: center;
        margin-bottom: 2;
        text-opacity: 100%;
    }

    .hero-subtitle {
        color: #8bb4e8;
        text-align: center;
        text-style: italic;
    }

    /* ══════════════════════════════════════════════════════════
       ACTION CARDS SECTION
       ══════════════════════════════════════════════════════════ */

    .cards-container {
        width: 100%;
        height: auto;
        padding: 2 0;
    }

    .action-grid {
        layout: grid;
        grid-size: 2 1;
        grid-gutter: 5 3;
        height: auto;
        width: 100%;
    }

    .action-card {
        height: auto;
        min-height: 20;
        background: #0c1a2e;
        border: solid #1e3a5f;
        padding: 3 3;
        margin: 0;
    }

    .action-card:hover {
        border: solid #00ffff;
        background: #1a3050;
    }

    .card-content {
        height: auto;
        width: 100%;
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
        color: #8bb4e8;
        text-align: center;
        margin-bottom: 3;
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
        color: #050a15;
        text-style: bold;
    }

    /* ══════════════════════════════════════════════════════════
       HEADER & FOOTER
       ══════════════════════════════════════════════════════════ */

    Footer {
        background: #0a1525;
        color: #6b9bd1;
    }

    Footer:hover {
        color: #8bb4e8;
    }

    Header {
        background: #0a1525;
        color: #00ffff;
    }

    Header:hover {
        color: #00d4ff;
    }
    """

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()

        # ══════════════════════════════════════════════════════════
        # HERO BANNER
        # ══════════════════════════════════════════════════════════
        with Container(classes="hero-container"):
            yield Static("❄️  I C E   C U B E  ❄️", classes="hero-title")
            yield Static("Slice through NHL data like a pro skater.", classes="hero-subtitle")

        # ══════════════════════════════════════════════════════════
        # ACTION CARDS WITH BUTTONS
        # ══════════════════════════════════════════════════════════
        with Container(classes="cards-container"):
            with Grid(classes="action-grid"):
                # CARD 1: Custom Query
                with Container(classes="action-card"):
                    with Vertical(classes="card-content"):
                        yield Static("🏒  THE RINK", classes="card-icon")
                        yield Static("Raw Data Lookup", classes="card-title")
                        yield Static(
                            "Skate through the raw tables.\nBuild your own plays from scratch.",
                            classes="card-desc",
                        )
                        yield Button("Enter the Rink", id="btn-custom", classes="card-button")

                # CARD 2: Pre-defined Queries
                with Container(classes="action-card"):
                    with Vertical(classes="card-content"):
                        yield Static("📋  THE PLAYBOOK", classes="card-icon")
                        yield Static("Pro Analytics", classes="card-title")
                        yield Static(
                            "Winning strategies and deep insights.\nNo coaching license required.",
                            classes="card-desc",
                        )
                        yield Button(
                            "Open Playbook", id="btn-predefined", classes="card-button"
                        )

        yield Footer()

    # ══════════════════════════════════════════════════════════
    # BUTTON HANDLERS
    # ══════════════════════════════════════════════════════════

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks"""
        if event.button.id == "btn-custom":
            self.action_table_lookup()
        elif event.button.id == "btn-predefined":
            self.action_predefined_queries()

    # ══════════════════════════════════════════════════════════
    # NAVIGATION ACTIONS
    # ══════════════════════════════════════════════════════════

    def action_table_lookup(self) -> None:
        """Launch Custom Query Engine"""
        try:
            from ui.screens.search_screen import SearchScreen

            self.notify("Launching Search Engine", severity="information")
            self.app.push_screen(SearchScreen())
        except Exception as e:
            self.notify(f"Error loading Query Screen: {e}", severity="error")

    def action_predefined_queries(self) -> None:
        """Launch Signature Queries Dashboard"""
        try:
            from ui.screens.analytics_screen import AnalyticsScreen

            self.notify("📊 Loading Signature Queries...", severity="information")
            self.app.push_screen(AnalyticsScreen())
        except Exception as e:
            self.notify(f"Error loading Results Screen: {e}", severity="error")

    def action_disconnect(self) -> None:
        """Disconnect from database"""
        request = UIRequest(action="disconnect_db", params={})
        response = self.app.controller.handle_request(request)
        if response.success:
            self.notify("❄️ Database disconnected successfully", severity="information")
            self.app.set_db_status(False)
            self.app.pop_screen()
        else:
            self.notify(f"⚠️ Disconnect failed: {response.message}", severity="error")
