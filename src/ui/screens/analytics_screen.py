"""
Analytics Screen - Pre-defined queries with controller integration
Displays real results from database via QueryController
"""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Input, Static

from query_registry import Query
from ui.interfaces import UIRequest

from ..widgets.query_card import QueryCard


class AnalyticsScreen(Screen):
    """Results screen with pre-defined queries using QueryController"""

    CSS = """
    AnalyticsScreen {
        background: #050a15;
    }

    .sidebar {
        width: 25%;
        background: #0d2847;
        border-right: tall #00d4ff;
        height: 100%;
        padding-right: 2;
    }

    .sidebar-title {
        background: #1e3a5f;
        color: #00ffff;
        padding: 1;
        text-align: center;
        text-style: bold;
    }

    .content-area {
        padding: 0 1;
        height: 100%;
    }

    .content-title {
        text-style: bold;
        color: #00ffff;
        margin-top: 1;
        margin-bottom: 0;
    }

    .query-description {
        color: #8899a6;
        margin-bottom: 1;
    }

    .input-form {
        height: auto;
        layout: horizontal;
        margin-bottom: 1;
        border: solid #1e4d7a;
        padding: 1;
        background: #0a1525;
    }

    .input-group {
        width: 1fr;
        margin-right: 1;
        height: auto;
    }

    .input-label {
        color: #00d4ff;
        margin-bottom: 0;
    }

    .param-input {
        border: solid #1e4d7a;
        background: #050a15;
        color: #ffffff;
    }

    .param-input:focus {
        border: solid #00ffff;
    }

    #submit-btn {
        margin: 0;
        background: #1e3a5f;
        color: #00ffff;
        border: solid #00d4ff;
        width: 100%;
    }

    #submit-btn:hover {
        background: #00d4ff;
        color: #050a15;
        text-style: bold;
    }

    #results-container {
        height: 1fr;
        border: solid #1a3050;
        background: #0a1525;
    }

    DataTable {
        scrollbar-color: #00d4ff #0a1525;
    }
    """

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
                    with Container(classes="input-form"):
                        # Create input fields based on payload_labels
                        for label in self.query_info.payload_labels:
                            with Vertical(classes="input-group"):
                                yield Static(f"{label}:", classes="input-label")
                                yield Input(
                                    placeholder=f"{label}",
                                    id=f"input-{label.replace(' ', '-')}",
                                    classes="param-input",
                                )

                        # Submit Button
                        with Vertical(classes="input-group"):
                            yield Static("", classes="input-label")  # Spacer
                            yield Button("Submit", id="submit-btn")

                # Results table (always present, but may start hidden for payload queries)
                with Container(id="results-container"):
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

    # def action_dismiss(self) -> None:
