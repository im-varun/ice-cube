"""
Enhanced Data Table Widget - Custom table with additional features
"""

from typing import Any, Dict, List, Optional

from textual.message import Message
from textual.widgets import DataTable


class EnhancedDataTable(DataTable):
    """
    Enhanced DataTable with additional features:
    - Row highlighting
    - Custom cell formatting
    - Export functionality
    - Search/filter
    """

    class RowSelected(Message):
        """Message emitted when a row is selected"""

        def __init__(self, row_index: int, row_data: Dict[str, Any]):
            super().__init__()
            self.row_index = row_index
            self.row_data = row_data

    def __init__(self, *args, highlight_rows: Optional[List[int]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.highlight_rows = highlight_rows or []
        self._row_data: List[Dict[str, Any]] = []
        self.cursor_type = "row"

    def add_data_row(self, data: Dict[str, Any], *cells, highlight: bool = False):
        """
        Add a row with associated data

        Args:
            data: Dictionary containing row data
            cells: Cell values to display
            highlight: Whether to highlight this row
        """
        row_key = self.add_row(*cells)
        self._row_data.append(data)

        if highlight:
            row_index = len(self._row_data) - 1
            self.highlight_rows.append(row_index)

        return row_key

    def get_row_data(self, row_index: int) -> Optional[Dict[str, Any]]:
        """Get the data associated with a row"""
        if 0 <= row_index < len(self._row_data):
            return self._row_data[row_index]
        return None

    def on_data_table_row_selected(self, event) -> None:
        """Handle row selection"""
        row_index = event.cursor_row
        row_data = self.get_row_data(row_index)
        if row_data:
            self.post_message(self.RowSelected(row_index, row_data))

    def clear_table(self) -> None:
        """Clear all rows and data"""
        self.clear()
        self._row_data = []
        self.highlight_rows = []

    def export_to_csv(self) -> str:
        """
        Export table data to CSV format

        Returns:
            CSV formatted string
        """
        if not self._row_data:
            return ""

        # Get column headers
        headers = list(self._row_data[0].keys())
        csv_lines = [",".join(headers)]

        # Add data rows
        for row in self._row_data:
            row_values = [str(row.get(h, "")) for h in headers]
            csv_lines.append(",".join(row_values))

        return "\n".join(csv_lines)

    def filter_rows(self, filter_func) -> None:
        """
        Filter rows based on a function

        Args:
            filter_func: Function that takes row data and returns True to keep
        """
        self.clear()

        filtered_data = [row for row in self._row_data if filter_func(row)]

        # Re-add filtered rows
        for data in filtered_data:
            # Extract cell values from data
            cells = list(data.values())
            self.add_row(*cells)

    def search(self, query: str, columns: Optional[List[str]] = None) -> List[int]:
        """
        Search for query in specified columns

        Args:
            query: Search string
            columns: List of column names to search in (None = all columns)

        Returns:
            List of matching row indices
        """
        query = query.lower()
        matching_rows = []

        for i, row in enumerate(self._row_data):
            search_values = []

            if columns:
                search_values = [str(row.get(col, "")) for col in columns]
            else:
                search_values = [str(v) for v in row.values()]

            # Check if query appears in any search value
            if any(query in str(v).lower() for v in search_values):
                matching_rows.append(i)

        return matching_rows

    def sort_by_column(self, column_name: str, reverse: bool = False) -> None:
        """
        Sort table by a specific column

        Args:
            column_name: Name of column to sort by
            reverse: Sort in descending order if True
        """
        if not self._row_data or column_name not in self._row_data[0]:
            return

        # Sort the data
        sorted_data = sorted(self._row_data, key=lambda x: x.get(column_name, ""), reverse=reverse)

        # Clear and re-populate table
        self.clear()
        self._row_data = []

        for data in sorted_data:
            cells = list(data.values())
            self.add_data_row(data, *cells)

    def get_column_stats(self, column_name: str) -> Dict[str, Any]:
        """
        Get statistics for a numeric column

        Args:
            column_name: Name of column to analyze

        Returns:
            Dictionary with min, max, avg, sum, count
        """
        if not self._row_data or column_name not in self._row_data[0]:
            return {}

        values = []
        for row in self._row_data:
            val = row.get(column_name)
            try:
                values.append(float(val))
            except (ValueError, TypeError):
                continue

        if not values:
            return {}

        return {
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "sum": sum(values),
            "count": len(values),
        }

    def highlight_row_by_value(self, column_name: str, value: Any) -> None:
        """
        Highlight rows where column equals value

        Args:
            column_name: Column to check
            value: Value to match
        """
        for i, row in enumerate(self._row_data):
            if row.get(column_name) == value:
                if i not in self.highlight_rows:
                    self.highlight_rows.append(i)
