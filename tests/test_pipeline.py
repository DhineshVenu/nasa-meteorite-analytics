from pathlib import Path
import polars as pl
import pytest
from src.data_pipeline import MeteoriteDataEngine


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """Creates a temporary sample CSV matching NASA dataset schema."""
    csv_content = (
        "name,id,nametype,recclass,mass (g),fall,year,reclat,reclong,GeoLocation\n"
        'Aachen,1,Valid,L5,21,Fell,1880,50.775,6.08333,"(50.775, 6.08333)"\n'
        'Aarhus,2,Valid,H6,720,Fell,1951,56.18333,10.23333,"(56.18333, 10.23333)"\n'
        'Abee,6,Valid,EH4,107000,Fell,1952,54.21667,-113.0,"(54.21667, -113.0)"\n'
    )
    file_path = tmp_path / "test_meteorites.csv"
    file_path.write_text(csv_content)
    return file_path


def test_data_loading_and_cleaning(sample_csv: Path):
    engine = MeteoriteDataEngine(str(sample_csv))
    df = engine.load_data()

    assert isinstance(df, pl.DataFrame)
    assert len(df) == 3
    assert "mass_kg" in df.columns
    assert df["mass_kg"][0] == pytest.approx(0.021)
    assert df["mass_kg"][2] == pytest.approx(107.0)


def test_summary_metrics(sample_csv: Path):
    engine = MeteoriteDataEngine(str(sample_csv))
    engine.load_data()
    metrics = engine.get_summary_metrics()

    assert metrics["total_landings"] == 3
    assert metrics["largest_name"] == "Abee"
    assert metrics["largest_mass_kg"] == pytest.approx(107.0)


def test_top_landings_sorting(sample_csv: Path):
    engine = MeteoriteDataEngine(str(sample_csv))
    engine.load_data()
    top_df = engine.get_top_landings(limit=2)

    assert len(top_df) == 2
    assert top_df["name"][0] == "Abee"
    assert top_df["name"][1] == "Aarhus"
