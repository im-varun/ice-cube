"""
Loading Spinner Widget - Custom loading indicators
"""

import asyncio
from typing import Optional

from textual.app import ComposeResult
from textual.containers import Center, Container
from textual.reactive import reactive
from textual.widgets import LoadingIndicator, Static


class LoadingSpinner(Container):
    """
    Custom loading spinner with message

    Features:
    - Animated spinner
    - Loading message
    - Progress percentage
    - Customizable colors
    """

    is_loading = reactive(False)
    message = reactive("Loading...")
    progress = reactive(0)

    def __init__(self, message: str = "Loading...", show_progress: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.loading_message = message
        self.show_progress = show_progress
        self.add_class("loading-container")

    def compose(self) -> ComposeResult:
        """Compose the loading spinner"""
        with Center():
            yield LoadingIndicator()
            yield Static(self.loading_message, id="loading-message", classes="content-title")
            if self.show_progress:
                yield Static("0%", id="progress-text", classes="stat-value")

    def watch_message(self, new_message: str) -> None:
        """Update the loading message"""
        msg_widget = self.query_one("#loading-message", Static)
        msg_widget.update(new_message)

    def watch_progress(self, new_progress: int) -> None:
        """Update the progress percentage"""
        if self.show_progress:
            progress_widget = self.query_one("#progress-text", Static)
            progress_widget.update(f"{new_progress}%")

    def start_loading(self, message: Optional[str] = None) -> None:
        """Start the loading animation"""
        self.is_loading = True
        if message:
            self.message = message
        self.display = True

    def stop_loading(self) -> None:
        """Stop the loading animation"""
        self.is_loading = False
        self.display = False

    def update_progress(self, progress: int, message: Optional[str] = None) -> None:
        """Update progress and optionally message"""
        self.progress = progress
        if message:
            self.message = message


class HockeyLoadingSpinner(Container):
    """
    Hockey-themed loading animation
    """

    FRAMES = [
        "🏒    🥅",
        " 🏒   🥅",
        "  🏒  🥅",
        "   🏒 🥅",
        "    🏒🥅",
        "     🏒",
        "    🏒 ",
        "   🏒  ",
        "  🏒   ",
        " 🏒    ",
    ]

    def __init__(self, message: str = "Loading NHL data...", **kwargs):
        super().__init__(**kwargs)
        self.loading_message = message
        self.current_frame = 0
        self.is_active = False
        self.add_class("loading-container")

    def compose(self) -> ComposeResult:
        """Compose the hockey loading spinner"""
        with Center():
            yield Static(self.FRAMES[0], id="hockey-animation", classes="stat-value-large")
            yield Static(self.loading_message, id="hockey-message", classes="content-title")

    async def start_animation(self) -> None:
        """Start the hockey animation"""
        self.is_active = True
        self.display = True

        animation = self.query_one("#hockey-animation", Static)

        while self.is_active:
            self.current_frame = (self.current_frame + 1) % len(self.FRAMES)
            animation.update(self.FRAMES[self.current_frame])
            await asyncio.sleep(0.1)

    def stop_animation(self) -> None:
        """Stop the hockey animation"""
        self.is_active = False
        self.display = False


class DataLoadingIndicator(Container):
    """
    Loading indicator specifically for data operations
    """

    def __init__(self, operation: str = "Loading", total_items: Optional[int] = None, **kwargs):
        super().__init__(**kwargs)
        self.operation = operation
        self.total_items = total_items
        self.loaded_items = 0
        self.add_class("stats-panel")

    def compose(self) -> ComposeResult:
        """Compose the data loading indicator"""
        with Center():
            yield Static("⏳", classes="stat-value-large")
            yield Static(f"{self.operation}...", id="operation-text", classes="content-title")
            if self.total_items:
                yield Static(
                    f"0 / {self.total_items} items", id="progress-count", classes="stat-value"
                )

    def update_progress(self, loaded: int, message: Optional[str] = None) -> None:
        """Update loading progress"""
        self.loaded_items = loaded

        if message:
            op_text = self.query_one("#operation-text", Static)
            op_text.update(message)

        if self.total_items:
            progress = self.query_one("#progress-count", Static)
            percentage = (loaded / self.total_items) * 100
            progress.update(f"{loaded} / {self.total_items} items ({percentage:.1f}%)")


class QueryExecutionSpinner(Container):
    """
    Spinner specifically for SQL query execution
    """

    QUERY_STAGES = [
        "Parsing query...",
        "Validating syntax...",
        "Optimizing query plan...",
        "Executing query...",
        "Fetching results...",
        "Formatting data...",
    ]

    def __init__(self, query_preview: str = "", **kwargs):
        super().__init__(**kwargs)
        self.query_preview = query_preview
        self.current_stage = 0
        self.add_class("stats-panel")

    def compose(self) -> ComposeResult:
        """Compose the query execution spinner"""
        with Center():
            yield LoadingIndicator()
            yield Static("Executing Query", classes="content-title")

            if self.query_preview:
                preview = (
                    self.query_preview[:100] + "..."
                    if len(self.query_preview) > 100
                    else self.query_preview
                )
                yield Static(preview, classes="content-subtitle")

            yield Static(self.QUERY_STAGES[0], id="stage-text", classes="highlight-cyan")
            yield Static(
                "Estimated time: calculating...", id="time-estimate", classes="content-subtitle"
            )

    def advance_stage(self) -> None:
        """Advance to next execution stage"""
        if self.current_stage < len(self.QUERY_STAGES) - 1:
            self.current_stage += 1
            stage_text = self.query_one("#stage-text", Static)
            stage_text.update(self.QUERY_STAGES[self.current_stage])

    def update_time_estimate(self, seconds: float) -> None:
        """Update estimated time remaining"""
        time_widget = self.query_one("#time-estimate", Static)
        if seconds < 1:
            time_widget.update("Almost done...")
        else:
            time_widget.update(f"Estimated time: {seconds:.1f}s remaining")


class MinimalSpinner(Static):
    """
    Minimal inline spinner (just the text animation)
    """

    SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, message: str = "", **kwargs):
        super().__init__("", **kwargs)
        self.spinner_message = message
        self.current_frame = 0
        self.is_spinning = False

    async def start(self) -> None:
        """Start the spinner animation"""
        self.is_spinning = True

        while self.is_spinning:
            frame = self.SPINNER_FRAMES[self.current_frame]
            self.update(f"{frame} {self.spinner_message}")
            self.current_frame = (self.current_frame + 1) % len(self.SPINNER_FRAMES)
            await asyncio.sleep(0.1)

    def stop(self, final_message: str = "✓") -> None:
        """Stop the spinner"""
        self.is_spinning = False
        self.update(f"{final_message} {self.spinner_message}")


class ProgressSpinner(Container):
    """
    Spinner with detailed progress bar
    """

    def __init__(self, title: str = "Processing", total_steps: int = 100, **kwargs):
        super().__init__(**kwargs)
        self.spinner_title = title
        self.total_steps = total_steps
        self.current_step = 0
        self.add_class("stats-panel")

    def compose(self) -> ComposeResult:
        """Compose the progress spinner"""
        yield Static(self.spinner_title, classes="content-title")
        yield LoadingIndicator()
        yield Static("0%", id="percentage", classes="stat-value-large")
        yield Static("░" * 50, id="progress-bar", classes="highlight-cyan")
        yield Static(f"Step 0 of {self.total_steps}", id="step-counter", classes="content-subtitle")

    def update_progress(self, step: int, message: Optional[str] = None) -> None:
        """Update progress bar"""
        self.current_step = step
        percentage = (step / self.total_steps) * 100

        # Update percentage
        pct_widget = self.query_one("#percentage", Static)
        pct_widget.update(f"{percentage:.0f}%")

        # Update progress bar
        filled = int((step / self.total_steps) * 50)
        bar = "█" * filled + "░" * (50 - filled)
        bar_widget = self.query_one("#progress-bar", Static)
        bar_widget.update(bar)

        # Update step counter
        step_widget = self.query_one("#step-counter", Static)
        counter_text = f"Step {step} of {self.total_steps}"
        if message:
            counter_text += f" - {message}"
        step_widget.update(counter_text)
