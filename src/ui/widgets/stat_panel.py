"""
Statistics Panel Widget - Reusable component for displaying stats
"""

from typing import List, Optional, Tuple

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static


class StatPanel(Container):
    """
    A reusable panel for displaying statistics

    Features:
    - Title and description
    - Multiple stat rows
    - Icons and colors
    - Comparison indicators
    """

    def __init__(
        self,
        title: str,
        stats: Optional[List[Tuple[str, str]]] = None,
        description: Optional[str] = None,
        icon: Optional[str] = None,
        highlight: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.panel_title = title
        self.stats = stats or []
        self.panel_description = description
        self.icon = icon
        self.highlight = highlight

        # Apply styling class
        if highlight:
            self.add_class("stats-panel")
            self.add_class("highlight-panel")
        else:
            self.add_class("stats-panel")

    def compose(self) -> ComposeResult:
        """Compose the stat panel"""
        with Vertical():
            # Title with optional icon
            title_text = f"{self.icon} {self.panel_title}" if self.icon else self.panel_title
            yield Static(title_text, classes="stat-label")

            # Description if provided
            if self.panel_description:
                yield Static(self.panel_description, classes="content-subtitle")

            # Stat rows
            for label, value in self.stats:
                with Horizontal():
                    yield Static(f"{label}:", classes="stat-label")
                    yield Static(str(value), classes="stat-value")

    def update_stat(self, label: str, new_value: str) -> None:
        """Update a specific stat value"""
        for i, (stat_label, _) in enumerate(self.stats):
            if stat_label == label:
                self.stats[i] = (label, new_value)
                self.refresh()
                break

    def add_stat(self, label: str, value: str) -> None:
        """Add a new stat to the panel"""
        self.stats.append((label, value))
        self.refresh()

    def clear_stats(self) -> None:
        """Clear all stats"""
        self.stats = []
        self.refresh()


class ComparisonPanel(Container):
    """
    Panel for comparing two entities side-by-side
    """

    def __init__(
        self,
        entity1_name: str,
        entity2_name: str,
        stats: List[Tuple[str, str, str]],  # (label, value1, value2)
        winner: Optional[int] = None,  # 1 or 2
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.entity1_name = entity1_name
        self.entity2_name = entity2_name
        self.stats = stats
        self.winner = winner

        self.add_class("stats-panel")

    def compose(self) -> ComposeResult:
        """Compose the comparison panel"""
        with Vertical():
            # Header with names
            with Horizontal():
                entity1_class = "highlight-cyan" if self.winner == 1 else ""
                entity2_class = "highlight-orange" if self.winner == 2 else ""

                yield Static(self.entity1_name, classes=entity1_class)
                yield Static(" VS ", classes="vs-divider")
                yield Static(self.entity2_name, classes=entity2_class)

            # Comparison stats
            for label, val1, val2 in self.stats:
                with Horizontal():
                    yield Static(str(val1), classes="stat-value")
                    yield Static(label, classes="stat-label")
                    yield Static(str(val2), classes="stat-value")


class MetricCard(Container):
    """
    Compact card for displaying a single metric
    """

    def __init__(
        self,
        label: str,
        value: str,
        subtitle: Optional[str] = None,
        color: str = "orange",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.metric_label = label
        self.metric_value = value
        self.subtitle = subtitle
        self.color = color

        self.add_class("stats-panel")

    def compose(self) -> ComposeResult:
        """Compose the metric card"""
        with Vertical():
            yield Static(self.metric_label, classes="stat-label")

            value_class = f"stat-value-large highlight-{self.color}"
            yield Static(self.metric_value, classes=value_class)

            if self.subtitle:
                yield Static(self.subtitle, classes="content-subtitle")

    def update_value(self, new_value: str) -> None:
        """Update the metric value"""
        self.metric_value = new_value
        self.refresh()


class ProgressBar(Container):
    """
    Simple progress bar widget
    """

    def __init__(
        self,
        label: str,
        value: float,
        max_value: float = 100.0,
        color: str = "cyan",
        show_percentage: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.bar_label = label
        self.value = value
        self.max_value = max_value
        self.color = color
        self.show_percentage = show_percentage

        self.add_class("stats-panel")

    def compose(self) -> ComposeResult:
        """Compose the progress bar"""
        with Vertical():
            # Label
            yield Static(self.bar_label, classes="stat-label")

            # Progress bar
            percentage = (self.value / self.max_value) * 100
            filled = int(percentage / 2)  # 50 chars for 100%
            empty = 50 - filled

            bar = "█" * filled + "░" * empty
            bar_class = f"highlight-{self.color}"
            yield Static(bar, classes=bar_class)

            # Percentage text
            if self.show_percentage:
                pct_text = f"{percentage:.1f}% ({self.value}/{self.max_value})"
                yield Static(pct_text, classes="content-subtitle")

    def update_progress(self, new_value: float) -> None:
        """Update the progress value"""
        self.value = new_value
        self.refresh()


class RankingPanel(Container):
    """
    Panel for displaying rankings with medals/badges
    """

    def __init__(
        self,
        title: str,
        rankings: List[Tuple[int, str, str]],  # (rank, name, value)
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.ranking_title = title
        self.rankings = rankings

        self.add_class("stats-panel")

    def compose(self) -> ComposeResult:
        """Compose the ranking panel"""
        with Vertical():
            yield Static(self.ranking_title, classes="content-title")

            for rank, name, value in self.rankings:
                # Add medals for top 3
                if rank == 1:
                    icon = "🥇"
                    style = "highlight-orange"
                elif rank == 2:
                    icon = "🥈"
                    style = "highlight-cyan"
                elif rank == 3:
                    icon = "🥉"
                    style = "highlight-yellow"
                else:
                    icon = f"{rank}."
                    style = ""

                with Horizontal():
                    yield Static(f"{icon} {name}", classes=style)
                    yield Static(value, classes="stat-value")


class TrendIndicator(Container):
    """
    Widget showing trend with arrow indicators
    """

    def __init__(self, label: str, current_value: float, previous_value: float, **kwargs):
        super().__init__(**kwargs)
        self.trend_label = label
        self.current_value = current_value
        self.previous_value = previous_value

        self.add_class("stats-panel")

    def compose(self) -> ComposeResult:
        """Compose the trend indicator"""
        with Vertical():
            yield Static(self.trend_label, classes="stat-label")

            # Calculate trend
            diff = self.current_value - self.previous_value
            pct_change = (diff / self.previous_value) * 100 if self.previous_value != 0 else 0

            # Determine arrow and color
            if diff > 0:
                arrow = "↑"
                color = "highlight-green"
                sign = "+"
            elif diff < 0:
                arrow = "↓"
                color = "highlight-orange"
                sign = ""
            else:
                arrow = "→"
                color = "highlight-cyan"
                sign = ""

            trend_text = f"{arrow} {sign}{diff:.2f} ({sign}{pct_change:.1f}%)"
            yield Static(trend_text, classes=color)
            yield Static(f"Current: {self.current_value:.2f}", classes="content-subtitle")
