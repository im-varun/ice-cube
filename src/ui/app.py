# src/ui/app.py
from textual.app import App
from shared.interfaces import UIRequest, UIResponse, ControllerInterface

class IceCubeApp(App):
    def __init__(self, controller: ControllerInterface):
        self.controller = controller
        super().__init__()
    
    def on_button_click(self, event):
        request = UIRequest(
            action="get_player_stats",
            params={"player_id": 123}
        )
        response = self.controller.handle_request(request)
        self.display_results(response)