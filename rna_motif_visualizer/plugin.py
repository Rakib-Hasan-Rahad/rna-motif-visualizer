"""
RNA Motif Visualizer - Main Plugin Module
PyMOL plugin for visualizing RNA structural motifs using scalable Atlas database.

Version: 2.0.0 (Scalable)
Author: Structural Biology Lab
License: MIT

This module is the entry point when the plugin is loaded into PyMOL.
Now supports any PDB structure with automatic motif lookup from RNA 3D Atlas.
"""

from pymol import cmd
from .gui import initialize_gui
from .utils import initialize_logger
from .atlas_loader import get_atlas_loader
from .pdb_motif_mapper import get_pdb_mapper
import os
from pathlib import Path


def __init_plugin__(app):
    """
    Initialize plugin in PyMOL with scalable Atlas database support.
    
    This function is called by PyMOL when the plugin is first loaded.
    
    Initialization steps:
    1. Setup logging
    2. Initialize Atlas database and mapper
    3. Register GUI commands
    4. Print welcome message with usage instructions
    
    Args:
        app: PyMOL application instance
    """
    # Initialize logger
    plugin_dir = Path(__file__).parent
    logger = initialize_logger(use_pymol_console=True)
    
    # Pre-initialize scalable database components
    try:
        database_dir = plugin_dir / 'motif_database'
        logger.debug(f"Initializing Atlas database from {database_dir}")
        
        # Initialize and build the PDB index (this loads all JSON files)
        atlas_loader = get_atlas_loader(str(database_dir))
        _ = get_pdb_mapper(str(database_dir))
        
        logger.success(f"Atlas database loaded successfully")
        logger.debug(f"Available PDB structures in database: {len(atlas_loader.pdb_index)}")
        
    except Exception as e:
        logger.error(f"Error initializing Atlas database: {e}")
    
    # Initialize GUI and register commands
    initialize_gui()
    
    # Print welcome message
    print("\n" + "="*70)
    print("RNA MOTIF VISUALIZER v2.0.0 (SCALABLE)")
    print("="*70)
    print("Now supports ANY PDB structure with automatic motif lookup!")
    print("Using RNA 3D Atlas database with 1000+ structures and motifs.")
    print("\nQuick Start:")
    print("  1. Load structure:   rna_load 4V9F")
    print("  2. Load local file:  rna_load ~/my_structure.pdb")
    print("  3. Toggle motifs:    rna_toggle HL on/off")
    print("  4. Check status:     rna_status")
    print("  5. Change bg color:  rna_bg_color lightgray")
    print("\nAvailable motif types:")
    print("  Atlas database: HL (hairpin loops), IL (internal loops)")
    print("                  J3, J4, J5, J6, J7 (junctions)")
    print("\nBackground color options:")
    print("  gray80, gray60, gray40, white, lightgray, salmon, etc.")
    print("\nExample commands:")
    print("  rna_load 4V9F, bg_color=lightgray")
    print("  rna_load ~/rna.pdb, bg_color=white")
    print("  rna_toggle IL off       (hide internal loops)")
    print("  rna_toggle HL on        (show hairpin loops)")
    print("="*70 + "\n")


# Module metadata

__all__ = ['__init_plugin__']
