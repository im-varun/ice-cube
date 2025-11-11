"""
Screens Module - Individual Screen Implementations
==================================================

Each file represents a complete screen in the application.

Files:
------
home_screen.py
    Main dashboard/home screen.
    Displays overview stats, recent activity, and navigation options.

login_screen.py
    User authentication screen.
    Handles login form, validation, and session initialization.

query_screen.py
    Query builder and predefined queries screen.
    Allows users to select and customize analytics queries.

results_screen.py
    Query results display screen.
    Shows data tables, charts, and export options.

analytics_screen.py
    Advanced analytics and visualization screen.
    Displays complex analytics like revenge game effect, birthday curse, etc.

Guidelines:
----------
- Each screen inherits from textual.screen.Screen
- Screens should be self-contained and reusable
- Use widgets from ../widgets/ for common components
- Communicate with controllers via UIRequest/UIResponse
- Handle loading states and errors gracefully

Owner: UI Developer (Krisha Sanjay Bhalala)
"""

from .home_screen import HomeScreen
from .login_screen import LoginScreen
from .query_screen import QueryScreen
from .results_screen import ResultsScreen
from .analytics_screen import AnalyticsScreen

__all__ = [
    "HomeScreen",
    "LoginScreen",
    "QueryScreen",
    "ResultsScreen",
    "AnalyticsScreen",
]
