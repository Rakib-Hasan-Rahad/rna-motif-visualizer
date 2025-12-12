"""
RNA Motif Visualizer - Main Plugin Module
PyMOL plugin for visualizing pre-annotated RNA structural motifs.

Version: 1.0.0
Author: Structural Biology Lab
License: MIT

This module is the entry point when the plugin is loaded into PyMOL.
"""

from pymol import cmd
from .gui import initialize_gui
from .utils import initialize_logger
import os
from pathlib import Path


def __init_plugin__(app):
    """
    Initialize plugin in PyMOL.
    
    This function is called by PyMOL when the plugin is first loaded.
    
    Args:
        app: PyMOL application instance
    """
    # Initialize logger
    plugin_dir = Path(__file__).parent
    initialize_logger(use_pymol_console=True)
    
    # Initialize GUI and register commands
    initialize_gui()
    
    # Print welcome message
    print("\n" + "="*60)
    print("RNA MOTIF VISUALIZER v1.0.0")
    print("="*60)
    print("Ready to visualize RNA structural motifs!")
    print("\nQuick Start:")
    print("  1. Load a structure: rna_load 1S72")
    print("  2. Toggle motifs: rna_toggle KTURN on/off")
    print("  3. Check status: rna_status")
    print("  4. Change bg color: rna_bg_color gray80")
    print("\nBackground color options:")
    print("  gray80, gray60, gray40, white, lightgray, etc.")
    print("="*60 + "\n")


# Module metadata
__all__ = ['__init_plugin__']
