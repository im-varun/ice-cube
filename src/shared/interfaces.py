"""
Central interface definitions for IceCube.
ALL members should reference these interfaces.
"""

from typing import Protocol, Any, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class ActionType(Enum):
    """Available UI actions"""
    LOGIN = "login"
    LOGOUT = "logout"
    GET_PLAYER_STATS = "get_player_stats"
    RUN_ANALYTICS = "run_analytics"
    CUSTOM_QUERY = "custom_query"


@dataclass
class UIRequest:
    """Request from UI to Controller"""
    action: ActionType
    params: Dict[str, Any]
    user_id: Optional[int] = None
    
    def validate(self) -> bool:
        """Validate request has required fields"""
        return self.action is not None


@dataclass
class UIResponse:
    """Response from Controller to UI"""
    success: bool
    data: Any
    message: str
    error_code: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ControllerInterface(Protocol):
    """Contract for all controllers"""
    
    def handle_request(self, request: UIRequest) -> UIResponse:
        """Handle a UI request and return formatted response"""
        ...