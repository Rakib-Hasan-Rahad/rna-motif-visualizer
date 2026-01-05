 # RNA Motif Visualizer (PyMOL Plugin)

 Visualize **RNA 3D Motif Atlas** motifs on structures loaded in PyMOL.

 This project is **Atlas-only** and **scalable**: it pre-indexes the bundled Atlas JSON datasets so it can quickly map:

 PDB ID → motif instances → residues

 It can load/fetch any structure by PDB ID (or local file), and it will overlay motifs **when that PDB is present in the Atlas dataset**.

 ## Motif classes (Atlas v4.5)

 - `HL` — hairpin loops
 - `IL` — internal loops
 - `J3`, `J4`, `J5`, `J6`, `J7` — junctions

 ## Install (PyMOL)

 Copy the plugin package folder into PyMOL’s startup directory.

 macOS / Linux:

 ```bash
 cp -r rna_motif_visualizer ~/.pymol/startup/
 ```

 Restart PyMOL.

 ## Usage (PyMOL console)

 Load a structure (PDB ID or local file):

 ```pml
 rna_load 4V9F
 rna_load ~/structures/my_rna.pdb
 rna_load 4V9F, bg_color=lightgray
 ```

 Toggle motif visibility:

 ```pml
 rna_toggle HL off
 rna_toggle IL on
 rna_toggle J3 on
 rna_toggle J7 off
 ```

 Show status:

 ```pml
 rna_status
 ```

 Change background color:

 ```pml
 rna_bg_color gray80
 rna_bg_color white
 ```

 ## Developer validation (no PyMOL needed)

 ```bash
 python3 test_atlas_validation.py
 ```

## Upgrading the Atlas database (low hassle)

- Drop the new Atlas JSON files into `rna_motif_visualizer/motif_database/` (e.g., `hl_4.6.json`, `il_4.6.json`, `j3_4.6.json`, …).
- The loader auto-selects the **latest** `<type>_<version>.json` per motif type.

Optional: pin to a specific Atlas version during validation or development:

```bash
RNA_MOTIF_ATLAS_VERSION=4.6 python3 test_atlas_validation.py
```

 ## Project layout

 - `rna_motif_visualizer/` – plugin package
 - `rna_motif_visualizer/motif_database/` – Atlas JSON + `motif_registry.json`
 - `rna_motif_visualizer/atlas_loader.py` – Atlas indexing + residue extraction
 - `rna_motif_visualizer/pdb_motif_mapper.py` – convenience wrapper for PDB → motifs
 - `test_atlas_validation.py` – CLI validation

 ## License

 MIT (see `LICENSE`).

