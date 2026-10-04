from pathlib import Path
import polars as pl


class MeteoriteDataEngine:

    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self._df = None

    def load_data(self) -> pl.DataFrame:

        lazy_df = pl.scan_csv(
            self.data_path,
            has_header=True,
            schema_overrides={"mass (g)": pl.Float64, "year": pl.Int64},
        )

        self._df = (
            lazy_df.filter(
                pl.col("reclat").is_not_null() & pl.col("reclong").is_not_null()
            )
            .with_columns(
                [
                    pl.col("mass (g)").fill_null(0.0).alias("mass_g"),
                    (pl.col("mass (g)").fill_null(0.0) / 1000.0).alias("mass_kg"),
                    pl.col("year").fill_null(0),
                ]
            )
            .collect()
        )
        return self._df

    def get_summary_metrics(self) -> dict:

        total_count = len(self._df)
        total_mass_tons = self._df["mass_kg"].sum() / 1000.0
        avg_mass_kg = self._df["mass_kg"].mean()
        max_mass_kg = self._df["mass_kg"].max()
        largest_meteorite = self._df.filter(
            pl.col("mass_kg") == max_mass_kg
        ).to_dicts()[0]

        return {
            "total_landings": total_count,
            "total_mass_tons": round(total_mass_tons, 2),
            "avg_mass_kg": round(avg_mass_kg, 2),
            "largest_name": largest_meteorite["name"],
            "largest_mass_kg": round(max_mass_kg, 2),
            "largest_year": int(largest_meteorite["year"]),
        }

    def get_top_landings(self, limit: int = 50) -> pl.DataFrame:

        return self._df.sort("mass_kg", descending=True).head(limit)
