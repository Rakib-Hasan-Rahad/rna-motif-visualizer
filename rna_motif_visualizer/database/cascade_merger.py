"""
Cascade Merger - Priority-ordered motif merging with Jaccard deduplication

Merges motif datasets from multiple sources using a right-to-left cascade
strategy with strict priority ordering. The leftmost source in the
user's input is the highest priority.

Algorithm:
  Given ordered sources [Src1, Src2, Src3]:
    1. result = pairwise_merge(Src2, Src3)   # Src2 has priority
    2. final  = pairwise_merge(Src1, result)  # Src1 has priority
  
  In each pairwise merge:
    - For each motif in the lower-priority set (updater):
      - Check Jaccard overlap against ALL motifs in the higher-priority set (ref)
      - If Jaccard >= threshold with ANY ref motif: DISCARD updater motif
      - If Jaccard < threshold with ALL ref motifs: KEEP updater motif (unique)
    - Final = ref motifs + non-overlapping updater motifs

Uses Jaccard similarity: J(A,B) = |A intersect B| / |A union B|
Threshold: 0.60 by default

Author: CBB Lab
Version: 1.0.0
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Set, Tuple

from .base_provider import MotifInstance, ResidueSpec

logger = logging.getLogger(__name__)


def _get_residue_set(instance: MotifInstance) -> Set[Tuple[str, int]]:
    """
    Extract a set of (chain, residue_number) tuples from a MotifInstance.
    
    Using (chain, residue_number) pairs ensures chain-aware comparison.
    """
    return {(r.chain, r.residue_number) for r in instance.residues}


def _jaccard(set_a: Set, set_b: Set) -> float:
    """
    Calculate Jaccard similarity between two sets.
    
    J(A, B) = |A intersect B| / |A union B|
    """
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


class CascadeMerger:
    """
    Merges motif datasets from multiple sources using cascade strategy.
    
    Key principles:
    - Sources are priority-ordered (first = highest priority)
    - Merge proceeds right-to-left in cascade fashion
    - Overlapping motifs are resolved by keeping the higher-priority version
    - Non-overlapping motifs from lower-priority sources are added
    - Uses Jaccard similarity for overlap detection (across ALL motif types)
    """
    
    def __init__(self, jaccard_threshold: float = 0.60):
        """
        Initialize the CascadeMerger.
        
        Args:
            jaccard_threshold: Minimum Jaccard similarity to consider
                              two motifs as overlapping (default 0.60)
        """
        self.threshold = jaccard_threshold
    
    def merge_sources(
        self,
        ordered_sources: List[Dict[str, List[MotifInstance]]],
        source_labels: Optional[List[str]] = None,
    ) -> Dict[str, List[MotifInstance]]:
        """
        Merge multiple motif datasets using right-to-left cascade.
        
        Args:
            ordered_sources: List of motif dicts, ordered by priority
                            (index 0 = highest priority).
                            Each dict maps motif_type -> [MotifInstance, ...]
            source_labels: Optional labels for logging (e.g., ['Source 1', 'Source 3'])
        
        Returns:
            Merged motif dict: motif_type -> [MotifInstance, ...]
        """
        if not ordered_sources:
            return {}
        
        if len(ordered_sources) == 1:
            return ordered_sources[0]
        
        labels = source_labels or [f"Source_{i}" for i in range(len(ordered_sources))]
        
        logger.info(f"[CASCADE] Merging {len(ordered_sources)} sources: {labels}")
        
        # Right-to-left cascade: merge from the end
        # Start with the last (lowest priority) source
        result = ordered_sources[-1]
        logger.info(
            f"[CASCADE] Starting with {labels[-1]}: "
            f"{self._count_motifs(result)} motifs in {len(result)} categories"
        )
        
        # Merge each source from right to left (second-to-last back to first)
        for i in range(len(ordered_sources) - 2, -1, -1):
            ref = ordered_sources[i]
            updater = result
            
            ref_label = labels[i]
            updater_label = f"intermediate" if i < len(ordered_sources) - 2 else labels[i + 1]
            
            result = self._pairwise_merge(ref, updater, ref_label, updater_label)
            
            logger.info(
                f"[CASCADE] After merging {ref_label} (priority) + {updater_label}: "
                f"{self._count_motifs(result)} motifs in {len(result)} categories"
            )
        
        logger.info(
            f"[CASCADE] Final result: "
            f"{self._count_motifs(result)} motifs in {len(result)} categories"
        )
        
        return result
    
    def _pairwise_merge(
        self,
        ref: Dict[str, List[MotifInstance]],
        updater: Dict[str, List[MotifInstance]],
        ref_label: str = "ref",
        updater_label: str = "updater",
    ) -> Dict[str, List[MotifInstance]]:
        """
        Merge two motif datasets with ref having priority over updater.
        
        For each updater motif:
          - If it overlaps (Jaccard >= threshold) with ANY ref motif: DISCARD
          - Otherwise: KEEP (it's a unique motif not in ref)
        
        Args:
            ref: Higher-priority motif dataset
            updater: Lower-priority motif dataset
            ref_label: Label for logging
            updater_label: Label for logging
            
        Returns:
            Merged motif dict (ref motifs + non-overlapping updater motifs)
        """
        # Start with all ref motifs (normalize keys to uppercase)
        merged: Dict[str, List[MotifInstance]] = {}
        for mtype, instances in ref.items():
            norm_key = mtype.upper()
            if norm_key in merged:
                merged[norm_key].extend(instances)
            else:
                merged[norm_key] = list(instances)
        
        # Pre-compute ref residue sets for efficiency
        ref_residue_sets: List[Tuple[str, MotifInstance, Set]] = []
        for mtype, instances in ref.items():
            for inst in instances:
                rset = _get_residue_set(inst)
                if rset:
                    ref_residue_sets.append((mtype.upper(), inst, rset))
        
        # Check each updater motif against all ref motifs
        stats = {'kept': 0, 'discarded': 0}
        
        for u_type, u_instances in updater.items():
            u_type_norm = u_type.upper()
            for u_inst in u_instances:
                u_rset = _get_residue_set(u_inst)
                if not u_rset:
                    # No residues - keep it anyway
                    merged.setdefault(u_type_norm, []).append(u_inst)
                    stats['kept'] += 1
                    continue
                
                # Check overlap against ALL ref motifs (cross-type)
                is_overlap = False
                best_j = 0.0
                best_ref_type = None
                
                for r_type, r_inst, r_rset in ref_residue_sets:
                    j = _jaccard(u_rset, r_rset)
                    if j >= self.threshold:
                        is_overlap = True
                        if j > best_j:
                            best_j = j
                            best_ref_type = r_type
                        break  # Found overlap, no need to check more
                
                if is_overlap:
                    stats['discarded'] += 1
                    logger.debug(
                        f"[CASCADE] Discarded {updater_label} motif "
                        f"'{u_type_norm}/{u_inst.instance_id}' - overlaps with "
                        f"{ref_label} '{best_ref_type}' (Jaccard={best_j:.3f})"
                    )
                else:
                    # Unique motif from updater - add to merged
                    merged.setdefault(u_type_norm, []).append(u_inst)
                    stats['kept'] += 1
        
        logger.info(
            f"[CASCADE] Pairwise merge {ref_label} + {updater_label}: "
            f"kept {stats['kept']} from {updater_label}, "
            f"discarded {stats['discarded']} overlapping"
        )
        
        return merged
    
    def _count_motifs(self, motifs: Dict[str, List[MotifInstance]]) -> int:
        """Count total motif instances across all types."""
        return sum(len(instances) for instances in motifs.values())
