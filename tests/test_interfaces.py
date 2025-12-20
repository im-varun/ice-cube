"""
Tests for UI interfaces - UIRequest, UIResponse, and ControllerInterface.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ui.interfaces import ControllerInterface, UIRequest, UIResponse


class TestUIRequest:
    """Tests for UIRequest dataclass."""

    def test_create_basic_request(self):
        """Should create a request with action only."""
        request = UIRequest(action="head_to_head")
        assert request.action == "head_to_head"
        assert request.payload is None

    def test_create_request_with_payload(self):
        """Should create a request with action and payload."""
        request = UIRequest(
            action="head_to_head",
            payload={"Player_1": "Connor McDavid", "Player_2": "Sidney Crosby"},
        )
        assert request.action == "head_to_head"
        assert request.payload["Player_1"] == "Connor McDavid"

    def test_request_equality(self):
        """Two requests with same data should be equal."""
        r1 = UIRequest(action="test", payload={"x": 1})
        r2 = UIRequest(action="test", payload={"x": 1})
        assert r1 == r2


class TestUIResponse:
    """Tests for UIResponse dataclass."""

    def test_create_success_response(self):
        """Should create successful response."""
        response = UIResponse(success=True, data={"result": "ok"}, message="Done")
        assert response.success is True
        assert response.data == {"result": "ok"}
        assert response.message == "Done"

    def test_create_error_response(self):
        """Should create error response."""
        response = UIResponse(success=False, message="SQL injection detected")
        assert response.success is False
        assert response.data is None
        assert response.message == "SQL injection detected"

    def test_default_values(self):
        """Should have proper defaults."""
        response = UIResponse(success=True)
        assert response.data is None
        assert response.message == ""

    def test_response_equality(self):
        """Two responses with same data should be equal."""
        r1 = UIResponse(success=True, message="ok")
        r2 = UIResponse(success=True, message="ok")
        assert r1 == r2


class TestControllerInterface:
    """Tests for ControllerInterface protocol."""

    def test_mock_controller_implements_interface(self):
        """Mock controller should satisfy the interface."""

        class MockController:
            def handle_request(self, request: UIRequest) -> UIResponse:
                return UIResponse(success=True, message="mock response")

        controller = MockController()
        result = controller.handle_request(UIRequest(action="test"))
        assert isinstance(result, UIResponse)
        assert result.success is True

    def test_controller_interface_type_hints(self):
        """Interface should have correct type annotations."""
        import inspect

        sig = inspect.signature(ControllerInterface.handle_request)
        params = list(sig.parameters.keys())
        assert "request" in params
