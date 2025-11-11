import os  # noqa: E402
import sys  # noqa: E402

# Add the local lib/ directory to Python's path to use textual lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

# All the imports will be searched in lib/ in by default
from textual.app import App, ComposeResult  # type: ignore # noqa: E402
from textual.widgets import Header, Label  # type: ignore  # noqa: E402


class HelloWorldApp(App):  # type: ignore
    """A simple Hello World app using Textual."""

    CSS = """
    Label {
        text-align: center;
        margin-top: 10;
    }
    """

    def compose(self) -> ComposeResult:  # type: ignore
        """Compose the app's widgets."""
        yield Header(show_clock=True)
        yield Label("this is without installs.", id="message")


if __name__ == "__main__":
    app = HelloWorldApp()
    app.run()  # type: ignore
