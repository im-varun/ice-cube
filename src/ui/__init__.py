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
