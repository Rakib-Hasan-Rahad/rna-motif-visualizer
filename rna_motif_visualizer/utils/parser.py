"""
RNA Motif Visualizer - Parser Module
Handles parsing of PDB/mmCIF files and motif database JSON files.
"""

import json
import os
from pathlib import Path


class MotifDatabaseParser:
    """Parser for motif database JSON files."""
    
    def __init__(self, database_dir):
        """
        Initialize parser.
        
        Args:
            database_dir (str): Path to motif database directory
        """
        self.database_dir = Path(database_dir)
    
    def load_motif_file(self, motif_type):
        """
        Load motif annotations from JSON file.
        
        Args:
            motif_type (str): Motif type (e.g., 'kturn', 'aminor')
        
        Returns:
            dict: Motif data keyed by PDB ID, or None if file not found
        """
        filepath = self.database_dir / f"{motif_type}.json"
        
        if not filepath.exists():
            return None
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return data
        except json.JSONDecodeError as e:
            print(f"Error parsing {filepath}: {e}")
            return None
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None
    
    def get_motifs_for_pdb(self, pdb_id, motif_type):
        """
        Get all motif instances for a specific PDB ID and motif type.
        
        Supports both specific PDB IDs and generic 'RNA_STRUCTURE' key.
        
        Args:
            pdb_id (str): PDB ID (e.g., '1S72')
            motif_type (str): Motif type (e.g., 'kink_turn')
        
        Returns:
            list: List of motif dictionaries for this PDB, or empty list if none found
        """
        data = self.load_motif_file(motif_type)
        if data is None:
            return []
        
        pdb_key = pdb_id.upper()
        
        # Try specific PDB ID first, then fall back to generic RNA_STRUCTURE key
        motifs = data.get(pdb_key, [])
        if motifs:
            return motifs
        
        # Fall back to generic RNA_STRUCTURE key for universal motif data
        return data.get('RNA_STRUCTURE', [])
    
    def list_available_motif_types(self):
        """
        List all available motif types in the database.
        
        Returns:
            list: List of motif type names (without .json extension)
        """
        if not self.database_dir.exists():
            return []
        
        motif_types = []
        for f in self.database_dir.glob('*.json'):
            motif_types.append(f.stem)
        
        return sorted(motif_types)


class PDBParser:
    """Simple parser for PDB metadata (minimal - mostly handled by PyMOL)."""
    
    @staticmethod
    def extract_pdb_id(filepath_or_id):
        """
        Extract PDB ID from file path or return if already a PDB ID.
        
        Args:
            filepath_or_id (str): Either a PDB ID or file path
        
        Returns:
            str: PDB ID (4 characters) or None if invalid
        """
        # Check if it's already a PDB ID (4 characters, alphanumeric)
        if len(filepath_or_id) == 4 and filepath_or_id.isalnum():
            return filepath_or_id.upper()
        
        # Try to extract from filename
        filename = os.path.basename(filepath_or_id)
        # PDB files often named like "1s72.pdb" or "1S72.cif"
        if filename:
            name_without_ext = os.path.splitext(filename)[0]
            if len(name_without_ext) >= 4:
                potential_id = name_without_ext[:4]
                if potential_id.isalnum():
                    return potential_id.upper()
        
        return None
    
    @staticmethod
    def is_valid_pdb_id(pdb_id):
        """
        Check if a string is a valid PDB ID.
        
        Args:
            pdb_id (str): Potential PDB ID
        
        Returns:
            bool: True if valid format
        """
        if not isinstance(pdb_id, str):
            return False
        return len(pdb_id) == 4 and pdb_id.isalnum()


class SelectionParser:
    """Parser for creating PyMOL selection strings from residue data."""
    
    @staticmethod
    def create_selection_string(chain, residues):
        """
        Create a PyMOL selection string from chain and residue numbers.
        
        Args:
            chain (str): Chain identifier
            residues (list): List of residue numbers
        
        Returns:
            str: PyMOL selection string (e.g., "chain A and resi 77-82")
        """
        if not residues:
            return None
        
        residues = sorted(residues)
        selection = f"chain {chain} and resi {residues[0]}-{residues[-1]}"
        return selection
    
    @staticmethod
    def create_detailed_selection(chain, residues):
        """
        Create a detailed PyMOL selection string listing all residues.
        
        Args:
            chain (str): Chain identifier
            residues (list): List of residue numbers
        
        Returns:
            str: Detailed PyMOL selection string
        """
        if not residues:
            return None
        
        residue_list = "+".join([f"resi {r}" for r in sorted(residues)])
        selection = f"chain {chain} and ({residue_list})"
        return selection


def validate_motif_data(motif_entry):
    """
    Validate a motif entry has required fields.
    
    Args:
        motif_entry (dict): Motif dictionary to validate
    
    Returns:
        bool: True if valid
    """
    required_fields = ['chain', 'residues', 'motif_id']
    return all(field in motif_entry for field in required_fields) and \
           isinstance(motif_entry.get('residues'), list) and \
           len(motif_entry.get('residues', [])) > 0
