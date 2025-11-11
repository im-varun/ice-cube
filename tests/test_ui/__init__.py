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
