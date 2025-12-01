"""
Search Screen: Custom SQL Query Builder
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    Select,
    SelectionList,
)
from textual.widgets.selection_list import Selection

from ui.interfaces import UIRequest

# schema based on sql/schema.sql
DB_SCHEMA = {
    "game": [
        "game_id",
        "season",
        "type",
        "date_time_GMT",
        "away_team_id",
        "home_team_id",
        "away_goals",
        "home_goals",
        "outcome",
        "home_rink_side_start",
        "venue",
    ],
    "game_goalie_stats": [
        "game_id",
        "player_id",
        "team_id",
        "timeOnIce",
        "assists",
        "goals",
        "pim",
        "shots",
        "saves",
        "powerPlaySaves",
        "shortHandedSaves",
        "evenSaves",
        "shortHandedShotsAgainst",
        "evenShotsAgainst",
        "powerPlayShotsAgainst",
        "decision",
        "savePercentage",
        "powerPlaySavePercentage",
        "evenStrengthSavePercentage",
    ],
    "game_goals": [
        "game_goal_id",
        "play_id",
        "strength",
        "gameWinningGoal",
        "emptyNet",
    ],
    "game_officials": [
        "game_id",
        "official_name",
        "official_type",
    ],
    "game_penalties": [
        "play_id",
        "penaltySeverity",
        "penaltyMinutes",
    ],
    "game_plays": [
        "play_id",
        "game_id",
        "team_id_for",
        "team_id_against",
        "event",
        "secondaryType",
        "x",
        "y",
        "period",
        "periodType",
        "periodTime",
        "periodTimeRemaining",
        "dateTime",
        "goals_away",
        "goals_home",
        "description",
        "st_x",
        "st_y",
    ],
    "game_plays_players": [
        "play_id",
        "game_id",
        "player_id",
        "playerType",
    ],
    "game_scratches": [
        "game_id",
        "team_id",
        "player_id",
    ],
    "game_shifts": [
        "game_id",
        "player_id",
        "period",
        "shift_start",
        "shift_end",
    ],
    "game_skater_stats": [
        "game_id",
        "player_id",
        "team_id",
        "timeOnIce",
        "assists",
        "goals",
        "shots",
        "hits",
        "powerPlayGoals",
        "powerPlayAssists",
        "penaltyMinutes",
        "faceOffWins",
        "faceoffTaken",
        "takeaways",
        "giveaways",
        "shortHandedGoals",
        "shortHandedAssists",
        "blocked",
        "plusMinus",
        "evenTimeOnIce",
        "shortHandedTimeOnIce",
        "powerPlayTimeOnIce",
    ],
    "game_teams_stats": [
        "game_id",
        "team_id",
        "HoA",
        "won",
        "settled_in",
        "head_coach",
        "goals",
        "shots",
        "hits",
        "pim",
        "powerPlayOpportunities",
        "powerPlayGoals",
        "faceOffWinPercentage",
        "giveaways",
        "takeaways",
        "blocked",
        "startRinkSide",
    ],
    "player_info": [
        "player_id",
        "firstName",
        "lastName",
        "nationality",
        "birthCity",
        "primaryPosition",
        "birthDate",
        "birthStateProvince",
        "height",
        "weight",
        "shootsCatches",
    ],
    "team_info": [
        "team_id",
        "shortName",
        "teamName",
        "abbreviation",
    ],
}


class SearchScreen(Screen):
    """Screen for building custom SQL queries safely."""

    CSS = """
    SearchScreen {
        background: #050a15;
    }

    .control-panel {
        height: auto;
        background: #0d2847;
        border: tall #00d4ff;
        padding: 0 1;
        margin: 0 1;
        layout: vertical;
    }

    .top-controls {
        height: auto;
        layout: horizontal;
        margin-bottom: 1;
        width: 100%;
    }

    .input-group {
        height: auto;
        margin-right: 1;
    }

    #table-group {
        width: 25%;
    }

    #where-group {
        width: 59%;
    }

    #btn-group {
        width: 15%;
        align-vertical: bottom;
    }

    Label {
        color: #00ffff;
        margin-bottom: 0;
    }

    Select {
        width: 100%;
    }

    SelectionList {
        height: 8;
        border: solid #1e4d7a;
        background: #0a1525;
        scrollbar-color: #00d4ff #0a1525;
        margin-bottom: 1;
    }

    Input {
        border: solid #1e4d7a;
        background: #0a1525;
        color: #ffffff;
    }

    Input:focus {
        border: solid #00ffff;
    }

    .search-btn {
        width: 100%;
        background: #1e3a5f;
        color: #00ffff;
        border: solid #00d4ff;
    }

    .search-btn:hover {
        background: #00d4ff;
        color: #0a0f1c;
        text-style: bold;
    }

    .results-container {
        height: 1fr;
        border: solid #1a3050;
        margin: 0 1 1 1;
        background: #0a1525;
    }

    DataTable {
        height: 100%;
        scrollbar-color: #00d4ff #0a1525;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(classes="control-panel"):
            # Top Controls: Table, WHERE, Search
            with Container(classes="top-controls"):
                # Table Selection
                with Vertical(classes="input-group", id="table-group"):
                    yield Label("Select Table:")
                    yield Select(
                        [(table, table) for table in DB_SCHEMA.keys()],
                        prompt="Table...",
                        id="table-select",
                    )

                # WHERE Clause
                with Vertical(classes="input-group", id="where-group"):
                    yield Label("WHERE Clause (Optional):")
                    yield Input(
                        placeholder="e.g. nationality = 'CAN'", id="where-input"
                    )

                # Search Button
                with Vertical(classes="input-group", id="btn-group"):
                    yield Label("") # Spacer
                    yield Button("Search", id="btn-search", classes="search-btn")

            # Column Selection (Full width below top controls)
            with Vertical(classes="input-group"):
                yield Label("Select Columns:")
                yield SelectionList(id="column-select")

        with Container(classes="results-container"):
            yield DataTable(id="results-table", zebra_stripes=True)

        yield Footer()

    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle table selection change."""
        if event.select.id == "table-select":
            table_name = str(event.value)
            self._update_columns(table_name)

    def _update_columns(self, table_name: str) -> None:
        """Update the column selection list based on the selected table."""
        column_list = self.query_one("#column-select", SelectionList)
        column_list.clear_options()

        if table_name in DB_SCHEMA:
            columns = DB_SCHEMA[table_name]
            # Select all by default or let user choose? Let's select all by default for convenience
            selections = [Selection(col, col, initial_state=True) for col in columns]
            column_list.add_options(selections)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle search button press."""
        if event.button.id == "btn-search":
            self._perform_search()

    def _perform_search(self) -> None:
        """Construct and execute the query."""
        table_select = self.query_one("#table-select", Select)
        column_list = self.query_one("#column-select", SelectionList)
        where_input = self.query_one("#where-input", Input)
        self.query_one("#results-table", DataTable)

        # Validation
        if table_select.value == Select.BLANK:
            self.notify("Please select a table.", severity="warning")
            return

        selected_columns = column_list.selected
        if not selected_columns:
            self.notify("Please select at least one column.", severity="warning")
            return

        where_clause = where_input.value.strip()

        # Construct Query
        cols_str = ", ".join(selected_columns)
        query = f"SELECT DISTINCT {cols_str} FROM {table_select.value}"

        if where_clause:
            query += f" WHERE {where_clause}"

        # Execute
        self.notify(f"Executing: {query}", severity="information")

        request = UIRequest(action="custom", payload={"query": query})
        response = self.app.controller.handle_request(request)

        if response.success:
            self._display_results(response.data, selected_columns)
        else:
            self.notify(f"Query failed: {response.message}", severity="error")

    def _display_results(self, data: list[dict] | int, columns: list[str]) -> None:
        """Populate the DataTable with results."""
        table = self.query_one("#results-table", DataTable)
        table.clear(columns=True)

        if isinstance(data, int):
            self.notify("Database returned an error code.", severity="error")
            return

        if not data:
            self.notify("No results found.", severity="warning")
            return

        # Add columns
        table.add_columns(*columns)

        # Add rows
        rows = []
        for row in data:
            # Ensure order matches selected columns
            row_data = [str(row.get(col, "")) for col in columns]
            rows.append(row_data)

        table.add_rows(rows)
        self.notify(f"Loaded {len(rows)} rows.", severity="information")
