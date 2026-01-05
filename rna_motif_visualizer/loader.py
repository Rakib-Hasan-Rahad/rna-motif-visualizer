"""
RNA Motif Visualizer - Updated Loader Module
Handles loading structures and motif annotations using scalable Atlas database.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

from .utils import (
    PDBParser,
    MotifSelector,
    get_logger,
)
from . import colors
from .atlas_loader import get_atlas_loader
from .pdb_motif_mapper import get_pdb_mapper


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


class ScalableMotifLoader:
    """
    Loads motifs from the scalable Atlas database.
    Handles both Atlas motifs and legacy custom motifs.
    """
    
    def __init__(self, cmd, database_dir):
        """
        Initialize motif loader with scalable database.
        
        Args:
            cmd: PyMOL cmd module
            database_dir (str): Path to motif database directory
        """
        self.cmd = cmd
        self.database_dir = database_dir
        self.logger = get_logger()
        
        # Initialize new scalable components
        self.atlas_loader = get_atlas_loader(database_dir)
        self.pdb_mapper = get_pdb_mapper()
        
        self.selector = MotifSelector(cmd)
        self.loaded_motifs = {}  # Track loaded motif objects
    
    def load_motifs(self, structure_name: str, pdb_id: str) -> Dict:
        """
        Load all available motifs for a structure from Atlas database.
        Automatically queries all motif types and loads what's available.
        
        Args:
            structure_name (str): Name of structure in PyMOL
            pdb_id (str): PDB ID to look up motifs for
        
        Returns:
            dict: Dictionary of loaded motifs: {motif_type: {details}}
        """
        try:
            self.loaded_motifs = {}
            pdb_id = pdb_id.upper()
            
            # Get all available Atlas motifs for this PDB from mapper
            available_motifs = self.pdb_mapper.get_available_motifs(pdb_id)
            
            if not available_motifs:
                self.logger.warning(f"No motifs found for PDB {pdb_id}")
                return {}
            
            if available_motifs:
                self.logger.info(
                    f"Found {sum(len(m) for m in available_motifs.values())} Atlas motifs in {pdb_id}"
                )
            
            # Process each motif type
            for motif_type, instances in available_motifs.items():
                try:
                    self._load_motif_type(
                        structure_name, 
                        pdb_id, 
                        motif_type, 
                        instances
                    )
                except Exception as e:
                    self.logger.error(f"Error loading {motif_type} motifs: {e}")
                    continue
            
            return self.loaded_motifs
            
        except Exception as e:
            self.logger.error(f"Failed to load motifs: {e}")
            return {}
    
    def _load_motif_type(self, structure_name: str, pdb_id: str, 
                        motif_type: str, instances: List[Dict]) -> None:
        """
        Load a specific motif type and create PyMOL objects.
        
        Args:
            structure_name: PyMOL structure name
            pdb_id: PDB ID
            motif_type: Type of motif (HL, IL, J3, etc.)
            instances: List of motif instances
        """
        if not instances:
            return
        
        # Build motif_list in the format MotifSelector expects:
        # [{motif_id, chain, residues}, ...]
        motif_list: List[Dict] = []
        motif_details = []
        
        for instance in instances:
            motif_id = instance.get("motif_id", "unknown")
            instance_id = instance.get("instance_id", "")
            
            # Load actual residues for this motif instance
            residues = self.atlas_loader.load_motif_residues(
                pdb_id, 
                motif_type, 
                instance_id
            )
            
            if not residues:
                continue

            # Group residues by chain for robust selections
            by_chain: Dict[str, List[int]] = {}
            for nuc_type, res_num, chain in residues:
                by_chain.setdefault(chain, []).append(res_num)

            for chain, res_nums in by_chain.items():
                motif_list.append(
                    {
                        'motif_id': str(motif_id),
                        'chain': str(chain),
                        'residues': sorted(set(res_nums)),
                    }
                )

            motif_details.append({
                'motif_id': motif_id,
                'residues': residues,
                'instance_id': instance_id
            })
        
        if not motif_list:
            self.logger.debug(f"No residues found for {motif_type} motifs in {pdb_id}")
            return
        
        # Create PyMOL object for this motif type
        obj_name = self.selector.create_motif_class_object(
            structure_name,
            motif_type.upper(),
            motif_list,
        )
        
        if obj_name:
            # Color the motif
            motif_type_upper = motif_type.upper()
            colors.set_motif_color_in_pymol(self.cmd, obj_name, motif_type_upper)
            
            self.loaded_motifs[motif_type_upper] = {
                'object_name': obj_name,
                'count': len(instances),
                'visible': True,
                'motifs': motif_list,
                'motif_details': motif_details
            }
            
            self.logger.success(
                f"Loaded {len(instances)} {motif_type_upper} motifs into {obj_name}"
            )

    def toggle_motif_type(self, motif_type: str, visible: bool) -> bool:
        """
        Toggle visibility of a motif type.
        
        Args:
            motif_type (str): Motif type (e.g., 'HL', 'IL')
            visible (bool): True to show, False to hide
        
        Returns:
            bool: True if successful
        """
        motif_type = str(motif_type).upper().strip()
        motif_type = motif_type.replace('-', '_').replace(' ', '_')

        # Atlas-only: keep normalization simple and consistent.
        
        if motif_type not in self.loaded_motifs:
            self.logger.warning(f"Motif type {motif_type} not loaded")
            return False
        
        obj_name = self.loaded_motifs[motif_type]['object_name']
        self.selector.toggle_object_visibility(obj_name, visible)
        self.loaded_motifs[motif_type]['visible'] = visible
        return True
    
    def get_loaded_motifs(self) -> Dict:
        """Get dictionary of loaded motifs."""
        return self.loaded_motifs
    
    def clear_motifs(self) -> None:
        """Clear all loaded motif objects from PyMOL."""
        try:
            for motif_type, info in self.loaded_motifs.items():
                obj_name = info['object_name']
                self.selector.delete_object(obj_name)
            self.loaded_motifs = {}
            self.logger.info("Cleared all motif objects")
        except Exception as e:
            self.logger.error(f"Failed to clear motifs: {e}")
    
    def reload_motifs(self, structure_name: str, pdb_id: str) -> Dict:
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
    
    def get_available_motif_types(self, pdb_id: str) -> List[str]:
        """Get list of motif types available for a PDB."""
        pdb_id = pdb_id.upper()
        available = self.pdb_mapper.get_available_motifs(pdb_id)
        return sorted(list(available.keys()))


class VisualizationManager:
    """High-level manager for the entire visualization workflow."""
    
    def __init__(self, cmd, database_dir):
        """
        Initialize visualization manager with scalable components.
        
        Args:
            cmd: PyMOL cmd module
            database_dir (str): Path to motif database directory
        """
        self.cmd = cmd
        self.structure_loader = StructureLoader(cmd)
        self.motif_loader = ScalableMotifLoader(cmd, database_dir)
        self.logger = get_logger()
    
    def setup_clean_visualization(self, structure_name: str, 
                                 background_color: Optional[str] = None) -> None:
        """
        Set up clean RNA visualization with uniform color.
        Automatically displays all RNA chains with all motifs overlaid.
        
        Workflow:
        1. Hide everything
        2. Select all polymer.nucleic (all RNA chains)
        3. Show cartoon representation
        4. Set cartoon nucleic acid mode
        5. Color uniformly with background_color
        6. Motifs overlay on top with distinct colors
        
        Args:
            structure_name (str): Name of structure in PyMOL
            background_color (str): Color for the RNA (default: 'gray80')
        """
        try:
            if background_color is None:
                background_color = colors.NON_MOTIF_COLOR or 'gray80'
            
            # Step 1: Hide everything first
            self.cmd.hide('everything', 'all')
            self.logger.debug("Hidden all objects")
            
            # Step 2: Select ALL polymer.nucleic (all RNA chains in structure)
            rna_selection = f"{structure_name}_rna"
            self.cmd.select(rna_selection, f"{structure_name} and polymer.nucleic")
            self.logger.debug(f"Selected all RNA chains: {rna_selection}")
            
            # Step 3: Show cartoon representation
            self.cmd.show('cartoon', rna_selection)
            self.logger.debug("Showed cartoon representation")
            
            # Step 4: Set cartoon nucleic acid mode to 1
            self.cmd.set('cartoon_nucleic_acid_mode', 1)
            self.logger.debug("Set cartoon_nucleic_acid_mode = 1")
            
            # Step 5: Color uniformly
            self.cmd.color(background_color, rna_selection)
            self.logger.info(f"Visualization setup: All RNA shown as {background_color} cartoon")
            
            # Step 6: Clean up temporary selection (motifs will be shown on top)
            self.cmd.delete(rna_selection)
            
        except Exception as e:
            self.logger.error(f"Failed to set up clean visualization: {e}")
    
    def load_and_visualize(self, pdb_id_or_path: str, 
                          background_color: Optional[str] = None) -> Dict:
        """
        Complete workflow: load structure and automatically visualize all motifs.
        
        Automated workflow:
        1. Load structure (from PDB database or local file)
        2. Hide everything
        3. Select all polymer.nucleic chains
        4. Show cartoon with cartoon_nucleic_acid_mode = 1
        5. Color uniformly with background_color (default: gray80)
        6. Automatically load and overlay all motifs from Atlas database
        
        Args:
            pdb_id_or_path (str): PDB ID or file path
            background_color (str): Color for RNA backbone (default: 'gray80')
        
        Returns:
            dict: Loaded motifs, or empty dict if failed
        """
        # Load structure
        structure_name = self.structure_loader.load_structure(pdb_id_or_path)
        if not structure_name:
            return {}
        
        pdb_id = self.structure_loader.get_current_pdb_id()
        
        # Set up clean visualization with uniform color for all RNA chains
        self.setup_clean_visualization(structure_name, background_color)
        
        # Load motifs - they automatically overlay on the uniform backbone with distinct colors
        motifs = self.motif_loader.load_motifs(structure_name, pdb_id)
        return motifs
    
    def get_structure_info(self) -> Dict:
        """Get current structure and motif info."""
        return {
            'structure': self.structure_loader.get_current_structure(),
            'pdb_id': self.structure_loader.get_current_pdb_id(),
            'motifs': self.motif_loader.get_loaded_motifs()
        }
    
    def get_available_motif_summary(self, pdb_id: str) -> str:
        """Get summary of available motifs for a PDB."""
        motif_types = self.motif_loader.get_available_motif_types(pdb_id)
        if not motif_types:
            return f"No motifs found for {pdb_id}"
        return f"Available motifs: {', '.join(motif_types)}"
