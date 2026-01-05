"""rna_motif_visualizer.atlas_loader

Loads RNA 3D Motif Atlas JSON files (and indexes by PDB ID) for scalable lookup.

Atlas JSON structure (simplified):
- List[dict] of motifs
- Each motif has an "alignment" dict
- alignment maps instance_id -> { position_index: "PDB|Model|Chain|Nuc|ResNum", ... }

This module builds an in-memory index:
  PDB_ID -> List[{motif_type, motif_id, instance_id, ...}]
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


ResidueSpec = Tuple[str, int, str]  # (nucleotide, residue_number, chain)


class AtlasMotifLoader:
    """Loader + indexer for RNA 3D Motif Atlas JSON files."""

    def __init__(self, motif_db_path: str):
        self.db_path = Path(motif_db_path)
        self.registry_file = self.db_path / "motif_registry.json"
        self.registry: Dict[str, Any] = self._load_registry()

        self.pdb_index: Dict[str, List[Dict[str, Any]]] = {}

    def _load_registry(self) -> Dict[str, Any]:
        try:
            with open(self.registry_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def build_pdb_index(self) -> None:
        """Scan all registry files and build PDB->motifs index."""
        self.pdb_index.clear()

        all_files: Dict[str, Dict[str, Any]] = {}
        all_files.update(self.registry.get("motif_files", {}) or {})

        for motif_type, cfg in all_files.items():
            file_name = cfg.get("file")
            if not file_name:
                continue

            file_path = self.db_path / file_name
            if not file_path.exists():
                continue

            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
            except Exception:
                continue

            self._index_motif_file_data(data, motif_type)

    def _index_motif_file_data(self, data: Any, motif_type: str) -> None:
        """Index one Atlas motif JSON file."""
        if not isinstance(data, list):
            return

        motifs: Iterable[Any] = data

        for motif_entry in motifs:
            if not isinstance(motif_entry, dict):
                continue

            alignment = motif_entry.get("alignment")
            if not isinstance(alignment, dict):
                # Not an Atlas motif entry; skip.
                continue

            for instance_id in alignment.keys():
                pdb_id = self._extract_pdb_id(str(instance_id))
                if not pdb_id:
                    continue

                self.pdb_index.setdefault(pdb_id, []).append(
                    {
                        "motif_id": motif_entry.get("motif_id", "unknown"),
                        "motif_type": motif_type,
                        "instance_id": instance_id,
                        "num_instances": motif_entry.get("num_instances"),
                        "num_nucleotides": motif_entry.get("num_nucleotides"),
                    }
                )

    @staticmethod
    def _extract_pdb_id(instance_id: str) -> Optional[str]:
        # Case 1: residue spec style in key (rare)
        if "|" in instance_id:
            head = instance_id.split("|", 1)[0]
            return head.upper() if len(head) == 4 else None

        # Case 2: typical Atlas instance_id like HL_6SVS_002 (PDB IDs are 4-char and can start with a digit)
        parts = instance_id.split("_")
        for part in parts:
            if len(part) == 4 and part.isalnum():
                return part.upper()
        return None

    def get_available_pdb_structures(self) -> List[str]:
        return sorted(self.pdb_index.keys())

    def get_motifs_for_pdb(self, pdb_id: str) -> List[Dict[str, Any]]:
        return self.pdb_index.get(pdb_id.upper(), [])

    def load_motif_residues(self, pdb_id: str, motif_type: str, instance_id: str) -> List[ResidueSpec]:
        """Load residue specs for a single motif instance."""
        pdb_id = pdb_id.upper()

        all_files: Dict[str, Dict[str, Any]] = {}
        all_files.update(self.registry.get("motif_files", {}) or {})
        cfg = all_files.get(motif_type)
        if not cfg:
            return []

        file_name = cfg.get("file")
        if not file_name:
            return []

        file_path = self.db_path / file_name
        if not file_path.exists():
            return []

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except Exception:
            return []

        if not isinstance(data, list):
            return []

        for motif_entry in data:
            if not isinstance(motif_entry, dict):
                continue

            alignment = motif_entry.get("alignment")
            if not isinstance(alignment, dict):
                continue

            residues = alignment.get(instance_id)
            if isinstance(residues, dict):
                parsed = self._parse_alignment_residues(residues)
                # Note: residue specs in Atlas entries are already for this instance_id.
                return parsed

        return []

    @staticmethod
    def _parse_alignment_residues(residues: Dict[str, str]) -> List[ResidueSpec]:
        result: List[ResidueSpec] = []
        # Sort by numeric position when possible
        for _, spec in sorted(residues.items(), key=lambda kv: int(kv[0]) if str(kv[0]).isdigit() else 10**9):
            parts = str(spec).split("|")
            if len(parts) < 5:
                continue
            chain = parts[2]
            nuc = parts[3]
            try:
                res_num = int(parts[4])
            except ValueError:
                continue
            result.append((nuc, res_num, chain))
        return result


_loader_instance: Optional[AtlasMotifLoader] = None


def get_atlas_loader(motif_db_path: Optional[str] = None) -> AtlasMotifLoader:
    global _loader_instance
    if _loader_instance is None:
        if motif_db_path is None:
            motif_db_path = str(Path(__file__).parent / "motif_database")
        _loader_instance = AtlasMotifLoader(motif_db_path)
        _loader_instance.build_pdb_index()
    return _loader_instance
