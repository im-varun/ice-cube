"""
Query Screen - SQL Query Runner Interface
"""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Static, TextArea


class QueryScreen(Screen):
    """SQL Query Runner Screen"""

    BINDINGS = [
        Binding("ctrl+e", "execute_query", "Execute", show=True),
        Binding("ctrl+l", "clear_query", "Clear", show=True),
        Binding("escape", "back", "Back", show=True),
    ]

    def compose(self) -> ComposeResult:
        """Compose the query screen layout"""
        yield Header()

        with Container(classes="content-area"):
            # Title
            yield Static("SQL Query Runner", classes="content-title")

            # Query input section
            with Vertical():
                yield Static("Enter SQL Query", classes="highlight-magenta")

                query_area = TextArea(
                    "e.g., SELECT * FROM players WHERE team = 'TBL';",
                    id="query-input",
                    language="sql",
                )
                query_area.styles.height = 20
                query_area.styles.margin = (1, 0)
                yield query_area

                # Execute button
                yield Button("Execute Query", variant="success", id="execute-btn")

            # Results section
            with Vertical():
                yield Static("Results", classes="content-title")

                results_area = TextArea(
                    "Query results will be displayed here.", id="results-output", read_only=True
                )
                results_area.styles.height = 30
                results_area.styles.margin = (1, 0)
                yield results_area

        # Footer with shortcuts
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press"""
        if event.button.id == "execute-btn":
            self.action_execute_query()

    def action_execute_query(self) -> None:
        """Execute the SQL query"""
        query_input = self.query_one("#query-input", TextArea)
        results_output = self.query_one("#results-output", TextArea)

        query = query_input.text

        if not query or query.strip() == "":
            results_output.text = "Error: Please enter a query."
            return

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
        query_input = self.query_one("#query-input", TextArea)
        results_output = self.query_one("#results-output", TextArea)

        query_input.text = ""
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
