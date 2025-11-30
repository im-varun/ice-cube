"""
Analytics Screen - Pre-defined queries with controller integration
Displays real results from database via QueryController
"""

from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Input, Static

from query_registry import Query
from ui.interfaces import UIRequest

from ..widgets.query_card import QueryCard


class AnalyticsScreen(Screen):
    """Results screen with pre-defined queries using QueryController"""

    BINDINGS = [("escape", "dismiss", "Return"), ("ctrl+q", "quit", "Quit")]

    def __init__(self, query_id: str = Query.PLAY_TYPES.value.id):
        super().__init__()
        self.query_id = query_id
        self.query_info = Query.get_info(query_id)

    def compose(self) -> ComposeResult:
        yield Header()

        # ────────────────────────────────────────────────────────────────
        # MAIN LAYOUT
        # ────────────────────────────────────────────────────────────────
        with Horizontal():
            with Vertical(classes="sidebar"):
                yield Static("PRE-DEFINED QUERIES", classes="sidebar-title")

                # ONE QueryCard per row
                with ScrollableContainer(id="query-container"):
                    for query_info in Query.list_queries():
                        yield QueryCard(query_info.value.title, query_info.value.id)

            # RIGHT Column: Title + content (input form OR results table)
            with Vertical(classes="content-area"):
                # Dynamic title
                yield Static(self.query_info.title, classes="content-title")

                # Show description
                yield Static(self.query_info.description, classes="query-description")

                # Conditional content based on needs_payload
                if self.query_info.needs_payload:
                    # Show input form
                    with ScrollableContainer(id="input-form", classes="input-form"):
                        yield Static("Enter Parameters:", classes="form-label")

                        # Create input fields based on payload_labels
                        for label in self.query_info.payload_labels:
                            yield Static(f"{label}:", classes="input-label")
                            yield Input(
                                placeholder=f"Enter {label}",
                                id=f"input-{label.replace(' ', '-')}",
                                classes="param-input",
                            )

                        yield Button("Submit Query", id="submit-btn", variant="primary")

                # Results table (always present, but may start hidden for payload queries)
                with ScrollableContainer(id="results-container"):
                    yield DataTable(id="results-table")

        yield Footer()

    def on_mount(self) -> None:
        """Load query results when screen is mounted (only for non-payload queries)"""
        if not self.query_info.needs_payload:
            self.load_query_results(payload={})

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle submit button press for payload queries"""
        if event.button.id == "submit-btn":
            # Collect input values
            payload = {}
            for label in self.query_info.payload_labels:
                input_id = f"input-{label.replace(' ', '-')}"
                try:
                    input_widget = self.query_one(f"#{input_id}", Input)
                    value = input_widget.value.strip()

                    # Try to convert to int if it looks like a number
                    if value.isdigit():
                        payload[label.replace(" ", "_")] = int(value)
                    else:
                        payload[label.replace(" ", "_")] = value
                except Exception:
                    pass

            # Execute query with payload
            self.load_query_results(payload=payload)

    def load_query_results(self, payload: dict) -> None:
        """Execute the current query and display results"""
        if not hasattr(self.app, "controller") or not self.app.controller:
            self.show_error("No controller available")
            return

        table = self.query_one("#results-table", DataTable)
        table.clear(columns=True)

        try:
            # Create request based on query_id
            request = UIRequest(action=self.query_id, payload=payload)

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
