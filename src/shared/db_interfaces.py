from typing import Protocol, List, Dict, Any
from dataclasses import dataclass
from enum import Enum

class QueryType(Enum):
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    CUSTOM = "CUSTOM"

@dataclass
class QueryRequest:
    """Standardized request from Controller to Database"""
    query_type: QueryType
    query_name: str | None = None  # For predefined queries
    params: Dict[str, Any] | None = None
    raw_query: str | None = None    # For custom queries

@dataclass
class QueryResponse:
    """Standardized response from Database to Controller"""
    success: bool
    data: List[Dict[str, Any]] | None
    rows_affected: int
    error_message: str | None = None
    error_code: str | None = None

class QueryEngineInterface(Protocol):
    """Interface for query engine"""
    def execute_query(self, request: QueryRequest) -> QueryResponse:
        ...
    
    def validate_query(self, query: str) -> tuple[bool, str]:
        ...