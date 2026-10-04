from pathlib import Path
import plotly.graph_objects as go
import polars as pl


class PlotlyEngine:

    def build_3d_globe(self, df: pl.DataFrame) -> str:
        # Filter valid latitude (-90 to 90) and longitude (-180 to 180) ranges
        pdf = df.filter(
            (pl.col("reclat") >= -90)
            & (pl.col("reclat") <= 90)
            & (pl.col("reclong") >= -180)
            & (pl.col("reclong") <= 180)
        ).to_pandas()

        fig = go.Figure(
            data=go.Scattergeo(
                lat=pdf["reclat"],
                lon=pdf["reclong"],
                mode="markers",
                text=pdf["name"],
                marker=dict(
                    size=4,
                    color=pdf["mass_kg"],
                    colorscale="Viridis",
                    showscale=True,
                    colorbar=dict(title="Mass (kg)"),
                ),
            )
        )

        fig.update_geos(
            projection_type="orthographic",
            showland=True,
            landcolor="rgb(240, 240, 240)",
            showocean=True,
            oceancolor="rgb(10, 10, 30)",
            showlakes=True,
            lakecolor="rgb(10, 10, 30)",
            showcountries=True,
        )

        fig.update_layout(
            title="3D Meteorite Landing Distribution",
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor="black",
            font=dict(color="white"),
        )

        output_path = Path("output_globe.html")
        fig.write_html(str(output_path))
        return str(output_path)
