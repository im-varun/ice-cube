"""
Query Screen - SQL Query Runner Interface
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Static, TextArea, Select, SelectionList, Input, Collapsible


class QueryScreen(Screen):
    """SQL Query Runner Screen"""

    BINDINGS = [
        Binding("ctrl+e", "execute_query", "Execute", show=True),
        Binding("ctrl+l", "clear_query", "Clear", show=True),
        Binding("escape", "back", "Back", show=True),
    ]

    # Mock Data
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
    ]

    def compose(self) -> ComposeResult:
        """Compose the query screen layout"""
        yield Header()

        with Container(classes="content-area"):
            # Title
            yield Static("SQL Query Runner", classes="content-title")

            # Query input section
            with Vertical(classes="input-section"):
                yield Static("Build your Query", classes="highlight-magenta")

                # Table Selection
                yield Static("Select Table:", classes="label")
                yield Select(self.TABLES, prompt="Choose a table...", id="table-select", classes="full-width")

                # Column Selection
                with Collapsible(title="Select Columns", classes="full-width"):
                    yield SelectionList[str](
                        *[(name, val, False) for name, val in self.COLUMNS],
                        id="column-select",
                        classes="scrollable-list"
                    )

                # Constraint Input
                yield Static("Where Condition (Optional):", classes="label")
                yield Input(placeholder="e.g., team_id = 1", id="constraint-input", classes="bordered-input full-width")

                # Execute button
                yield Button("Execute Query", variant="success", id="execute-btn", classes="bordered-btn")

            # Results section
            with Vertical(classes="results-section"):
                yield Static("Results", classes="content-title")

                results_area = TextArea(
                    "Query results will be displayed here.", id="results-output", read_only=True
                )
                # Use relative height or flex to avoid overflow
                results_area.styles.height = "1fr" 
                results_area.styles.border = ("solid", "green")
                yield results_area

        # Footer with shortcuts
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press"""
        if event.button.id == "execute-btn":
            self.action_execute_query()

    def action_execute_query(self) -> None:
        """Execute the SQL query"""
        table_select = self.query_one("#table-select", Select)
        column_select = self.query_one("#column-select", SelectionList)
        constraint_input = self.query_one("#constraint-input", Input)
        results_output = self.query_one("#results-output", TextArea)

        selected_table = table_select.value
        selected_columns = column_select.selected
        constraint = constraint_input.value

        if not selected_table:
            results_output.text = "Error: Please select a table."
            return

        if not selected_columns:
            results_output.text = "Error: Please select at least one column."
            return

        # Construct Query
        cols_str = ", ".join(selected_columns)
        query = f"SELECT {cols_str} FROM {selected_table}"
        
        if constraint and constraint.strip():
            query += f" WHERE {constraint}"
        
        query += ";"

        # TODO: Replace with actual database query execution
        # This is a placeholder - integrate with your database controller
        results_output.text = f"Executing query:\n{query}\n\n[Results would appear here]"

        # Example of how to call the database layer:
        # try:
        #     from controllers.query_controller import QueryController
        #     controller = QueryController()
        #     results = controller.execute_query(query)
        #     results_output.text = self._format_results(results)
        # except Exception as e:
        #     results_output.text = f"Error: {str(e)}"

    def action_clear_query(self) -> None:
        """Clear the query input"""
        table_select = self.query_one("#table-select", Select)
        column_select = self.query_one("#column-select", SelectionList)
        constraint_input = self.query_one("#constraint-input", Input)
        results_output = self.query_one("#results-output", TextArea)

        table_select.value = Select.BLANK
        column_select.deselect_all()
        constraint_input.value = ""
        results_output.text = "Query results will be displayed here."

    def action_back(self) -> None:
        """Go back to home screen"""
        self.app.pop_screen()

    def _format_results(self, results) -> str:
        """Format query results for display"""
        if not results:
            return "No results found."

        # Format as table
        # This is a simple implementation - enhance as needed
        output = []

        if isinstance(results, list) and len(results) > 0:
            # Get column names from first row
            if isinstance(results[0], dict):
                headers = list(results[0].keys())
                output.append(" | ".join(headers))
                output.append("-" * 80)

                for row in results:
                    output.append(" | ".join(str(row.get(h, "")) for h in headers))

        return "\n".join(output)
