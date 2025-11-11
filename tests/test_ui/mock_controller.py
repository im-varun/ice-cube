# tests/test_ui/mock_controller.py
class MockController:
    def handle_request(self, request: UIRequest) -> UIResponse:
        return UIResponse(
            success=True,
            data={"player": "Wayne Gretzky", "goals": 894},
            message="Success"
        )