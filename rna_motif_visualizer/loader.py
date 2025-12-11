"""
RNA Motif Visualizer - Loader Module
Handles loading structures and motif annotations into PyMOL.
"""

import os
from pathlib import Path
from .utils import (
    MotifDatabaseParser,
    PDBParser,
    MotifSelector,
    get_logger,
)
from . import colors


class StructureLoader:
    """Handles loading RNA structures into PyMOL."""
    
    def __init__(self, cmd):
        """
        Initialize loader.
        
        Args:
            cmd: PyMOL cmd module
        """
        self.cmd = cmd
        self.logger = get_logger()
        self.current_structure = None
        self.current_pdb_id = None
    
    def load_structure(self, pdb_id_or_path):
        """
        Load an RNA structure into PyMOL.
        
        Args:
            pdb_id_or_path (str): Either a PDB ID or local file path
        
        Returns:
            str: Name of loaded structure in PyMOL, or None if failed
        """
        try:
            # Determine if it's a PDB ID or file path
            if os.path.isfile(pdb_id_or_path):
                # Local file
                self.logger.info(f"Loading structure from file: {pdb_id_or_path}")
                structure_name = Path(pdb_id_or_path).stem
                self.cmd.load(pdb_id_or_path, structure_name)
                pdb_id = PDBParser.extract_pdb_id(pdb_id_or_path)
            else:
                # Assume PDB ID
                pdb_id = pdb_id_or_path.strip().upper()
                if not PDBParser.is_valid_pdb_id(pdb_id):
                    self.logger.error(f"Invalid PDB ID format: {pdb_id}")
                    return None
                
                self.logger.info(f"Downloading structure from RCSB: {pdb_id}")
                structure_name = pdb_id
                self.cmd.fetch(pdb_id, structure_name)
            
            self.current_structure = structure_name
            self.current_pdb_id = pdb_id
            
            self.logger.success(f"Loaded structure: {structure_name} (PDB: {pdb_id})")
            return structure_name
            
        except Exception as e:
            self.logger.error(f"Failed to load structure: {e}")
            return None
    
    def get_current_structure(self):
        """Get name of currently loaded structure."""
        return self.current_structure
    
    def get_current_pdb_id(self):
        """Get PDB ID of currently loaded structure."""
        return self.current_pdb_id


class MotifLoader:
    """Handles loading motif annotations and creating motif objects."""
    
    def __init__(self, cmd, database_dir):
        """
        Initialize motif loader.
        
        Args:
            cmd: PyMOL cmd module
            database_dir (str): Path to motif database directory
        """
        self.cmd = cmd
        self.database_dir = database_dir
        self.logger = get_logger()
        self.parser = MotifDatabaseParser(database_dir)
        self.selector = MotifSelector(cmd)
        self.loaded_motifs = {}  # Track loaded motif objects
    
    def load_motifs(self, structure_name, pdb_id):
        """
        Load all available motifs for a structure.
        
        Args:
            structure_name (str): Name of structure in PyMOL
            pdb_id (str): PDB ID to look up motifs for
        
        Returns:
            dict: Dictionary of loaded motifs: {motif_type: [object_names]}
        """
        try:
            self.loaded_motifs = {}
            motif_types = self.parser.list_available_motif_types()
            
            if not motif_types:
                self.logger.warning("No motif database files found")
                return {}
            
            self.logger.info(f"Available motif types: {', '.join(motif_types)}")
            
            for motif_type in motif_types:
                motifs = self.parser.get_motifs_for_pdb(pdb_id, motif_type)
                
                if not motifs:
                    self.logger.debug(f"No {motif_type} motifs found for {pdb_id}")
                    continue
                
                # Create PyMOL object for this motif type
                obj_name = self.selector.create_motif_class_object(
                    structure_name,
                    motif_type.upper(),
                    motifs
                )
                
                if obj_name:
                    # Color the motif
                    motif_type_upper = motif_type.upper()
                    colors.set_motif_color_in_pymol(self.cmd, obj_name, motif_type_upper)
                    
                    self.loaded_motifs[motif_type_upper] = {
                        'object_name': obj_name,
                        'count': len(motifs),
                        'visible': True
                    }
                    
                    self.logger.success(
                        f"Loaded {len(motifs)} {motif_type_upper} motifs "
                        f"into {obj_name}"
                    )
            
            return self.loaded_motifs
            
        except Exception as e:
            self.logger.error(f"Failed to load motifs: {e}")
            return {}
    
    def toggle_motif_type(self, motif_type, visible):
        """
        Toggle visibility of a motif type.
        
        Args:
            motif_type (str): Motif type (e.g., 'KTURN')
            visible (bool): True to show, False to hide
        
        Returns:
            bool: True if successful
        """
        motif_type = motif_type.upper()
        
        if motif_type not in self.loaded_motifs:
            self.logger.warning(f"Motif type {motif_type} not loaded")
            return False
        
        obj_name = self.loaded_motifs[motif_type]['object_name']
        self.selector.toggle_object_visibility(obj_name, visible)
        self.loaded_motifs[motif_type]['visible'] = visible
        return True
    
    def get_loaded_motifs(self):
        """Get dictionary of loaded motifs."""
        return self.loaded_motifs
    
    def clear_motifs(self):
        """Clear all loaded motif objects from PyMOL."""
        try:
            for motif_type, info in self.loaded_motifs.items():
                obj_name = info['object_name']
                self.selector.delete_object(obj_name)
            self.loaded_motifs = {}
            self.logger.info("Cleared all motif objects")
        except Exception as e:
            self.logger.error(f"Failed to clear motifs: {e}")
    
    def reload_motifs(self, structure_name, pdb_id):
        """
        Reload motifs (clear and reload).
        
        Args:
            structure_name (str): Name of structure in PyMOL
            pdb_id (str): PDB ID
        
        Returns:
            dict: Loaded motifs
        """
        self.clear_motifs()
        return self.load_motifs(structure_name, pdb_id)


class VisualizationManager:
    """High-level manager for the entire visualization workflow."""
    
    def __init__(self, cmd, database_dir):
        """
        Initialize visualization manager.
        
        Args:
            cmd: PyMOL cmd module
            database_dir (str): Path to motif database directory
        """
        self.cmd = cmd
        self.structure_loader = StructureLoader(cmd)
        self.motif_loader = MotifLoader(cmd, database_dir)
        self.logger = get_logger()
    
    def load_and_visualize(self, pdb_id_or_path):
        """
        Complete workflow: load structure and visualize motifs.
        
        Args:
            pdb_id_or_path (str): PDB ID or file path
        
        Returns:
            dict: Loaded motifs, or empty dict if failed
        """
        # Load structure
        structure_name = self.structure_loader.load_structure(pdb_id_or_path)
        if not structure_name:
            return {}
        
        pdb_id = self.structure_loader.get_current_pdb_id()
        
        # Load motifs
        motifs = self.motif_loader.load_motifs(structure_name, pdb_id)
        return motifs
    
    def get_structure_info(self):
        """Get current structure and motif info."""
        return {
            'structure': self.structure_loader.get_current_structure(),
            'pdb_id': self.structure_loader.get_current_pdb_id(),
            'motifs': self.motif_loader.get_loaded_motifs()
        }
