"""
Query Card Widget - Clickable card for pre-defined queries
"""

from textual.app import ComposeResult
from textual.containers import Container
from textual.message import Message
from textual.widgets import Static


class QueryCard(Container):
    """A clickable card widget for query selection"""

    class Selected(Message):
        """Message emitted when query card is selected"""

        def __init__(self, query_id: str):
            super().__init__()
            self.query_id = query_id

    def __init__(self, title: str, query_id: str, icon: str = "•", selected: bool = False):
        super().__init__()
        self.title = title
        self.query_id = query_id
        self.icon = icon
        self.is_selected = selected

        # Apply appropriate class based on selection
        if selected:
            self.add_class("query-card-selected")
        else:
            self.add_class("query-card")

    def compose(self) -> ComposeResult:
        """Compose the query card"""
        yield Static(f"{self.icon} {self.title}", classes="query-card-title")

    def on_click(self) -> None:
        """Handle click event"""
        self.post_message(self.Selected(self.query_id))

    def on_enter(self) -> None:
        """Handle hover enter"""
        if not self.is_selected:
            self.add_class("query-card")
            self.styles.border = ("solid", "#00d4ff")

    def on_leave(self) -> None:
        """Handle hover leave"""
        if not self.is_selected:
            self.styles.border = ("solid", "#1e3a5f")
