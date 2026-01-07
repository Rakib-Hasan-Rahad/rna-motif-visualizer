"""
RNA Motif Visualizer - Main Plugin Module
PyMOL plugin for visualizing RNA structural motifs with multi-database support.

Version: 2.0.0 (Scalable, Multi-Database)
Author: Structural Biology Lab
License: MIT

This module is the entry point when the plugin is loaded into PyMOL.
Supports multiple motif databases:
- RNA 3D Motif Atlas (JSON format)
- Rfam Motif Database (Stockholm format)
- Extensible to future databases and API sources

Usage in PyMOL:
    rna_load <PDB_ID>                    # Load with default database
    rna_load <PDB_ID>, database=atlas    # Load with RNA 3D Atlas
    rna_load <PDB_ID>, database=rfam     # Load with Rfam database
    rna_switch <database_id>             # Switch active database
    rna_databases                        # List available databases
    rna_status                           # Show current status
"""

from pymol import cmd
from .gui import initialize_gui
from .utils import initialize_logger
from .database import initialize_registry, get_registry
import os
from pathlib import Path


def __init_plugin__(app):
    """
    Initialize plugin in PyMOL with multi-database support.
    
    This function is called by PyMOL when the plugin is first loaded.
    
    Initialization steps:
    1. Setup logging
    2. Initialize database registry with all available providers
    3. Register GUI commands
    4. Print welcome message with usage instructions
    
    Args:
        app: PyMOL application instance
    """
    # Initialize logger
    plugin_dir = Path(__file__).parent
    logger = initialize_logger(use_pymol_console=True)
    
    # Initialize database registry with all available providers
    try:
        database_dir = plugin_dir / 'motif_database'
        logger.debug(f"Initializing database registry from {database_dir}")
        
        # Initialize registry - this registers all available providers
        registry = initialize_registry(str(database_dir))
        
        # Get summary of registered databases
        providers = registry.get_all_providers()
        total_pdbs = sum(len(p.get_available_pdb_ids()) for p in providers.values())
        total_motif_types = sum(len(p.get_available_motif_types()) for p in providers.values())
        
        logger.success(f"Loaded {len(providers)} database(s)")
        for pid, provider in providers.items():
            logger.debug(f"  {pid}: {provider.info.name} - "
                        f"{len(provider.get_available_motif_types())} motif types, "
                        f"{len(provider.get_available_pdb_ids())} PDB structures")
        
    except Exception as e:
        logger.error(f"Error initializing database registry: {e}")
        import traceback
        traceback.print_exc()
    
    # Initialize GUI and register commands
    initialize_gui()
    
    # Print welcome message
    print("\n" + "="*70)
    print("RNA MOTIF VISUALIZER v2.0.0 (MULTI-DATABASE)")
    print("="*70)
    print("Supports multiple motif databases with automatic switching!")
    print("")
    print("Available Databases:")
    try:
        for pid, provider in registry.get_all_providers().items():
            pdb_count = len(provider.get_available_pdb_ids())
            motif_count = len(provider.get_available_motif_types())
            print(f"  {pid:10s} - {provider.info.name}")
            print(f"              {motif_count} motif types, {pdb_count} PDB structures")
    except:
        print("  (Use rna_databases to list available databases)")
    print("")
    print("Quick Start:")
    print("  1. Load structure:     rna_load 4V9F")
    print("  2. Use specific DB:    rna_load 4V9F, database=atlas")
    print("  3. Switch database:    rna_switch rfam")
    print("  4. Toggle motifs:      rna_toggle HL on/off")
    print("  5. Check status:       rna_status")
    print("  6. List databases:     rna_databases")
    print("")
    print("Available motif types vary by database:")
    print("  RNA 3D Atlas: HL (hairpin loops), IL (internal loops)")
    print("                J3, J4, J5, J6, J7 (junctions)")
    print("  Rfam:         GNRA, T-loop, k-turn, sarcin-ricin, etc.")
    print("")
    print("Examples:")
    print("  rna_load 4V9F, database=atlas, bg_color=lightgray")
    print("  rna_load 3OWI, database=rfam")
    print("  rna_toggle IL off")
    print("  rna_switch atlas")
    print("="*70 + "\n")


# Module metadata
__all__ = ['__init_plugin__']
