import webbrowser
from pathlib import Path
from data_pipeline import MeteoriteDataEngine
from plotly_engine import PlotlyEngine
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, DataTable, Footer, Header, Static


class SummaryCard(Static):
    """Card displaying a single summary metric."""

    pass


class NASADataDashboard(App):

    CSS = """
    Screen {
        background: $surface-darken-1;
    }
    #summary-container {
        height: 7;
        margin: 1 1;
    }
    SummaryCard {
        background: $panel;
        color: $text;
        border: solid $accent;
        padding: 1;
        margin: 0 1;
        width: 1fr;
        content-align: center middle;
    }
    #controls {
        height: 3;
        margin: 1;
    }
    Button {
        margin-right: 2;
    }
    DataTable {
        height: 1fr;
        margin: 1;
        border: round $primary;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit Dashboard"),
        ("g", "open_globe", "Open 3D Globe Plot"),
    ]

    def __init__(self, data_path: str):
        super().__init__()
        self.engine = MeteoriteDataEngine(data_path)
        self.plotly_engine = PlotlyEngine()

    def on_mount(self) -> None:

        self.df = self.engine.load_data()
        self.metrics = self.engine.get_summary_metrics()

        # Update summary labels
        self.query_one("#m-total", SummaryCard).update(
            f"[b]Total Impacts[/b]\n{self.metrics['total_landings']:,}"
        )
        self.query_one("#m-mass", SummaryCard).update(
            f"[b]Total Mass[/b]\n{self.metrics['total_mass_tons']:,} Tons"
        )
        self.query_one("#m-largest", SummaryCard).update(
            f"[b]Largest Landing[/b]\n{self.metrics['largest_name']} ({self.metrics['largest_mass_kg']:,} kg)"
        )

        # Populate DataTable
        table = self.query_one(DataTable)
        table.add_columns("Name", "Class", "Mass (kg)", "Year", "Lat", "Long")

        top_landings = self.engine.get_top_landings(100).to_dicts()
        for row in top_landings:
            # Null-safe value formatting
            mass_str = f"{row['mass_kg']:.1f}" if row.get("mass_kg") is not None else "0.0"
            lat_str = f"{row['reclat']:.2f}" if row.get("reclat") is not None else "N/A"
            long_str = f"{row['reclong']:.2f}" if row.get("reclong") is not None else "N/A"
            year_str = str(row["year"]) if row.get("year") else "Unknown"

            table.add_row(
                row.get("name", "Unknown"),
                row.get("recclass", "Unknown"),
                mass_str,
                year_str,
                lat_str,
                long_str,
            )

    def compose(self) -> ComposeResult:

        yield Header(show_clock=True)
        yield Horizontal(
            SummaryCard("Loading...", id="m-total"),
            SummaryCard("Loading...", id="m-mass"),
            SummaryCard("Loading...", id="m-largest"),
            id="summary-container",
        )
        yield Horizontal(
            Button("🌍 Render Plotly 3D Globe", id="btn-globe", variant="primary"),
            Button("🎬 Render Manim Explainer", id="btn-manim", variant="success"),
            id="controls",
        )
        yield DataTable(id="data-table")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == "btn-globe":
            path = self.plotly_engine.build_3d_globe(self.df)
            webbrowser.open(f"file://{Path(path).absolute()}")
        elif event.button.id == "btn-manim":
            self.notify("Run 'python3 -m manim -pql src/manim_renderer.py' in terminal!")

    def action_open_globe(self) -> None:

        path = self.plotly_engine.build_3d_globe(self.df)
        webbrowser.open(f"file://{Path(path).absolute()}")


if __name__ == "__main__":
    import sys

    data_file = sys.argv[1] if len(sys.argv) > 1 else "data/meteorite_landings.csv"
    app = NASADataDashboard(data_file)
    app.run()
