# ui/interfaces.py
from dataclasses import dataclass
from typing import Protocol, Any

# Replace what you had in shared/interfaces.py


@dataclass
class UIRequest:
    """Represents a UI request to the controller"""

    action: str
    payload: Any = None


@dataclass
class UIResponse:
    """Represents a response from the controller to the UI"""

    success: bool
    data: Any = None
    message: str = ""


class ControllerInterface(Protocol):
    """
    Interface for controllers used by the UI 
    Any class with handle_request method that takes UIRequest and returns UIResponse is a valid controller
    """

    def handle_request(self, request: UIRequest) -> UIResponse: ...
