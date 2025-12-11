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
    
    def load_structure_action(self, pdb_id_or_path):
        """
        Load structure and automatically visualize motifs.
        
        Args:
            pdb_id_or_path (str): PDB ID or file path
        """
        try:
            self.logger.info(f"Loading structure: {pdb_id_or_path}")
            
            # Load and visualize
            motifs = self.viz_manager.load_and_visualize(pdb_id_or_path)
            
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
    def load_structure(pdb_id_or_path):
        """PyMOL command: Load structure and show motifs."""
        gui.load_structure_action(pdb_id_or_path)
    
    def toggle_motif(motif_type, visible="on"):
        """PyMOL command: Toggle motif visibility."""
        visible_bool = visible.lower() in ['on', 'true', '1', 'yes']
        gui.toggle_motif_action(motif_type, visible_bool)
    
    def motif_status():
        """PyMOL command: Show plugin status."""
        gui.print_status()
    
    # Add commands to PyMOL
    cmd.extend('rna_load', load_structure)
    cmd.extend('rna_toggle', toggle_motif)
    cmd.extend('rna_status', motif_status)
    
    gui.logger.success("RNA Motif Visualizer GUI initialized")
    gui.logger.info("Available commands: rna_load, rna_toggle, rna_status")
