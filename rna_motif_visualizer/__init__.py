"""RNA Motif Visualizer

PyMOL plugin for visualizing RNA structural motifs from multiple databases.

This package provides:
- 7 data sources (Atlas, Rfam, BGSU API, Rfam API, FR3D, RMS, RMSX)
- Split fetch pipeline: load PDB first, select source, fetch motifs
- Multi-source combine with cascade merge and Jaccard deduplication
- Label chain ID support (cif_use_auth=0)
- High-resolution image export with 8 representation options
- 18 PyMOL commands (rmv_help for full reference)

Author: CBB LAB @Rakib Hasan Rahad
Version: 2.3.0
"""

# NOTE:
# Keep this package importable outside PyMOL.
# PyMOL injects/provides the `pymol` module at runtime; importing it in a
# regular Python interpreter (e.g., during CLI tests) will fail.

__version__ = '2.3.0'
__author__ = 'CBB LAB @Rakib Hasan Rahad'


def __getattr__(name):
    """Lazy imports so non-PyMOL environments can import this package."""
    if name == '__init_plugin__':
        from .plugin import __init_plugin__ as value
        return value
    if name in {'get_gui', 'initialize_gui'}:
        from . import gui as _gui
        return getattr(_gui, name)
    if name == 'VisualizationManager':
        from .loader import VisualizationManager as value
        return value
    raise AttributeError(name)


__all__ = ['__init_plugin__', 'get_gui', 'initialize_gui', 'VisualizationManager']
