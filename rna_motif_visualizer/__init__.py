"""
RNA Motif Visualizer
PyMOL plugin for visualizing pre-annotated RNA structural motifs.

This package provides:
- Automatic loading of RNA structures from RCSB or local files
- JSON-based motif database system
- PyMOL visualization of K-turns, A-minors, GNRA tetraloops, and more
- Intuitive GUI for toggling motif visibility
- Fast, lightweight, and requires no external tools

Author: Structural Biology Lab
Version: 1.0.0
"""

from .plugin import __init_plugin__
from .gui import get_gui, initialize_gui
from .loader import VisualizationManager

__version__ = '1.0.0'
__author__ = 'Structural Biology Lab'
__all__ = [
    '__init_plugin__',
    'get_gui',
    'initialize_gui',
    'VisualizationManager',
]
