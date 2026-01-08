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
    
    def print_databases(self):
        """Print available databases to console."""
        print("\n" + "="*60)
        print("AVAILABLE MOTIF DATABASES")
        print("="*60)
        
        databases = self.list_databases()
        for db in databases:
            active_marker = " [ACTIVE]" if db.get('active') else ""
            print(f"\n{db['id']}{active_marker}")
            print(f"  Name: {db['name']}")
            print(f"  Description: {db['description']}")
            print(f"  Motif types: {db['motif_types']}")
            print(f"  PDB structures: {db['pdb_count']}")
        
        print("\n" + "="*60)
        print("To use a specific database:")
        print("  rna_load <PDB_ID>, database=atlas")
        print("  rna_load <PDB_ID>, database=rfam")
        print("  rna_switch <database_id>")
        print("="*60 + "\n")
    
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
            gui.print_databases()
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
    
    def list_databases():
        """PyMOL command: List available databases."""
        gui.print_databases()
    
    def set_bg_color(color_name='gray80'):
        """PyMOL command: Change background color of non-motif residues."""
        color_arg = str(color_name).strip()
        if not color_arg:
            color_arg = 'gray80'
        gui.set_background_color(color_arg)
    
    def motif_summary():
        """PyMOL command: Show detailed motif summary table."""
        gui.print_motif_summary()
    
    # Add commands to PyMOL
    cmd.extend('rna_load', load_structure)
    cmd.extend('rna_switch', switch_database)
    cmd.extend('rna_toggle', toggle_motif)
    cmd.extend('rna_status', motif_status)
    cmd.extend('rna_databases', list_databases)
    cmd.extend('rna_bg_color', set_bg_color)
    cmd.extend('rna_summary', motif_summary)
    
    gui.logger.success("RNA Motif Visualizer GUI initialized")
    gui.logger.info("Available commands:")
    gui.logger.info("  rna_load <PDB_ID> [, database=atlas|rfam] [, bg_color=gray80]")
    gui.logger.info("    - Load structure and visualize motifs from selected database")
    gui.logger.info("  rna_switch <database_id>")
    gui.logger.info("    - Switch to a different database and reload motifs")
    gui.logger.info("  rna_toggle <MOTIF_TYPE> <on|off>")
    gui.logger.info("    - Toggle motif visibility")
    gui.logger.info("  rna_status - Show current status")
    gui.logger.info("  rna_summary - Show detailed motif table with chains/residues")
    gui.logger.info("  rna_databases - List available databases")
    gui.logger.info("  rna_bg_color <COLOR_NAME> - Change background color")
    gui.logger.info("")
    gui.logger.info("Examples:")
    gui.logger.info("  rna_load 4V9F")
    gui.logger.info("  rna_load 4V9F, database=atlas")
    gui.logger.info("  rna_load 3OWI, database=rfam")
    gui.logger.info("  rna_switch rfam")
    gui.logger.info("  rna_toggle HL off")
