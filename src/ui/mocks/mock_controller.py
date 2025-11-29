# src/ui/mocks/mock_controller.py
from ui.interfaces import ControllerInterface, UIRequest, UIResponse


class MockController(ControllerInterface):
    """Mock controller for development/testing without a database"""

    def handle_request(self, request: UIRequest) -> UIResponse:
        return UIResponse(
            success=True,
            data={"mock": "This is mock data"},
            message=f"Mock response for action '{request.action}'",
        )
