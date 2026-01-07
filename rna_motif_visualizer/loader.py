"""
RNA Motif Visualizer - Updated Loader Module
Handles loading structures and motif annotations using scalable database providers.

This module provides:
- StructureLoader: Loads PDB structures into PyMOL
- UnifiedMotifLoader: Loads motifs from any registered database provider
- VisualizationManager: Coordinates the complete visualization workflow

The loader now uses the database registry to support multiple databases
(RNA 3D Atlas, Rfam, etc.) with a unified interface.

Author: Structural Biology Lab
Version: 2.0.0
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
from .database import (
    get_registry,
    MotifInstance,
)


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


class UnifiedMotifLoader:
    """
    Unified motif loader that works with any database provider.
    
    Uses the database registry to load motifs from the active database
    or any specified database provider.
    """
    
    def __init__(self, cmd, database_dir: str):
        """
        Initialize motif loader.
        
        Args:
            cmd: PyMOL cmd module
            database_dir (str): Path to motif database directory
        """
        self.cmd = cmd
        self.database_dir = database_dir
        self.logger = get_logger()
        self.selector = MotifSelector(cmd)
        self.loaded_motifs: Dict[str, Dict] = {}  # Track loaded motif objects
        
        # Get registry
        self._registry = get_registry()
    
    def load_motifs(self, structure_name: str, pdb_id: str,
                   provider_id: Optional[str] = None) -> Dict:
        """
        Load all available motifs for a structure.
        
        Args:
            structure_name (str): Name of structure in PyMOL
            pdb_id (str): PDB ID to look up motifs for
            provider_id (str): Optional specific provider to use (uses active if None)
        
        Returns:
            dict: Dictionary of loaded motifs: {motif_type: {details}}
        """
        try:
            self.loaded_motifs = {}
            pdb_id = pdb_id.upper()
            
            # Get provider
            if provider_id:
                provider = self._registry.get_provider(provider_id)
            else:
                provider = self._registry.get_active_provider()
            
            if not provider:
                self.logger.error("No database provider available")
                return {}
            
            # Get motifs for this PDB
            available_motifs = provider.get_motifs_for_pdb(pdb_id)
            
            if not available_motifs:
                self.logger.warning(f"No motifs found for PDB {pdb_id} in {provider.info.name}")
                return {}
            
            total_count = sum(len(instances) for instances in available_motifs.values())
            self.logger.info(f"Found {total_count} motifs in {pdb_id} ({provider.info.name})")
            
            # Process each motif type
            for motif_type, instances in available_motifs.items():
                try:
                    self._load_motif_type(structure_name, pdb_id, motif_type, instances)
                except Exception as e:
                    self.logger.error(f"Error loading {motif_type} motifs: {e}")
                    continue
            
            return self.loaded_motifs
            
        except Exception as e:
            self.logger.error(f"Failed to load motifs: {e}")
            return {}
    
    def _load_motif_type(self, structure_name: str, pdb_id: str,
                        motif_type: str, instances: List) -> None:
        """
        Load a specific motif type and create PyMOL objects.
        
        Args:
            structure_name: PyMOL structure name
            pdb_id: PDB ID
            motif_type: Type of motif (HL, IL, GNRA, etc.)
            instances: List of MotifInstance objects
        """
        if not instances:
            return
        
        # Build motif_list in format MotifSelector expects
        motif_list: List[Dict] = []
        motif_details = []
        
        for instance in instances:
            if not instance.residues:
                continue
            
            # Convert to legacy format for selector
            legacy_entries = instance.to_legacy_format()
            motif_list.extend(legacy_entries)
            
            motif_details.append({
                'motif_id': instance.motif_id,
                'instance_id': instance.instance_id,
                'residues': [r.to_tuple() for r in instance.residues],
                'annotation': instance.annotation,
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
            
            self.logger.success(f"Loaded {len(instances)} {motif_type_upper} motifs")
    
    def toggle_motif_type(self, motif_type: str, visible: bool) -> bool:
        """
        Toggle visibility of a motif type.
        
        Args:
            motif_type (str): Motif type (e.g., 'HL', 'IL', 'GNRA')
            visible (bool): True to show, False to hide
        
        Returns:
            bool: True if successful
        """
        motif_type = str(motif_type).upper().strip()
        motif_type = motif_type.replace('-', '_').replace(' ', '_')
        
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
    
    def reload_motifs(self, structure_name: str, pdb_id: str,
                     provider_id: Optional[str] = None) -> Dict:
        """
        Reload motifs (clear and reload).
        
        Args:
            structure_name (str): Name of structure in PyMOL
            pdb_id (str): PDB ID
            provider_id (str): Optional provider ID
        
        Returns:
            dict: Loaded motifs
        """
        self.clear_motifs()
        return self.load_motifs(structure_name, pdb_id, provider_id)
    
    def get_available_motif_types(self, pdb_id: str,
                                  provider_id: Optional[str] = None) -> List[str]:
        """Get list of motif types available for a PDB."""
        pdb_id = pdb_id.upper()
        
        if provider_id:
            provider = self._registry.get_provider(provider_id)
        else:
            provider = self._registry.get_active_provider()
        
        if not provider:
            return []
        
        motifs = provider.get_motifs_for_pdb(pdb_id)
        return sorted(list(motifs.keys()))
    
    def get_registry(self):
        """Get the database registry."""
        return self._registry


class VisualizationManager:
    """High-level manager for the entire visualization workflow."""
    
    def __init__(self, cmd, database_dir: str):
        """
        Initialize visualization manager.
        
        Args:
            cmd: PyMOL cmd module
            database_dir (str): Path to motif database directory
        """
        self.cmd = cmd
        self.database_dir = database_dir
        self.structure_loader = StructureLoader(cmd)
        self.motif_loader = UnifiedMotifLoader(cmd, database_dir)
        self.logger = get_logger()
        self._current_provider_id = None
    
    def setup_clean_visualization(self, structure_name: str,
                                 background_color: Optional[str] = None) -> None:
        """
        Set up clean RNA visualization with uniform color.
        
        Workflow:
        1. Hide everything
        2. Select all polymer.nucleic (all RNA chains)
        3. Show cartoon representation
        4. Set cartoon nucleic acid mode
        5. Color uniformly with background_color
        
        Args:
            structure_name (str): Name of structure in PyMOL
            background_color (str): Color for the RNA (default: 'gray80')
        """
        try:
            if background_color is None:
                background_color = colors.NON_MOTIF_COLOR or 'gray80'
            
            # Hide everything first
            self.cmd.hide('everything', 'all')
            self.logger.debug("Hidden all objects")
            
            # Select ALL polymer.nucleic
            rna_selection = f"{structure_name}_rna"
            self.cmd.select(rna_selection, f"{structure_name} and polymer.nucleic")
            
            # Show cartoon representation
            self.cmd.show('cartoon', rna_selection)
            
            # Set cartoon nucleic acid mode
            self.cmd.set('cartoon_nucleic_acid_mode', 1)
            
            # Color uniformly
            self.cmd.color(background_color, rna_selection)
            self.logger.info(f"Visualization: All RNA shown as {background_color} cartoon")
            
            # Clean up temporary selection
            self.cmd.delete(rna_selection)
            
        except Exception as e:
            self.logger.error(f"Failed to set up visualization: {e}")
    
    def load_and_visualize(self, pdb_id_or_path: str,
                          background_color: Optional[str] = None,
                          provider_id: Optional[str] = None) -> Dict:
        """
        Complete workflow: load structure and visualize all motifs.
        
        Args:
            pdb_id_or_path (str): PDB ID or file path
            background_color (str): Color for RNA backbone (default: 'gray80')
            provider_id (str): Optional database provider ID
        
        Returns:
            dict: Loaded motifs, or empty dict if failed
        """
        # Load structure
        structure_name = self.structure_loader.load_structure(pdb_id_or_path)
        if not structure_name:
            return {}
        
        pdb_id = self.structure_loader.get_current_pdb_id()
        
        # Set up clean visualization
        self.setup_clean_visualization(structure_name, background_color)
        
        # Load motifs from specified or active provider
        motifs = self.motif_loader.load_motifs(structure_name, pdb_id, provider_id)
        
        if provider_id:
            self._current_provider_id = provider_id
        
        return motifs
    
    def switch_database(self, provider_id: str) -> bool:
        """
        Switch to a different database provider.
        
        Args:
            provider_id: ID of the provider to switch to
            
        Returns:
            True if successful
        """
        registry = self.motif_loader.get_registry()
        if registry.set_active_provider(provider_id):
            self._current_provider_id = provider_id
            self.logger.info(f"Switched to database: {provider_id}")
            return True
        return False
    
    def reload_with_database(self, provider_id: str,
                            background_color: Optional[str] = None) -> Dict:
        """
        Reload current structure with a different database.
        
        Args:
            provider_id: Database provider to use
            background_color: Optional background color
            
        Returns:
            Loaded motifs
        """
        structure_name = self.structure_loader.get_current_structure()
        pdb_id = self.structure_loader.get_current_pdb_id()
        
        if not structure_name or not pdb_id:
            self.logger.error("No structure loaded")
            return {}
        
        # Clear existing motifs
        self.motif_loader.clear_motifs()
        
        # Set up visualization again
        self.setup_clean_visualization(structure_name, background_color)
        
        # Switch database and load
        self.switch_database(provider_id)
        return self.motif_loader.load_motifs(structure_name, pdb_id, provider_id)
    
    def get_structure_info(self) -> Dict:
        """Get current structure and motif info."""
        registry = self.motif_loader.get_registry()
        active_provider = registry.get_active_provider()
        
        return {
            'structure': self.structure_loader.get_current_structure(),
            'pdb_id': self.structure_loader.get_current_pdb_id(),
            'motifs': self.motif_loader.get_loaded_motifs(),
            'database': active_provider.info.name if active_provider else None,
            'database_id': self._current_provider_id,
        }
    
    def get_available_databases(self) -> List[Dict]:
        """Get list of available database providers."""
        registry = self.motif_loader.get_registry()
        return [
            {
                'id': pid,
                'name': provider.info.name,
                'description': provider.info.description,
                'motif_types': len(provider.get_available_motif_types()),
                'pdb_count': len(provider.get_available_pdb_ids()),
                'active': pid == self._current_provider_id,
            }
            for pid, provider in registry.get_all_providers().items()
        ]
    
    def get_available_motif_summary(self, pdb_id: str) -> str:
        """Get summary of available motifs for a PDB."""
        motif_types = self.motif_loader.get_available_motif_types(pdb_id)
        if not motif_types:
            return f"No motifs found for {pdb_id}"
        return f"Available motifs: {', '.join(motif_types)}"


# Backwards compatibility aliases
ScalableMotifLoader = UnifiedMotifLoader
