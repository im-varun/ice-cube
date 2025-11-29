"""
Query Screen - SQL Query Runner Interface
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Select,
    Static,
    TextArea,
)


class QueryScreen(Screen):
    """SQL Query Runner Screen"""

    CSS = """
    QueryScreen {
        align: center middle;
    }

    .content-area {
        width: 90%;
        height: 90%;
        border: solid $accent;
        padding: 1 2;
        background: $surface;
        overflow: hidden;
    }

    .content-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }

    .input-section, .results-section {
        height: auto;
        margin-bottom: 1;
    }

    .label {
        margin: 1 0;
    }

    .full-width {
        width: 100%;
    }

    #columns-grid {
        layout: grid;
        grid-size: 4;
        grid-gutter: 1;
        height: auto;
        margin: 1 0;
    }

    .column-btn {
        width: 100%;
        border: solid $primary-background;
        height: 3;
        padding: 0;
    }

    .column-btn.selected {
        background: $accent;
        color: $text;
        border: solid $accent-lighten-2;
        text-style: bold;
        height: 3;
    }

    .bordered-input, .bordered-btn {
        border: solid $primary;
        width: 100%;
        margin-top: 1;
    }
    """

    BINDINGS = [
        Binding("ctrl+e", "execute_query", "Execute", show=True),
        Binding("ctrl+l", "clear_query", "Clear", show=True),
        Binding("escape", "back", "Back", show=True),
    ]

    TABLES = [
        ("Players", "players"),
        ("Teams", "teams"),
        ("Games", "games"),
        ("Stats", "stats"),
    ]

    COLUMNS = [
        ("ID", "id"),
        ("Name", "name"),
        ("Team ID", "team_id"),
        ("Score", "score"),
        ("Date", "date"),
        ("Position", "position"),
        ("Age", "age"),
        ("Height", "height"),
        ("Weight", "weight"),
        ("Country", "country"),
        ("Jersey", "jersey_number"),
        ("Active", "is_active"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with VerticalScroll(classes="content-area"):
            yield Static("SQL Query Runner", classes="content-title")

            with Vertical(classes="input-section"):
                yield Static("Build your Query", classes="highlight-magenta")

                yield Static("Select Table:", classes="label")
                yield Select(
                    self.TABLES, prompt="Choose a table...", id="table-select", classes="full-width"
                )

                yield Static("Select Columns:", classes="label")
                with Grid(id="columns-grid"):
                    for name, val in self.COLUMNS:
                        btn = Button(name, id=f"col-{val}", classes="column-btn")
                        btn.column_value = val
                        yield btn

                yield Static("Where Condition (Optional):", classes="label")
                yield Input(
                    placeholder="e.g., team_id = 1",
                    id="constraint-input",
                    classes="bordered-input full-width",
                )

                yield Button(
                    "Execute Query", variant="success", id="execute-btn", classes="bordered-btn"
                )

            with Vertical(classes="results-section"):
                yield Static("Results", classes="content-title")
                results_area = TextArea(
                    "Query results will be displayed here.", id="results-output", read_only=True
                )
                results_area.styles.height = "1fr"
                results_area.styles.border = ("solid", "green")
                yield results_area

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "execute-btn":
            self.action_execute_query()
        elif "column-btn" in event.button.classes:
            event.button.toggle_class("selected")

    def action_execute_query(self) -> None:
        table_select = self.query_one("#table-select", Select)
        constraint_input = self.query_one("#constraint-input", Input)
        results_output = self.query_one("#results-output", TextArea)

        selected_table = table_select.value
        selected_columns = [
            btn.column_value
            for btn in self.query(Button)
            if "column-btn" in btn.classes and "selected" in btn.classes
        ]
        constraint = constraint_input.value.strip()

        if not selected_table:
            results_output.text = "Error: Please select a table."
            return
        if not selected_columns:
            results_output.text = "Error: Please select at least one column."
            return

        query = f"SELECT {', '.join(selected_columns)} FROM {selected_table}"
        if constraint:
            query += f" WHERE {constraint}"
        query += ";"

        results_output.text = f"Executing query:\n{query}\n\n[Results would appear here]"

    def action_clear_query(self) -> None:
        self.query_one("#table-select", Select).value = Select.BLANK
        self.query_one("#constraint-input", Input).value = ""
        for btn in self.query(Button):
            if "column-btn" in btn.classes:
                btn.remove_class("selected")
        self.query_one("#results-output", TextArea).text = "Query results will be displayed here."

    def action_back(self) -> None:
        self.app.pop_screen()
