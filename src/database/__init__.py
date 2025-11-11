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
