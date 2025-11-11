"""
Widgets Module - Reusable UI Components
=======================================

Custom Textual widgets used across multiple screens.

Files:
------
query_card.py
    Card component displaying a single predefined query option.
    Shows query name, description, parameters, and execute button.

data_table.py
    Enhanced data table widget for displaying query results.
    Supports sorting, filtering, pagination, and row selection.

stat_panel.py
    Statistical summary panel widget.
    Displays key metrics, trends, and visual indicators.

loading_spinner.py
    Loading indicator widget with customizable messages.
    Shows progress during database operations.

Guidelines:
----------
- Widgets should be highly reusable
- Accept data via props/parameters
- Emit events for parent screens to handle
- Follow Textual's reactive programming patterns
- Include proper CSS classes for styling

Owner: UI Developer (Krisha Sanjay Bhalala)
"""

from .query_card import QueryCard
from .data_table import DataTable
from .stat_panel import StatPanel
from .loading_spinner import LoadingSpinner

__all__ = [
    "QueryCard",
    "DataTable",
    "StatPanel",
    "LoadingSpinner",
]
