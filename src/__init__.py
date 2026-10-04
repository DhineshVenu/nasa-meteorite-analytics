"""
NASA Meteorite Analytics Package
--------------------------------
An end-to-end data processing and dynamic visualization platform.
"""

from .data_pipeline import MeteoriteDataEngine
from .manim_renderer import MeteoriteExplainerScene
from .plotly_engine import PlotlyEngine

__version__ = "1.0.0"
__all__ = ["MeteoriteDataEngine", "PlotlyEngine", "MeteoriteExplainerScene"]
