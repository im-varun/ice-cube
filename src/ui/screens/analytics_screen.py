"""
Analytics Screen - Pre-defined queries with controller integration
Displays real results from database via QueryController
"""

from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Static

from query_registry import Query
from ui.interfaces import UIRequest

from ..widgets.query_card import QueryCard


class AnalyticsScreen(Screen):
    """Results screen with pre-defined queries using QueryController"""

    BINDINGS = [("escape", "dismiss", "Return"), ("ctrl+q", "quit", "Quit")]

    def __init__(self, query_id: str = Query.PLAY_TYPES.value.id):
        super().__init__()
        self.query_id = query_id

    def compose(self) -> ComposeResult:
        yield Header()

        # ────────────────────────────────────────────────────────────────
        # MAIN LAYOUT
        # ────────────────────────────────────────────────────────────────
        with Horizontal():
            with Vertical(classes="sidebar"):
                yield Static("PRE-DEFINED QUERIES", classes="sidebar-title")

                # ONE QueryCard per row
                for query_info in Query.list_queries():
                    yield QueryCard(query_info.value.title, query_info.value.id)

            # ── RIGHT CONTENT: Title + scrollable table only ───────────
            with Vertical(classes="content-area"):
                # Dynamic title
                yield Static(Query.get_info(self.query_id).title, classes="content-title")

                # Scrollable results container
                with ScrollableContainer():
                    yield DataTable(id="results-table")

        yield Footer()

    def on_mount(self) -> None:
        """Load query results when screen is mounted"""
        self.load_query_results()

    def load_query_results(self) -> None:
        """Execute the current query and display results"""
        if not hasattr(self.app, "controller") or not self.app.controller:
            self.show_error("No controller available")
            return

        table = self.query_one("#results-table", DataTable)
        table.clear(columns=True)

        try:
            # Create request based on query_id
            request = UIRequest(action=self.query_id, payload={})

            # Execute query via controller
            response = self.app.controller.handle_request(request)

            if response.success and response.data:
                # Add columns from first row
                if len(response.data) > 0:
                    headers = list(response.data[0].keys())
                    for header in headers:
                        table.add_column(str(header), key=str(header))

                    # Add rows
                    for row in response.data:
                        values = [str(row.get(h, "")) for h in headers]
                        table.add_row(*values)
                else:
                    table.add_column("Message")
                    table.add_row("0 results")
            else:
                # Show error in table
                table.add_column("Error")
                table.add_row(response.message)

        except Exception as e:
            # Show exception in table
            table.add_column("Error")
            table.add_row(f"Exception: {str(e)}")

    def show_error(self, message: str) -> None:
        """Display error message in table"""
        table = self.query_one("#results-table", DataTable)
        table.clear(columns=True)
        table.add_column("Error")
        table.add_row(message)

    # ────────────────────────────────────────────────────────────────
    # Navigation
    # ────────────────────────────────────────────────────────────────
    def on_query_card_selected(self, event: QueryCard.Selected) -> None:
        """Switch to new result when a sidebar query is clicked"""
        self.app.push_screen(AnalyticsScreen(event.query_id))

    def action_dismiss(self) -> None:
        self.dismiss()
