"""
RNA Motif Visualizer - GUI Module
Provides PyMOL GUI interface for the plugin with multi-database support.

This module provides:
- MotifVisualizerGUI: Main GUI class for the plugin
- PyMOL command registration
- Database selection and switching functionality

Author: Structural Biology Lab
Version: 2.0.0
"""

from pymol import cmd
from .loader import VisualizationManager
from .utils import get_logger
from . import colors
from .database import get_registry
import os
from pathlib import Path


class MotifVisualizerGUI:
    """PyMOL GUI for RNA motif visualization with multi-database support."""
    
    def __init__(self):
        """Initialize GUI components."""
        self.logger = get_logger()
        
        # Get path to motif database
        plugin_dir = Path(__file__).parent
        self.database_dir = plugin_dir / 'motif_database'
        
        # Initialize visualization manager
        self.viz_manager = VisualizationManager(cmd, str(self.database_dir))
        
        # Track UI state
        self.motif_visibility = {}
    
    def load_structure_action(self, pdb_id_or_path, background_color=None,
                              database=None):
        """
        Load structure and automatically visualize all motifs.
        
        Args:
            pdb_id_or_path (str): PDB ID or file path
            background_color (str): Color for RNA backbone (default: 'gray80')
            database (str): Database to use ('atlas', 'rfam', or None for active)
        """
        try:
            self.logger.info(f"Loading structure: {pdb_id_or_path}")
            
            # Load and visualize with specified database
            motifs = self.viz_manager.load_and_visualize(
                pdb_id_or_path, 
                background_color,
                provider_id=database
            )
            
            if not motifs:
                self.logger.warning("No motifs found or error loading structure")
                return
            
            # Update UI state
            self.motif_visibility = {}
            for motif_type, info in motifs.items():
                self.motif_visibility[motif_type] = True
            
            self.logger.success(f"Loaded {len(motifs)} motif types")
            
        except Exception as e:
            self.logger.error(f"Failed to load structure: {e}")
    
    def switch_database_action(self, database_id):
        """
        Switch to a different database and reload motifs.
        
        Args:
            database_id (str): Database ID to switch to
        """
        try:
            # Check if structure is loaded
            info = self.viz_manager.get_structure_info()
            if not info.get('pdb_id'):
                # Just switch without reloading
                registry = get_registry()
                if registry.set_active_provider(database_id):
                    self.logger.success(f"Switched to database: {database_id}")
                else:
                    self.logger.error(f"Database not found: {database_id}")
                return
            
            # Reload with new database
            motifs = self.viz_manager.reload_with_database(database_id)
            
            if not motifs:
                self.logger.warning(f"No motifs found in {database_id}")
                return
            
            # Update UI state
            self.motif_visibility = {}
            for motif_type, info in motifs.items():
                self.motif_visibility[motif_type] = True
            
            self.logger.success(f"Reloaded with {len(motifs)} motif types from {database_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to switch database: {e}")
    
    def toggle_motif_action(self, motif_type, visible):
        """
        Toggle visibility of a motif type.
        
        Args:
            motif_type (str): Motif type
            visible (bool): Visibility state
        """
        try:
            success = self.viz_manager.motif_loader.toggle_motif_type(motif_type, visible)
            if success:
                self.motif_visibility[motif_type] = visible
                status = "shown" if visible else "hidden"
                self.logger.info(f"Motif {motif_type} {status}")
            else:
                self.logger.warning(f"Could not toggle motif {motif_type}")
        except Exception as e:
            self.logger.error(f"Failed to toggle motif visibility: {e}")
    
    def get_available_motifs(self):
        """
        Get list of available motif types for current PDB.
        
        Returns:
            list: Motif type names
        """
        try:
            pdb_id = self.viz_manager.structure_loader.get_current_pdb_id()
            if not pdb_id:
                return []
            
            motif_types = self.viz_manager.motif_loader.get_available_motif_types(pdb_id)
            return motif_types
        except Exception as e:
            self.logger.error(f"Failed to get motif types: {e}")
            return []
    
    def get_motif_summary(self, pdb_id):
        """
        Get human-readable summary of available motifs for a PDB.
        
        Args:
            pdb_id (str): PDB ID
            
        Returns:
            str: Summary text
        """
        try:
            return self.viz_manager.get_available_motif_summary(pdb_id)
        except Exception as e:
            self.logger.error(f"Failed to get motif summary: {e}")
            return "Error retrieving motif information"
    
    def set_background_color(self, color_name):
        """
        Change the background color of non-motif residues.
        
        Args:
            color_name (str): PyMOL color name (e.g., 'gray80', 'white', 'lightgray')
        """
        try:
            colors.set_background_color(color_name)
            # Recolor the current structure if one is loaded
            current_structure = self.viz_manager.structure_loader.get_current_structure()
            if current_structure:
                cmd.color(color_name, current_structure)
                self.logger.success(f"Background color changed to {color_name}")
            else:
                self.logger.info(f"Background color preference set to {color_name}")
        except Exception as e:
            self.logger.error(f"Failed to change background color: {e}")
    
    def get_motif_info(self, motif_type):
        """
        Get information about a motif type.
        
        Args:
            motif_type (str): Motif type
        
        Returns:
            dict: Motif information
        """
        motif_type_upper = motif_type.upper()
        
        loaded_motifs = self.viz_manager.motif_loader.get_loaded_motifs()
        
        if motif_type_upper not in loaded_motifs:
            return {
                'type': motif_type_upper,
                'loaded': False,
                'count': 0,
                'visible': False,
            }
        
        info = loaded_motifs[motif_type_upper]
        
        return {
            'type': motif_type_upper,
            'loaded': True,
            'count': info.get('count', 0),
            'visible': info.get('visible', False),
            'color': colors.get_color_name(motif_type_upper),
            'description': colors.MOTIF_LEGEND.get(motif_type_upper, {}).get('description', ''),
        }
    
    def list_databases(self):
        """
        List all available databases.
        
        Returns:
            list: Database information dictionaries
        """
        return self.viz_manager.get_available_databases()
    
    def print_status(self):
        """Print current status to PyMOL console."""
        info = self.viz_manager.get_structure_info()
        
        print("\n" + "="*60)
        print("RNA MOTIF VISUALIZER - STATUS")
        print("="*60)
        
        # Database info
        databases = self.list_databases()
        print("\nAvailable Databases:")
        for db in databases:
            active_marker = " [ACTIVE]" if db.get('active') else ""
            print(f"  {db['id']:10s} - {db['name']}{active_marker}")
            print(f"              {db['motif_types']} motif types, {db['pdb_count']} PDB structures")
        
        if info['structure']:
            print(f"\nLoaded Structure: {info['structure']}")
            print(f"PDB ID: {info['pdb_id']}")
            print(f"Using database: {info.get('database', 'N/A')}")
        else:
            print("\nNo structure loaded")
            print("\nTo get started:")
            print("  rna_load <PDB_ID>")
            print("  rna_load <PDB_ID>, database=rfam")
            return
        
        if info['motifs']:
            print(f"\nLoaded Motifs ({len(info['motifs'])}):")
            for motif_type, data in info['motifs'].items():
                visible_str = "✓ visible" if data['visible'] else "✗ hidden"
                print(f"  {motif_type:20s} ({data['count']:2d} instances) {visible_str}")
        else:
            print("\nNo motifs loaded for this structure")
        
        print("="*60 + "\n")
    
    def print_sources(self):
        """Print comprehensive source information - LOCAL and ONLINE separately."""
        print("\n" + "="*70)
        print("  RNA MOTIF DATA SOURCES")
        print("="*70)
        
        try:
            from .database import get_config, get_source_selector, SourceMode
            from .database.cache_manager import get_cache_manager
            
            config = get_config()
            
            # Current mode
            print(f"\n  Current Mode: {config.source_mode.value.upper()}")
            
            # LOCAL Sources
            print("\n" + "-"*70)
            print("  LOCAL SOURCES (Offline - Bundled with Plugin)")
            print("-"*70)
            
            source_selector = get_source_selector()
            if source_selector:
                local_sources = [(sid, p) for sid, p in source_selector.providers.items() 
                                if 'api' not in sid.lower()]
                for source_id, provider in local_sources:
                    print(f"\n  • {provider.info.name}")
                    print(f"    ID: {source_id}")
                    if hasattr(provider.info, 'description'):
                        print(f"    Description: {provider.info.description}")
                    # Get PDB count if available
                    pdbs = provider.get_supported_pdbs() if hasattr(provider, 'get_supported_pdbs') else []
                    if pdbs:
                        print(f"    Structures: {len(pdbs)} PDBs")
                    motif_types = provider.info.motif_types if hasattr(provider.info, 'motif_types') else []
                    if motif_types:
                        print(f"    Motif Types: {', '.join(motif_types)}")
                
                if not local_sources:
                    print("    No local sources available")
            
            # ONLINE Sources
            print("\n" + "-"*70)
            print("  ONLINE SOURCES (Require Internet)")
            print("-"*70)
            
            if source_selector:
                online_sources = [(sid, p) for sid, p in source_selector.providers.items() 
                                 if 'api' in sid.lower()]
                for source_id, provider in online_sources:
                    print(f"\n  • {provider.info.name}")
                    print(f"    ID: {source_id}")
                    if hasattr(provider.info, 'description'):
                        print(f"    Description: {provider.info.description}")
                    if 'bgsu' in source_id.lower():
                        print(f"    Coverage: ~3000+ RNA structures")
                    elif 'rfam' in source_id.lower():
                        print(f"    Coverage: Named RNA motif families")
                
                if not online_sources:
                    print("    No online sources available")
            
            # Cache info
            print("\n" + "-"*70)
            print("  CACHE STATUS")
            print("-"*70)
            cache_manager = get_cache_manager()
            if cache_manager and cache_manager.cache_dir.exists():
                cached_files = [f for f in cache_manager.cache_dir.glob("*.json") 
                               if not f.name.endswith('.meta.json')]
                print(f"  Directory: {cache_manager.cache_dir}")
                print(f"  Cached Entries: {len(cached_files)}")
                print(f"  Expiry: {config.freshness_policy.cache_days} days")
            else:
                print("  Cache not initialized")
            
        except ImportError:
            print("  Source system not initialized")
        
        # How to use
        print("\n" + "="*70)
        print("  HOW TO USE")
        print("="*70)
        print("""
  Set Source Mode:
    rna_source local     Use only local bundled databases (offline)
    rna_source bgsu      Use BGSU RNA 3D Hub API (3000+ structures)
    rna_source rfam      Use Rfam API (named motif families)
    rna_source auto      Auto-select (local first, then API) [DEFAULT]
    rna_source all       Combine all sources

  Load Structure:
    rna_load 1S72        Load using current source mode
    rna_load 4V9F        Load another structure

  Force Refresh:
    rna_refresh          Bypass cache, fetch fresh from API
""")
        print("="*70 + "\n")
    
    def print_help(self):
        """Print all available commands categorically."""
        print("\n" + "="*70)
        print("  RNA MOTIF VISUALIZER - COMMAND REFERENCE")
        print("="*70)
        
        print("""
┌──────────────────────────────────────────────────────────────────────┐
│  LOADING & SOURCES                                                   │
├──────────────────────────────────────────────────────────────────────┤
│  rna_load <PDB_ID>           Load structure and visualize motifs     │
│  rna_source                  Show current source mode & config       │
│  rna_source <MODE>           Set source (auto/local/bgsu/rfam/all)   │
│  rna_sources                 Show all available sources (detailed)   │
│  rna_switch <DB>             Switch database (atlas/rfam)            │
│  rna_refresh [PDB_ID]        Force refresh from API (bypass cache)   │
├──────────────────────────────────────────────────────────────────────┤
│  VISUALIZATION                                                       │
├──────────────────────────────────────────────────────────────────────┤
│  rna_all                     Show all motifs (reset view)            │
│  rna_show <MOTIF_TYPE>       Highlight specific motif type           │
│  rna_instance <TYPE> <NO>    View single instance (zoom + details)   │
│  rna_toggle <TYPE> <on|off>  Toggle motif visibility                 │
│  rna_bg_color <COLOR>        Change background color (e.g., gray80)  │
│  rna_color <TYPE> <COLOR>    Change motif color (e.g., rna_color HL blue) │
│  rna_colors                  Show color legend for motif types       │
├──────────────────────────────────────────────────────────────────────┤
│  INFORMATION                                                         │
├──────────────────────────────────────────────────────────────────────┤
│  rna_summary                 Show motif types and instance counts    │
│  rna_status                  Show current plugin status              │
│  rna_help                    Show this command reference             │
└──────────────────────────────────────────────────────────────────────┘

  EXAMPLES:
    rna_source bgsu              # Use BGSU API
    rna_load 1S72                # Load ribosome structure
    rna_show HL                  # Highlight hairpin loops
    rna_instance HL 5            # View instance #5 in detail
    rna_source                   # Check current source mode
""")
        print("="*70 + "\n")
    
    def print_motif_summary(self):
        """Print detailed motif summary table to console."""
        info = self.viz_manager.get_structure_info()
        
        if not info.get('pdb_id'):
            print("\nNo structure loaded. Use 'rna_load <PDB_ID>' first.\n")
            return
        
        pdb_id = info['pdb_id']
        motifs = info.get('motifs', {})
        
        if not motifs:
            print(f"\nNo motifs loaded for {pdb_id}.\n")
            return
        
        # Use the visualization manager's summary printer
        self.viz_manager._print_motif_summary_table(pdb_id, motifs, info.get('database_id'))
    
    def set_source_mode(self, mode: str):
        """
        Set the motif data source mode.
        
        Args:
            mode (str): Source mode: auto, local, bgsu, rfam, all
        """
        try:
            from .database import get_config, SourceMode
            
            mode_map = {
                'auto': SourceMode.AUTO,
                'local': SourceMode.LOCAL,
                'bgsu': SourceMode.BGSU,
                'rfam': SourceMode.RFAM,
                'all': SourceMode.ALL
            }
            
            mode_lower = mode.lower()
            if mode_lower not in mode_map:
                valid_modes = ', '.join(mode_map.keys())
                self.logger.error(f"Invalid source mode '{mode}'. Valid modes: {valid_modes}")
                return
            
            config = get_config()
            config.source_mode = mode_map[mode_lower]
            
            self.logger.success(f"Motif source mode set to: {mode_lower}")
            self._print_source_mode_info()
            
            # Print follow-up suggestions
            print("\n  Next steps:")
            print(f"    rna_load <PDB_ID>          Load a structure")
            print(f"    Example: rna_load 1S72")
            print()
            
        except Exception as e:
            self.logger.error(f"Failed to set source mode: {e}")
    
    def _print_source_mode_info(self):
        """Print information about current source mode."""
        try:
            from .database import get_config, SourceMode
            
            config = get_config()
            mode = config.source_mode
            
            mode_descriptions = {
                SourceMode.AUTO: "Automatically select best available source (local first, then API)",
                SourceMode.LOCAL: "Use only local bundled databases (offline mode)",
                SourceMode.BGSU: "Use only BGSU RNA 3D Hub API (online, ~3000+ PDBs)",
                SourceMode.RFAM: "Use only Rfam API (online, named motifs)",
                SourceMode.ALL: "Combine all sources (comprehensive, may have duplicates)"
            }
            
            print(f"\nCurrent mode: {mode.value}")
            print(f"Description: {mode_descriptions.get(mode, 'Unknown')}")
            
        except ImportError:
            print("Source selector not available")
    
    def refresh_motifs_action(self, pdb_id: str = None):
        """
        Force refresh motifs from API (bypass cache).
        
        Args:
            pdb_id (str): PDB ID to refresh (uses current if not specified)
        """
        try:
            info = self.viz_manager.get_structure_info()
            
            if not pdb_id:
                pdb_id = info.get('pdb_id')
            
            if not pdb_id:
                self.logger.error("No PDB ID specified and no structure loaded")
                return
            
            pdb_id = pdb_id.upper()
            self.logger.info(f"Force refreshing motifs for {pdb_id} from API...")
            
            # Clear cache for this PDB
            from .database import get_source_selector
            source_selector = get_source_selector()
            
            if source_selector:
                motifs, source = source_selector.get_motifs_for_pdb(pdb_id, force_refresh=True)
                
                if motifs:
                    total = sum(len(v) for v in motifs.values())
                    self.logger.success(f"Refreshed {total} motifs from {source}")
                    
                    # If this is the currently loaded structure, reload visualization
                    if info.get('pdb_id') == pdb_id and info.get('structure'):
                        self.logger.info("Reloading visualization...")
                        self.viz_manager.reload_with_database(None)
                else:
                    self.logger.warning(f"No motifs found for {pdb_id} in any source")
            else:
                self.logger.error("Source selector not available - API sources may not be initialized")
                
        except Exception as e:
            self.logger.error(f"Failed to refresh motifs: {e}")
    
    def print_source_info(self):
        """Print detailed source configuration and cache status."""
        print("\n" + "="*60)
        print("MOTIF DATA SOURCE CONFIGURATION")
        print("="*60)
        
        try:
            from .database import get_config, get_source_selector, SourceMode
            from .database.cache_manager import get_cache_manager
            
            config = get_config()
            
            # Source mode
            print(f"\nSource Mode: {config.source_mode.value}")
            mode_help = {
                SourceMode.AUTO: "  → Tries local databases first, then APIs if not found",
                SourceMode.LOCAL: "  → Uses only bundled databases (works offline)",
                SourceMode.BGSU: "  → Uses BGSU RNA 3D Hub API (requires internet)",
                SourceMode.RFAM: "  → Uses Rfam API (requires internet)",
                SourceMode.ALL: "  → Combines all sources (most comprehensive)"
            }
            print(mode_help.get(config.source_mode, ""))
            
            # Cache info
            cache_manager = get_cache_manager()
            if cache_manager:
                print(f"\nCache Directory: {cache_manager.cache_dir}")
                print(f"Cache Expiry: {config.freshness_policy.cache_days} days")
                
                # Count cached files
                if cache_manager.cache_dir.exists():
                    cached_files = list(cache_manager.cache_dir.glob("*.json"))
                    meta_files = list(cache_manager.cache_dir.glob("*.meta.json"))
                    data_files = [f for f in cached_files if not f.name.endswith('.meta.json')]
                    print(f"Cached Entries: {len(data_files)}")
            else:
                print("\nCache: Not initialized")
            
            # Source selector status
            source_selector = get_source_selector()
            if source_selector:
                print(f"\nRegistered Sources ({len(source_selector.providers)}):")
                for source_id, provider in source_selector.providers.items():
                    is_api = 'api' in source_id.lower()
                    source_type = "API" if is_api else "Local"
                    print(f"  {source_id:15s} [{source_type}] - {provider.info.name}")
            else:
                print("\nSource Selector: Not initialized")
            
            # Last source used
            loader = self.viz_manager.motif_loader
            if hasattr(loader, 'get_last_source_used'):
                last_source = loader.get_last_source_used()
                if last_source:
                    print(f"\nLast Source Used: {last_source}")
            
        except ImportError as e:
            print(f"\nNote: Advanced source features not available ({e})")
            print("Using standard database registry only.")
        
        print("\n" + "="*60)
        print("Commands:")
        print("  rna_source auto   - Auto-select best source")
        print("  rna_source local  - Use only local databases")
        print("  rna_source bgsu   - Use BGSU API (3000+ PDBs)")
        print("  rna_source rfam   - Use Rfam API")
        print("  rna_source all    - Combine all sources")
        print("  rna_switch <DB>   - Switch database (atlas/rfam)")
        print("  rna_refresh       - Force refresh from API")
        print("  rna_source        - Show this information again")
        print("="*60 + "\n")


# Global GUI instance
_gui_instance = None


def get_gui():
    """Get or create global GUI instance."""
    global _gui_instance
    if _gui_instance is None:
        _gui_instance = MotifVisualizerGUI()
    return _gui_instance


def initialize_gui():
    """Initialize GUI and register commands."""
    gui = get_gui()
    
    # Register PyMOL commands
    def load_structure(pdb_id_or_path='', background_color='', database=''):
        """PyMOL command: Load structure and automatically show all motifs.
        
        Usage:
            rna_load <pdb_id_or_path>
            rna_load <pdb_id_or_path>, bg_color=lightgray
            rna_load <pdb_id_or_path>, database=atlas
            rna_load <pdb_id_or_path>, database=rfam, bg_color=white
        """
        if not pdb_id_or_path:
            gui.logger.error("Usage: rna_load <PDB_ID_or_PATH> [, bg_color=gray80] [, database=atlas]")
            return
        
        pdb_arg = str(pdb_id_or_path).strip()
        bg_arg = str(background_color).strip() if background_color else None
        db_arg = str(database).strip() if database else None
        
        gui.load_structure_action(pdb_arg, bg_arg, db_arg)
    
    def switch_database(database_id=''):
        """PyMOL command: Switch to a different database.
        
        Usage:
            rna_switch atlas
            rna_switch rfam
        """
        if not database_id:
            gui.print_sources()
            return
        
        gui.switch_database_action(str(database_id).strip())
    
    def toggle_motif(motif_type='', visible=''):
        """PyMOL command: Toggle motif visibility."""
        # PyMOL can pass arguments different ways, so handle both
        
        # Case 1: Both arguments passed separately
        if motif_type and visible:
            motif_arg = motif_type
            visible_arg = visible
        else:
            # Case 2: Everything in motif_type as a single string
            full_arg = str(motif_type).strip()
            parts = full_arg.split()
            
            if len(parts) < 2:
                gui.logger.error(f"Usage: rna_toggle MOTIF_TYPE on/off")
                gui.logger.error(f"Example: rna_toggle HL on")
                return
            
            motif_arg = parts[0]
            visible_arg = parts[1]
        
        # Parse visibility
        visible_bool = str(visible_arg).lower() in ['on', 'true', '1', 'yes', 'show']
        motif_arg = str(motif_arg).upper().strip()
        
        gui.toggle_motif_action(motif_arg, visible_bool)
    
    def motif_status():
        """PyMOL command: Show plugin status."""
        gui.print_status()
    
    def list_sources():
        """PyMOL command: Show available data sources."""
        gui.print_sources()
    
    def show_help():
        """PyMOL command: Show all available commands."""
        gui.print_help()
    
    def set_bg_color(color_name='gray80'):
        """PyMOL command: Change background color of non-motif residues."""
        color_arg = str(color_name).strip()
        if not color_arg:
            color_arg = 'gray80'
        gui.set_background_color(color_arg)
    
    def motif_summary():
        """PyMOL command: Show detailed motif summary table."""
        gui.print_motif_summary()
    
    def set_source(mode=''):
        """PyMOL command: Set motif data source mode.
        
        Usage:
            rna_source auto   - Auto-select best available source
            rna_source local  - Use only local bundled databases
            rna_source bgsu   - Use BGSU RNA 3D Hub API (~3000+ PDBs)
            rna_source rfam   - Use Rfam API (named motifs)
            rna_source all    - Combine all sources
        """
        if not mode:
            gui.print_source_info()
            return
        
        gui.set_source_mode(str(mode).strip())
    
    def refresh_motifs(pdb_id=''):
        """PyMOL command: Force refresh motifs from API (bypass cache).
        
        Usage:
            rna_refresh        - Refresh current structure
            rna_refresh 4V9F   - Refresh specific PDB
        """
        pdb_arg = str(pdb_id).strip() if pdb_id else None
        gui.refresh_motifs_action(pdb_arg)
    
    def show_motif(motif_type=''):
        """PyMOL command: Show specific motif type, hide others, print instance table.
        
        Usage:
            rna_show GNRA      - Show only GNRA motifs
            rna_show HL        - Show only hairpin loops
        """
        if not motif_type:
            gui.logger.error("Usage: rna_show <MOTIF_TYPE>")
            gui.logger.error("Example: rna_show GNRA")
            return
        
        motif_arg = str(motif_type).strip().upper()
        gui.viz_manager.show_motif_type(motif_arg)
    
    def show_instance(motif_type='', instance_no=''):
        """PyMOL command: Show specific instance of a motif type.
        
        Usage:
            rna_instance GNRA 1   - Show GNRA instance #1
            rna_instance HL 3     - Show hairpin loop instance #3
        """
        # Handle both separate args and combined string
        if motif_type and instance_no:
            motif_arg = str(motif_type).strip().upper()
            try:
                no_arg = int(instance_no)
            except ValueError:
                gui.logger.error("Instance number must be an integer")
                return
        else:
            # Parse combined string
            full_arg = str(motif_type).strip()
            parts = full_arg.split()
            
            if len(parts) < 2:
                gui.logger.error("Usage: rna_instance <MOTIF_TYPE> <NO>")
                gui.logger.error("Example: rna_instance GNRA 1")
                return
            
            motif_arg = parts[0].upper()
            try:
                no_arg = int(parts[1])
            except ValueError:
                gui.logger.error("Instance number must be an integer")
                return
        
        gui.viz_manager.show_motif_instance(motif_arg, no_arg)
    
    def show_all():
        """PyMOL command: Show all motifs (reset to default view)."""
        gui.viz_manager.show_all_motifs()
    
    # Add commands to PyMOL
    cmd.extend('rna_load', load_structure)
    cmd.extend('rna_switch', switch_database)
    cmd.extend('rna_toggle', toggle_motif)
    cmd.extend('rna_status', motif_status)
    cmd.extend('rna_sources', list_sources)
    cmd.extend('rna_help', show_help)
    cmd.extend('rna_bg_color', set_bg_color)
    cmd.extend('rna_summary', motif_summary)
    cmd.extend('rna_source', set_source)
    cmd.extend('rna_refresh', refresh_motifs)
    cmd.extend('rna_show', show_motif)
    cmd.extend('rna_instance', show_instance)
    cmd.extend('rna_all', show_all)
    
    def show_colors():
        """PyMOL command: Show color legend for all motif types."""
        from . import colors as color_module
        loaded = gui.viz_manager.motif_loader.get_loaded_motifs()
        if loaded:
            color_module.print_color_legend(loaded)
        else:
            color_module.print_color_legend()
    
    cmd.extend('rna_colors', show_colors)
    
    def set_motif_color(motif_type='', color=''):
        """PyMOL command: Change color of a specific motif type.
        
        Usage:
            rna_color HL red         Change HL to red
            rna_color GNRA blue      Change GNRA to blue
            rna_color IL 0.5 1.0 0.5 Change IL to RGB values
        
        Available colors: red, green, blue, yellow, cyan, magenta, orange,
                         pink, purple, teal, gold, coral, turquoise, etc.
        """
        if not motif_type:
            print("\nUsage: rna_color <MOTIF_TYPE> <COLOR>")
            print("Examples:")
            print("  rna_color HL red")
            print("  rna_color GNRA blue")
            print("  rna_color IL green")
            print("\nAvailable colors: red, green, blue, yellow, cyan, magenta,")
            print("                  orange, pink, purple, teal, gold, coral, etc.")
            return
        
        if not color:
            gui.logger.error("Please specify a color")
            gui.logger.error("Example: rna_color HL red")
            return
        
        from . import colors as color_module
        
        motif_arg = str(motif_type).strip().upper()
        color_arg = str(color).strip().lower()
        
        # Set the custom color
        result = color_module.set_custom_motif_color(motif_arg, color_arg)
        
        gui.logger.success(f"Changed {motif_arg} color to {color_arg}")
        
        # Re-apply color to currently loaded motifs if any
        loaded_motifs = gui.viz_manager.motif_loader.get_loaded_motifs()
        if motif_arg in loaded_motifs:
            info = loaded_motifs[motif_arg]
            structure_name = info.get('structure_name')
            main_selection = info.get('main_selection')
            
            # Re-color the motif residues in the structure
            if main_selection:
                try:
                    color_module.set_motif_color_in_pymol(cmd, main_selection, motif_arg)
                    gui.logger.info(f"Applied new color to {motif_arg} residues")
                except Exception as e:
                    gui.logger.debug(f"Could not apply color: {e}")
        
        print(f"\n  {motif_arg} is now colored {color_arg}")
        print(f"  Use 'rna_show {motif_arg}' or 'rna_all' to see the change\n")
    
    cmd.extend('rna_color', set_motif_color)
    
    gui.logger.success("RNA Motif Visualizer GUI initialized")
    gui.logger.info("")
    gui.logger.info("Quick Start:")
    gui.logger.info("  rna_source bgsu         Set source to BGSU API (3000+ structures)")
    gui.logger.info("  rna_load 1S72           Load and visualize motifs")
    gui.logger.info("  rna_show HL             Highlight hairpin loops")
    gui.logger.info("  rna_instance HL 1       View specific instance")
    gui.logger.info("")
    gui.logger.info("  rna_help                Show all commands")
    gui.logger.info("  rna_sources             Show available data sources")
    gui.logger.info("")
