#!/bin/bash
# Only Run this if you want to delete entire project and start from empty project
echo "Creating an Empty IceCube project structure..."

# Create main directories
mkdir -p src/{ui/{screens,widgets,styles},controllers,database/{queries,models},shared}
mkdir -p scripts
mkdir -p data/{raw,cleaned}
mkdir -p reports
mkdir -p tests/{test_ui,test_controllers,test_database,test_shared}

# Create Python __init__.py files
touch src/__init__.py
touch src/ui/__init__.py
touch src/ui/screens/__init__.py
touch src/ui/widgets/__init__.py
touch src/ui/styles/__init__.py
touch src/controllers/__init__.py
touch src/database/__init__.py
touch src/database/queries/__init__.py
touch src/database/models/__init__.py
touch src/shared/__init__.py
touch tests/__init__.py
touch tests/test_ui/__init__.py
touch tests/test_controllers/__init__.py
touch tests/test_database/__init__.py
touch tests/test_shared/__init__.py

# Create UI files
touch src/ui/screens/{home_screen,login_screen,query_screen,results_screen,analytics_screen}.py
touch src/ui/widgets/{query_card,data_table,stat_panel,loading_spinner}.py
touch src/ui/styles/{theme,components}.tcss
touch src/ui/app.py

# Create controller files
touch src/controllers/{base_controller,auth_controller,query_controller,analytics_controller,data_formatter}.py

# Create database files
touch src/database/{connection,query_engine,query_validator,query_builder}.py
touch src/database/queries/{player_queries,team_queries,game_queries,analytics_queries}.py
touch src/database/models/{player,team,game}.py

# Create shared files
touch src/shared/{config,constants,exceptions,logger,types,interfaces,db_interfaces}.py

# Create main entry point
touch src/main.py

# Create script files
touch scripts/{populate_database,empty_database,data_cleaning,view_metadata}.py

# Create data files
touch data/{metadata.txt,schema.sql}
touch data/raw/.gitkeep
touch data/cleaned/.gitkeep
touch reports/.gitkeep

# Create README and CONTRIBUTING
touch CONTRIBUTING.md

# Create config files
touch .gitignore .pre-commit-config.yaml .flake8 pyproject.toml requirements.txt


echo "Populating __init__.py files with documentation..."

# src/__init__.py
cat > src/__init__.py << 'EOF'
"""
IceCube - NHL Database Management System
=========================================

Main application package containing all core modules.

Structure:
- ui/          : User interface components (Textual-based CLI)
- controllers/ : Business logic and request orchestration
- database/    : Database connection, query engine, and data models
- shared/      : Shared utilities, interfaces, and constants
"""

__version__ = "1.0.0"
__author__ = "IceCube Team"
EOF

# src/ui/__init__.py
cat > src/ui/__init__.py << 'EOF'
"""
UI Module - User Interface Layer
=================================

Handles all user interface components using the Textual library.

Files:
------
app.py
    Main Textual application class and entry point for UI.
    Coordinates screen navigation and manages app lifecycle.

Subdirectories:
--------------
screens/
    Individual screen implementations (home, login, query, results, analytics).
    Each screen is a self-contained Textual Screen component.

widgets/
    Reusable UI components used across multiple screens.
    Includes data tables, cards, panels, and loading indicators.

styles/
    TCSS (Textual CSS) stylesheets for theming and component styling.
    Separated into theme.tcss (global) and components.tcss (specific).

Responsibilities:
----------------
- Render UI components
- Handle user input events
- Display data received from controllers
- Navigate between screens
- Manage UI state

Dependencies:
------------
- textual library for terminal UI
- rich library for styled output
- Controllers via src/shared/interfaces.py

Owner: UI Developer (Krisha Sanjay Bhalala)
"""

from .app import IceCubeApp

__all__ = ["IceCubeApp"]
EOF

# src/ui/screens/__init__.py
cat > src/ui/screens/__init__.py << 'EOF'
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
EOF

# src/ui/widgets/__init__.py
cat > src/ui/widgets/__init__.py << 'EOF'
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
EOF

# src/ui/styles/__init__.py
cat > src/ui/styles/__init__.py << 'EOF'
"""
Styles Module - TCSS Stylesheets
=================================

Contains Textual CSS files for styling the application.

Files:
------
theme.tcss
    Global theme definitions including:
    - Color palette (primary, secondary, accent colors)
    - Typography (fonts, sizes, weights)
    - Spacing and layout constants
    - Dark/light mode variations

components.tcss
    Component-specific styles:
    - Widget styling (buttons, inputs, tables)
    - Screen layouts
    - Animation definitions
    - Responsive design rules

Guidelines:
----------
- Follow Textual CSS syntax
- Use CSS variables for consistency
- Keep styles modular and maintainable
- Document complex selectors
- Test in different terminal sizes

Owner: UI Developer (Krisha Sanjay Bhalala)
"""
EOF

# src/controllers/__init__.py
cat > src/controllers/__init__.py << 'EOF'
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

from .base_controller import BaseController
from .auth_controller import AuthController
from .query_controller import QueryController
from .analytics_controller import AnalyticsController
from .data_formatter import DataFormatter

__all__ = [
    "BaseController",
    "AuthController",
    "QueryController",
    "AnalyticsController",
    "DataFormatter",
]
EOF

# src/database/__init__.py
cat > src/database/__init__.py << 'EOF'
"""
Database Module - Data Access Layer
===================================

Manages all database interactions, query execution, and data models.

Files:
------
connection.py
    Database connection management.
    Functions: get_connection(), close_connection(), connection_pool()

query_engine.py
    Core query execution engine implementing QueryEngineInterface.
    Methods: execute_query(), validate_query(), execute_transaction()

query_validator.py
    SQL injection prevention and query safety validation.
    Functions: is_safe(), sanitize_input(), validate_parameters()

query_builder.py
    Safe SQL query construction utilities.
    Provides parameterized query building to prevent injection.

Subdirectories:
--------------
queries/
    Predefined query implementations organized by domain.
    Contains ready-to-use queries for common operations.

models/
    Data models and schemas representing database entities.
    Includes Player, Team, Game models with validation.

Responsibilities:
----------------
- Receive QueryRequest from controllers
- Validate query safety (SQL injection prevention)
- Execute queries against database
- Handle database errors and transactions
- Transform raw results into structured format
- Return QueryResponse to controllers

Security:
--------
- ALWAYS validate queries before execution
- Use parameterized queries
- Never concatenate user input into SQL
- Log all query executions
- Handle sensitive data appropriately

Owner: Database Developer (Varun Mulchandani)
"""

from .connection import get_connection, close_connection
from .query_engine import QueryEngine
from .query_validator import QueryValidator
from .query_builder import QueryBuilder

__all__ = [
    "get_connection",
    "close_connection",
    "QueryEngine",
    "QueryValidator",
    "QueryBuilder",
]
EOF

# src/database/queries/__init__.py
cat > src/database/queries/__init__.py << 'EOF'
"""
Queries Module - Predefined Query Implementations
=================================================

Contains organized, reusable query functions for common operations.

Files:
------
player_queries.py
    Player-related queries:
    - get_player_by_id()
    - get_player_stats()
    - get_top_scorers()
    - get_players_with_most_assists()
    - get_players_longest_shifts()
    - get_pure_goal_scorers() (score but never assist)

team_queries.py
    Team-related queries:
    - get_team_by_id()
    - get_team_roster()
    - get_highest_scoring_teams()
    - get_team_season_stats()
    - get_home_vs_away_performance()

game_queries.py
    Game-related queries:
    - get_game_by_id()
    - get_longest_games()
    - get_games_by_team()
    - get_game_scoring_trends()
    - get_most_common_play_types()

analytics_queries.py
    Advanced analytics queries:
    - head_to_head_duel_tracker()
    - revenge_game_effect()
    - home_rink_advantage()
    - birthday_curse_analysis()
    - scoring_trends_by_period()

Guidelines:
----------
- Each function returns QueryResponse
- Use query_builder for safe SQL construction
- Include comprehensive docstrings
- Handle edge cases (no results, invalid params)
- Log query execution for debugging
- Use type hints for all parameters

Owner: Database Developer (Varun Mulchandani)
"""

from .player_queries import (
    get_player_by_id,
    get_player_stats,
    get_top_scorers,
)
from .team_queries import (
    get_team_by_id,
    get_highest_scoring_teams,
)
from .game_queries import (
    get_game_by_id,
    get_longest_games,
)
from .analytics_queries import (
    head_to_head_duel,
    revenge_game_effect,
)

__all__ = [
    # Player queries
    "get_player_by_id",
    "get_player_stats",
    "get_top_scorers",
    # Team queries
    "get_team_by_id",
    "get_highest_scoring_teams",
    # Game queries
    "get_game_by_id",
    "get_longest_games",
    # Analytics queries
    "head_to_head_duel",
    "revenge_game_effect",
]
EOF

# src/database/models/__init__.py
cat > src/database/models/__init__.py << 'EOF'
"""
Models Module - Data Models and Schemas
=======================================

Defines data structures representing database entities.

Files:
------
player.py
    Player model with attributes:
    - player_id, name, position, team_id
    - jersey_number, birthdate, height, weight
    Methods: from_dict(), to_dict(), validate()

team.py
    Team model with attributes:
    - team_id, name, city, arena_name
    - division, conference, founded_year
    Methods: from_dict(), to_dict(), validate()

game.py
    Game model with attributes:
    - game_id, date, home_team_id, away_team_id
    - home_score, away_score, overtime, shootout
    - duration, attendance
    Methods: from_dict(), to_dict(), validate()

Guidelines:
----------
- Use dataclasses or pydantic for models
- Include validation methods
- Provide serialization (to/from dict)
- Document all fields with type hints
- Handle None/null values appropriately
- Include helper methods for common operations

Owner: Database Developer (Varun Mulchandani)
"""

from .player import Player
from .team import Team
from .game import Game

__all__ = [
    "Player",
    "Team",
    "Game",
]
EOF

# src/shared/__init__.py
cat > src/shared/__init__.py << 'EOF'
"""
Shared Module - Common Utilities and Interfaces
===============================================

Contains code shared across all layers (UI, Controllers, Database).

Files:
------
interfaces.py
    UI ↔ Controller interface definitions:
    - UIRequest, UIResponse dataclasses
    - ControllerInterface protocol
    - ActionType enum

db_interfaces.py
    Controller ↔ Database interface definitions:
    - QueryRequest, QueryResponse dataclasses
    - QueryEngineInterface protocol
    - QueryType enum

config.py
    Application configuration management:
    - Database connection settings
    - Application constants (timeouts, limits)
    - Environment-specific settings
    - Configuration loading/validation

constants.py
    Global constants used throughout the application:
    - Error codes
    - Status codes
    - Default values
    - Magic numbers with meaningful names

exceptions.py
    Custom exception classes:
    - DatabaseError, QueryValidationError
    - AuthenticationError, AuthorizationError
    - DataFormatError, ConfigurationError

logger.py
    Centralized logging configuration:
    - Logger setup and formatting
    - Log levels by environment
    - File and console handlers

types.py
    Common type definitions and type aliases:
    - Custom types for better code clarity
    - Type unions and optional types
    - Protocol definitions

CRITICAL RULES:
--------------
1. This directory is SHARED - all 3 members depend on it
2. Create an issue BEFORE modifying any file here
3. Get team approval before making changes
4. Notify ALL team members after changes
5. Never break existing interfaces
6. Add, don't modify (when possible)

Owner: Shared by ALL members (requires coordination)
"""

from .interfaces import UIRequest, UIResponse, ActionType, ControllerInterface
from .db_interfaces import QueryRequest, QueryResponse, QueryType, QueryEngineInterface
from .exceptions import (
    IceCubeError,
    DatabaseError,
    QueryValidationError,
    AuthenticationError,
)
from .logger import get_logger

__all__ = [
    # Interfaces
    "UIRequest",
    "UIResponse",
    "ActionType",
    "ControllerInterface",
    "QueryRequest",
    "QueryResponse",
    "QueryType",
    "QueryEngineInterface",
    # Exceptions
    "IceCubeError",
    "DatabaseError",
    "QueryValidationError",
    "AuthenticationError",
    # Utilities
    "get_logger",
]
EOF

# tests/__init__.py
cat > tests/__init__.py << 'EOF'
"""
Tests Module - Unit and Integration Tests
=========================================

Test suite organized to mirror the src/ structure.

Structure:
---------
test_ui/
    Tests for UI components, screens, and widgets.
    Uses mock controllers to test UI in isolation.

test_controllers/
    Tests for controller logic and data orchestration.
    Uses mock database responses to test independently.

test_database/
    Tests for query engine, validators, and predefined queries.
    Uses test database with known data.

test_shared/
    Tests for shared utilities, interfaces, and helpers.

Guidelines:
----------
- One test file per source file
- Use descriptive test names: test_<function>_<scenario>_<expected>
- Include docstrings explaining what is being tested
- Use fixtures for common setup
- Mock external dependencies
- Aim for >80% code coverage
- Run tests before committing

Running Tests:
-------------
pytest tests/                    # Run all tests
pytest tests/test_ui/           # Run UI tests only
pytest tests/ -v                # Verbose output
pytest tests/ --cov=src         # With coverage report

Owner: All members test their own code
"""
EOF

# tests/test_ui/__init__.py
cat > tests/test_ui/__init__.py << 'EOF'
"""
UI Tests - User Interface Layer Tests
=====================================

Tests for all UI components including screens and widgets.

Test Files (to be created):
--------------------------
test_app.py
    Tests for main application class and lifecycle.

test_home_screen.py
    Tests for home screen rendering and navigation.

test_login_screen.py
    Tests for login form validation and authentication flow.

test_query_screen.py
    Tests for query selection and parameter input.

test_results_screen.py
    Tests for results display and data table rendering.

test_analytics_screen.py
    Tests for analytics visualizations and interactions.

test_query_card.py
    Tests for query card widget rendering and events.

test_data_table.py
    Tests for data table sorting, filtering, pagination.

test_stat_panel.py
    Tests for stat panel data display and updates.

test_loading_spinner.py
    Tests for loading indicator states and transitions.

Mocking Strategy:
----------------
Use MockController to simulate controller responses:

```python
from tests.mocks import MockController

def test_query_screen_loads_queries():
    controller = MockController()
    screen = QueryScreen(controller)
    screen.on_mount()
    assert len(screen.query_cards) > 0
```

Owner: UI Developer (Krisha Bhalala)
"""
EOF

# tests/test_controllers/__init__.py
cat > tests/test_controllers/__init__.py << 'EOF'
"""
Controller Tests - Business Logic Layer Tests
=============================================

Tests for controller logic and request orchestration.

Test Files (to be created):
--------------------------
test_base_controller.py
    Tests for base controller error handling and logging.

test_auth_controller.py
    Tests for login, logout, session validation logic.

test_query_controller.py
    Tests for query orchestration and data transformation.

test_analytics_controller.py
    Tests for analytics query coordination and calculations.

test_data_formatter.py
    Tests for data formatting and transformation functions.

Mocking Strategy:
----------------
Use MockQueryEngine to simulate database responses:

```python
from tests.mocks import MockQueryEngine

def test_query_controller_handles_player_stats():
    engine = MockQueryEngine()
    controller = QueryController(engine)
    request = UIRequest(action="get_player_stats", params={"id": 1})
    response = controller.handle_request(request)
    assert response.success is True
```

Owner: Controller Developer (Krish Sanjay Bhalala)
"""
EOF

# tests/test_database/__init__.py
cat > tests/test_database/__init__.py << 'EOF'
"""
Database Tests - Data Access Layer Tests
========================================

Tests for query engine, validators, and database operations.

Test Files (to be created):
--------------------------
test_connection.py
    Tests for database connection management.

test_query_engine.py
    Tests for query execution and error handling.

test_query_validator.py
    Tests for SQL injection prevention and validation.

test_query_builder.py
    Tests for safe query construction.

test_player_queries.py
    Tests for all player-related predefined queries.

test_team_queries.py
    Tests for all team-related predefined queries.

test_game_queries.py
    Tests for all game-related predefined queries.

test_analytics_queries.py
    Tests for all analytics queries.

test_player_model.py
    Tests for Player model validation and serialization.

test_team_model.py
    Tests for Team model validation and serialization.

test_game_model.py
    Tests for Game model validation and serialization.

Testing Strategy:
----------------
Use test database with known data:

```python
import pytest
from database.query_engine import QueryEngine

@pytest.fixture
def test_db():
    # Setup test database
    engine = QueryEngine(test_mode=True)
    yield engine
    # Cleanup

def test_get_player_by_id(test_db):
    result = test_db.execute_query(
        QueryRequest(query_name="get_player_by_id", params={"id": 1})
    )
    assert result.success is True
```

Owner: Database Developer (Varun Mulchandani)
"""
EOF

# tests/test_shared/__init__.py
cat > tests/test_shared/__init__.py << 'EOF'
"""
Shared Tests - Common Utilities Tests
=====================================

Tests for shared modules used across all layers.

Test Files (to be created):
--------------------------
test_interfaces.py
    Tests for interface dataclass validation and serialization.

test_db_interfaces.py
    Tests for database interface dataclass validation.

test_config.py
    Tests for configuration loading and validation.

test_constants.py
    Tests verifying constants have expected values.

test_exceptions.py
    Tests for custom exception behavior.

test_logger.py
    Tests for logger configuration and output.

test_types.py
    Tests for custom type definitions and validation.

Owner: Shared by all members
"""
EOF

echo "All __init__.py files populated with documentation!"


echo "Project structure created successfully!"
echo ""
echo "Next steps:"
echo "  1. Add your dependencies to lib/ directory if needed"
echo "  2. Set PYTHONPATH: export PYTHONPATH=\"\${PYTHONPATH}:\$(pwd)/lib\""
echo "  3. Read the __init__.py file in your module before starting work!"
echo "  4. Start coding!"