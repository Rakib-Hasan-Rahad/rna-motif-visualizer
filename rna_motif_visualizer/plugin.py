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
    print("RNA MOTIF VISUALIZER v2.1.0 (SCALABLE, MULTI-SOURCE)")
    print("="*70)
    print("Now supports ~3000+ PDB structures via online APIs!")
    print("")
    print("Data Sources:")
    print("  LOCAL:  Bundled RNA 3D Atlas + Rfam databases (offline)")
    print("  BGSU:   BGSU RNA 3D Hub API (~3000+ PDBs with loop data)")
    print("  RFAM:   Rfam API (named motifs: GNRA, K-turn, T-loop, etc.)")
    print("")
    print("Quick Start:")
    print("  1. Load structure:     rna_load 4V9F")
    print("  2. Use API source:     rna_source bgsu")
    print("  3. Load any PDB:       rna_load 6ZMI")
    print("  4. Toggle motifs:      rna_toggle HL on/off")
    print("  5. Check status:       rna_status")
    print("")
    print("Source Modes (rna_source <mode>):")
    print("  auto  - Auto-select best source (local first, then API)")
    print("  local - Use only bundled databases (offline)")
    print("  bgsu  - Use BGSU RNA 3D Hub API")
    print("  rfam  - Use Rfam API")
    print("  all   - Combine all sources")
    print("")
    print("Commands:")
    print("  rna_load <PDB_ID>          Load structure and show motifs")
    print("  rna_source <mode>          Set data source mode")
    print("  rna_refresh [PDB_ID]       Force refresh from API")
    print("  rna_toggle <MOTIF> on/off  Toggle motif visibility")
    print("  rna_status                 Show current status")
    print("  rna_source_info            Show source config & cache")
    print("  rna_databases              List local databases")
    print("="*70 + "\n")


# Module metadata
__all__ = ['__init_plugin__']
