"""
QueryCard – Clean, icon-free, fixed-size, glow-only selection
"""

from textual.app import ComposeResult
from textual.containers import Container
from textual.message import Message
from textual.widgets import Static


class QueryCard(Container):
    """Clickable query card – no icons, glow-only hover/selection"""

    class Selected(Message):
        def __init__(self, query_id: str):
            super().__init__()
            self.query_id = query_id

    def __init__(self, title: str, query_id: str):
        super().__init__()
        self.title = title
        self.query_id = query_id
        self.add_class("query-card")

    def compose(self) -> ComposeResult:
        yield Static(self.title, classes="query-card-title")

    def on_click(self) -> None:
        self.post_message(self.Selected(self.query_id))

    def on_enter(self) -> None:
        self.styles.border = ("solid", "#00ffff")

    def on_leave(self) -> None:
        self.styles.border = ("solid", "#1e3a5f")
