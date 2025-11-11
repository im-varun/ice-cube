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

from .db_interfaces import QueryEngineInterface, QueryRequest, QueryResponse, QueryType
from .exceptions import (
    AuthenticationError,
    DatabaseError,
    IceCubeError,
    QueryValidationError,
)
from .interfaces import ActionType, ControllerInterface, UIRequest, UIResponse
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
