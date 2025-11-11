"""
Controllers Module - Business Logic Layer
=========================================

Orchestrates application logic between UI and database layers.

Files:
------
base_controller.py
    Abstract base controller class defining common interface.
    Includes error handling, logging, and validation patterns.

auth_controller.py
    Handles user authentication and session management.
    Methods: login(), logout(), verify_session(), get_user_info()

query_controller.py
    Manages query execution workflow.
    Orchestrates query requests, validates inputs, formats responses.

analytics_controller.py
    Handles complex analytics queries.
    Implements: revenge_game_effect(), birthday_curse(), home_advantage(), etc.

data_formatter.py
    Transforms database responses into UI-friendly formats.
    Includes: format_table_data(), format_stats(), format_chart_data()

Responsibilities:
----------------
- Receive UIRequest from UI layer
- Validate and sanitize user input
- Orchestrate one or multiple database queries
- Transform raw data into presentation format
- Handle errors and edge cases
- Return UIResponse to UI layer

Communication:
-------------
- Receives: UIRequest from src/ui/
- Sends: QueryRequest to src/database/
- Returns: UIResponse to src/ui/

Owner: Controller Developer (Krish Sanjay Bhalala)
"""

from .analytics_controller import AnalyticsController
from .auth_controller import AuthController
from .base_controller import BaseController
from .data_formatter import DataFormatter
from .query_controller import QueryController

__all__ = [
    "BaseController",
    "AuthController",
    "QueryController",
    "AnalyticsController",
    "DataFormatter",
]
