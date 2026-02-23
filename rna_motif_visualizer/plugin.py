"""
RNA Motif Visualizer - Main Plugin Module
PyMOL plugin for visualizing RNA structural motifs with multi-database support.

Version: 2.3.0
Author: CBB LAB @Rakib Hasan Rahad
License: MIT

This module is the entry point when the plugin is loaded into PyMOL.
Supports 7 data sources:
- RNA 3D Motif Atlas [1], Rfam [2] (bundled, offline)
- BGSU RNA 3D Hub [3], Rfam API [4] (online)
- FR3D [5], RNAMotifScan [6], RNAMotifScanX [7] (user annotations)

Usage in PyMOL:
    rmv_fetch 1S72                # Load PDB structure
    rmv_source 3                  # Select data source (BGSU)
    rmv_motifs                    # Fetch motif data
    rmv_summary                   # View motif summary
    rmv_show HL                   # Render hairpin loops
    rmv_help                      # Full command reference
"""

from pymol import cmd
from pathlib import Path
from .gui import initialize_gui
from .utils import initialize_logger
from .database import initialize_registry, get_registry
from datetime import datetime


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
    
    # Layer 1: Lock chain ID convention to auth_asym_id
    # This ensures PyMOL uses auth_asym_id as the 'chain' property when loading
    # CIF files, which matches the convention used by BGSU, Atlas, and other
    # motif annotation sources. The label_asym_id is stored in 'segi' as fallback.
    try:
        cmd.set("cif_use_auth", 1)
        logger.debug("Chain ID convention locked: cif_use_auth=1 (auth_asym_id)")
    except Exception as e:
        logger.warning(f"Could not set cif_use_auth: {e}")
    
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
    
    # Print professional welcome message
    last_updated = "20 February 2026"
    print("\n" + "="*80)
    print("┌" + " "*78 + "┐")
    print("│" + " "*20 + "🧬 RNA MOTIF VISUALIZER 🧬" + " "*32 + "│")
    print("│" + " "*78 + "│")
    print("│" + " Version 2.3.0" + " "*63 + "│")
    print("│" + " Last Updated: " + last_updated + " "*42 + "│")
    print("│" + " "*78 + "│")
    print("│" + " Multi-source RNA structural motif visualization for PyMOL" + " "*18 + "│")
    print("│" + " Fast loading: Load PDB first, select source, fetch motifs" + " "*19 + "│")
    print("│" + " "*78 + "│")
    print("└" + " "*78 + "┘")
    print("="*80)
    print("\n📊 AVAILABLE DATA SOURCES:")
    print("   • Local:       RNA 3D Atlas [1], Rfam [2] (offline)")
    print("   • Online:      BGSU RNA 3D Hub [3], Rfam API [4]")
    print("   • Annotations: FR3D [5], RNAMotifScan [6], RNAMotifScanX [7]")
    print("\n⚡ QUICK START:")
    print("   rmv_fetch 1S72            # Load PDB structure")
    print("   rmv_source 3              # Select BGSU API source")
    print("   rmv_motifs                # Fetch motif data from source")
    print("   rmv_summary               # Show available motifs")
    print("   rmv_show HL               # Render hairpin loops")
    print("\n📚 COMMANDS & HELP:")
    print("   rmv_help                  # All available commands")
    print("   rmv_sources               # List all data sources")
    print("   rmv_status                # Current plugin status")
    print("\n" + "="*80 + "\n")


# Module metadata
__all__ = ['__init_plugin__']
