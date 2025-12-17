"""
RNA Motif Visualizer - GUI Module
Provides PyMOL GUI interface for the plugin.
"""

from pymol import cmd
from .loader import VisualizationManager
from .utils import get_logger
from . import colors
import os
from pathlib import Path


class MotifVisualizerGUI:
    """PyMOL GUI for RNA motif visualization."""
    
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
    
    def load_structure_action(self, pdb_id_or_path, background_color=None):
        """
        Load structure and automatically visualize all motifs on all RNA chains.
        
        Args:
            pdb_id_or_path (str): PDB ID or file path
            background_color (str): Color for RNA backbone (default: 'gray80')
        """
        try:
            self.logger.info(f"Loading structure: {pdb_id_or_path}")
            
            # Load and visualize with clean setup
            motifs = self.viz_manager.load_and_visualize(pdb_id_or_path, background_color)
            
            if not motifs:
                self.logger.warning("No motifs found or error loading structure")
                return
            
            # Update UI state
            self.motif_visibility = {}
            for motif_type, info in motifs.items():
                self.motif_visibility[motif_type] = True
            
            self.logger.success(f"Loaded {len(motifs)} motif types - now showing all RNA chains with motifs overlaid")
            
        except Exception as e:
            self.logger.error(f"Failed to load structure: {e}")
    
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
        Get list of available motif types.
        
        Returns:
            list: Motif type names
        """
        try:
            motif_types = self.viz_manager.motif_loader.parser.list_available_motif_types()
            return [mt.upper() for mt in motif_types]
        except Exception as e:
            self.logger.error(f"Failed to get motif types: {e}")
            return []
    
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
    
    def print_status(self):
        """Print current status to PyMOL console."""
        info = self.viz_manager.get_structure_info()
        
        print("\n" + "="*60)
        print("RNA MOTIF VISUALIZER - STATUS")
        print("="*60)
        
        if info['structure']:
            print(f"Structure: {info['structure']}")
            print(f"PDB ID: {info['pdb_id']}")
        else:
            print("No structure loaded")
            return
        
        if info['motifs']:
            print(f"\nLoaded Motifs ({len(info['motifs'])}):")
            for motif_type, data in info['motifs'].items():
                visible_str = "✓ visible" if data['visible'] else "✗ hidden"
                print(f"  {motif_type:20s} ({data['count']:2d} instances) {visible_str}")
        else:
            print("\nNo motifs loaded for this structure")
        
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
    def load_structure(pdb_id_or_path='', background_color=''):
        """PyMOL command: Load structure and automatically show all motifs.
        
        Usage:
            rna_load <pdb_id_or_path>
            rna_load <pdb_id_or_path>, bg_color=lightgray
        
        Automatically:
        - Hides everything
        - Selects all polymer.nucleic chains
        - Shows cartoon representation
        - Colors RNA with background_color
        - Displays all motifs with distinct colors
        """
        if not pdb_id_or_path:
            gui.logger.error("Usage: rna_load <PDB_ID_or_PATH> [, bg_color=gray80]")
            return
        
        pdb_arg = str(pdb_id_or_path).strip()
        bg_arg = str(background_color).strip() if background_color else None
        
        gui.load_structure_action(pdb_arg, bg_arg)
    
    def toggle_motif(motif_type='', visible=''):
        """PyMOL command: Toggle motif visibility."""
        # PyMOL can pass arguments different ways, so handle both
        
        # Case 1: Both arguments passed separately
        if motif_type and visible:
            motif_arg = motif_type
            visible_arg = visible
        else:
            # Case 2: Everything in motif_type as a single string
            # This happens when user types: rna_toggle KTURN on
            full_arg = str(motif_type).strip()
            parts = full_arg.split()
            
            if len(parts) < 2:
                gui.logger.error(f"Usage: rna_toggle MOTIF_TYPE on/off")
                gui.logger.error(f"Example: rna_toggle KTURN on")
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
    
    def set_bg_color(color_name='gray80'):
        """PyMOL command: Change background color of non-motif residues."""
        # Handle the color name argument
        color_arg = str(color_name).strip()
        if not color_arg:
            color_arg = 'gray80'
        gui.set_background_color(color_arg)
    
    # Add commands to PyMOL
    cmd.extend('rna_load', load_structure)
    cmd.extend('rna_toggle', toggle_motif)
    cmd.extend('rna_status', motif_status)
    cmd.extend('rna_bg_color', set_bg_color)
    
    gui.logger.success("RNA Motif Visualizer GUI initialized")
    gui.logger.info("Available commands:")
    gui.logger.info("  rna_load <PDB_ID_or_PATH> [, bg_color=gray80]")
    gui.logger.info("    - Load structure and automatically visualize all motifs")
    gui.logger.info("    - Displays all RNA chains uniformly, with motifs overlaid in distinct colors")
    gui.logger.info("    - bg_color: Color for RNA backbone (default: gray80)")
    gui.logger.info("  rna_toggle <MOTIF_TYPE> <on|off>")
    gui.logger.info("    - Toggle motif visibility")
    gui.logger.info("  rna_status - Show current status")
    gui.logger.info("  rna_bg_color <COLOR_NAME> - Change background color")
    gui.logger.info("")
    gui.logger.info("Examples:")
    gui.logger.info("  rna_load 1S72")
    gui.logger.info("  rna_load ~/structures/rna.pdb")
    gui.logger.info("  rna_load ~/structures/rna.pdb, bg_color=lightgray")
    gui.logger.info("  rna_toggle KINK-TURN off")
    gui.logger.info("  rna_status")
