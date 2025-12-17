# RNA Motif Visualizer - Data Pipeline Flowchart

## Complete Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DATA PIPELINE OVERVIEW                             │
└─────────────────────────────────────────────────────────────────────────────┘

1. SOURCE DATA LAYER
════════════════════════════════════════════════════════════════════════════════

    ┌──────────────────────────────┐
    │   motifs.csv (Master Data)   │
    │  ├─ PDB ID                   │
    │  ├─ Motif Type               │
    │  ├─ Chain ID                 │
    │  ├─ Residue Numbers          │
    │  └─ Partner Residues         │
    └──────────────────────────────┘
            │
            │ (36 motif instances)
            ▼
    ┌──────────────────────────────┐
    │  generate_motif_jsons.py     │
    │  (Conversion Script)         │
    │  ├─ Parse CSV rows           │
    │  ├─ Group by motif type      │
    │  └─ Generate JSON structure  │
    └──────────────────────────────┘


2. DATABASE STORAGE LAYER
════════════════════════════════════════════════════════════════════════════════

    Generated JSON Files (motif_database/):
    
    ├─ kink_turn.json (7 instances)
    │  └─ Structure: {
    │     "RNA_STRUCTURE": [
    │       {"pdb": "1S72", "chain": "0", "residues": [1437, ...], "partners": [...]},
    │       {...}
    │     ]
    │  }
    │
    ├─ c_loop.json (4 instances)
    │
    ├─ sarcin_ricin.json (13 instances)
    │
    ├─ reverse_kink_turn.json (2 instances)
    │
    └─ e_loop.json (10 instances)


3. USER INTERFACE LAYER
════════════════════════════════════════════════════════════════════════════════

    User in PyMOL Console:
    
    pymol> rna_load 1S72
            │
            ▼
    ┌──────────────────────────────┐
    │      gui.py                  │
    │  (load_structure_action)     │
    │  ├─ Receives: PDB ID         │
    │  └─ Calls: loader.load()     │
    └──────────────────────────────┘


4. MAIN LOADING PIPELINE
════════════════════════════════════════════════════════════════════════════════

    ┌─────────────────────────────────────────┐
    │         loader.py (Main Handler)        │
    └─────────────────────────────────────────┘
            │
            ├──► Step 1: setup_clean_visualization(pdb_id)
            │    ├─ Hide all objects
            │    ├─ Select all polymer.nucleic in structure
            │    ├─ Show cartoon representation
            │    ├─ Set cartoon_nucleic_acid_mode = 1
            │    └─ Color RNA gray80 (background)
            │
            └──► Step 2: load_motifs(pdb_id)
                 │
                 ▼
         ┌──────────────────────────┐
         │   parser.py              │
         │ (get_motifs_for_pdb)     │
         └──────────────────────────┘
                 │
                 ├─ Input: pdb_id (e.g., "1S72")
                 │
                 ▼
         ┌──────────────────────────────────┐
         │  Try Primary Lookup              │
         │  Look for specific PDB ID key    │
         │  in JSON file                    │
         │                                  │
         │  Example: {"1S72": [...]}        │
         └──────────────────────────────────┘
                 │
              Match?
                 │
          ┌──No──┴──Yes──┐
          │              │
          ▼              └─► Return motif data for PDB
      ┌─────────────────────────────┐
      │ Fallback Lookup             │
      │ Use generic "RNA_STRUCTURE" │
      │ key (universal access)      │
      │                             │
      │ {"RNA_STRUCTURE": [...]}    │
      └─────────────────────────────┘
              │
              └─► Return motif data


5. DATA ENRICHMENT & PROCESSING LAYER
════════════════════════════════════════════════════════════════════════════════

    Motif Data Retrieved:
    ┌────────────────────────────────────────┐
    │ For each motif instance:               │
    │ ├─ PDB ID: "1S72"                      │
    │ ├─ Motif Type: "KINK_TURN"             │
    │ ├─ Chain ID: "0"                       │
    │ ├─ Residues: [1437, 1438, 1439, ...]   │
    │ └─ Partners: [1437, 1438, ...]         │
    └────────────────────────────────────────┘
            │
            ▼
    ┌──────────────────────────────────────┐
    │  colors.py                           │
    │  (Color Lookup)                      │
    │  MOTIF_COLORS["KINK_TURN"]           │
    │  └─ Returns: (1.0, 0.0, 0.0) [Red]   │
    └──────────────────────────────────────┘
            │
            ▼
    ┌──────────────────────────────────────┐
    │  Format & Structure Data             │
    │  ├─ _format_residues()               │
    │  │  └─ Convert [1437,1438,1439,     │
    │  │     1440,1508] to                 │
    │  │     "1437-1440, 1508"             │
    │  │     (ranges + non-consecutive)    │
    │  │                                   │
    │  └─ Build motif display object:      │
    │     {                                │
    │       "id": "Kink-turn1",            │
    │       "chain": "0",                  │
    │       "residues": "1437-1440, 1508", │
    │       "partners": "1437-1440, 1508", │
    │       "color": (1.0, 0.0, 0.0)       │
    │     }                                │
    └──────────────────────────────────────┘


6. PYMOL OBJECT CREATION LAYER
════════════════════════════════════════════════════════════════════════════════

    ┌──────────────────────────────────────────┐
    │  selectors.py                            │
    │  (PyMOL Selection & Object Creation)     │
    └──────────────────────────────────────────┘
            │
            ▼
    For Each Motif:
    
    Input: {residues: [1437-1440, 1508], chain: "0", ...}
            │
            ├─ Create PyMOL Selection String:
            │  "motif_name and chain 0 and resi 1437-1440+1508"
            │
            ├─ Create Named Selection:
            │  cmd.select("Kink-turn1_sel", selection_string)
            │
            ├─ Show as Sticks:
            │  cmd.show("sticks", "Kink-turn1_sel")
            │
            └─ Apply Color:
               cmd.color((1.0, 0.0, 0.0), "Kink-turn1_sel")
               └─ Result: Red sticks for Kink-turn1


7. CONSOLE OUTPUT & LOGGING LAYER
════════════════════════════════════════════════════════════════════════════════

    ┌──────────────────────────────────┐
    │  logger.py                       │
    │  (Detailed Console Feedback)     │
    └──────────────────────────────────┘
            │
            ▼
    PyMOL Console Output:
    
    ════════════════════════════════════════
     Motif Information - 1S72
    ════════════════════════════════════════
    
    Total Motifs Found: 7
    
    [1] ID: Kink-turn1
        Chain: 0
        Residues: 1437-1440, 1508
        Partners: 1437-1440, 1508
    
    [2] ID: Kink-turn2
        Chain: 0
        Residues: 2004-2007, 2014
        Partners: 2004-2007, 2014
    
    ... (remaining motifs)


8. FINAL VISUALIZATION OUTPUT
════════════════════════════════════════════════════════════════════════════════

    PyMOL Window:
    
    ┌──────────────────────────────────────────┐
    │                                          │
    │   ≈≈≈ Gray80 RNA Cartoon ≈≈≈             │
    │      (Background Structure)              │
    │                                          │
    │   • Red sticks: Kink-turn motifs         │
    │   • Yellow sticks: C-loop motifs         │
    │   • Green sticks: Sarcin-ricin motifs    │
    │   • Cyan sticks: Reverse-kink-turn       │
    │   • Magenta sticks: E-loop motifs        │
    │                                          │
    └──────────────────────────────────────────┘


════════════════════════════════════════════════════════════════════════════════
COMPLETE DATA FLOW SUMMARY
════════════════════════════════════════════════════════════════════════════════

Source: motifs.csv (36 motifs)
    ↓
Processing: generate_motif_jsons.py
    ↓
Storage: 5 JSON files (motif_database/)
    ↓
User Input: PyMOL command "rna_load 1S72"
    ↓
Interface: gui.py
    ↓
Loading: loader.py + parser.py (lookup motifs)
    ↓
Enrichment: colors.py (map colors) + residue formatting
    ↓
Creation: selectors.py (create PyMOL objects)
    ↓
Output: Colored motif sticks + Console logging (logger.py)
    ↓
Display: PyMOL 3D Visualization


════════════════════════════════════════════════════════════════════════════════
KEY DATA TRANSFORMATIONS
════════════════════════════════════════════════════════════════════════════════

1. CSV Row → JSON Entry
   "1S72,KINK_TURN,0,1437;1438;1439;1440;1508,..." 
   →
   {"pdb": "1S72", "chain": "0", "residues": [...], "partners": [...]}

2. JSON Data → Formatted String
   [1437, 1438, 1439, 1440, 1508]
   →
   "1437-1440, 1508"

3. Residue Data → PyMOL Selection
   "1437-1440, 1508"
   →
   "resi 1437-1440+1508"

4. Selection + Color → PyMOL Object
   {"residues": "1437-1440, 1508", "color": (1.0, 0.0, 0.0)}
   →
   Red sticks showing Kink-turn1 motif


════════════════════════════════════════════════════════════════════════════════
DATA FLOW - TIMELINE EXAMPLE (Loading 1S72)
════════════════════════════════════════════════════════════════════════════════

T0: User types: pymol> rna_load 1S72

T1: gui.py receives command → calls loader.load("1S72")

T2: loader.setup_clean_visualization("1S72")
    └─ PyMOL actions: hide all → show RNA cartoon → color gray80

T3: loader.load_motifs("1S72")
    └─ Calls parser.get_motifs_for_pdb("1S72")

T4: parser.py opens kink_turn.json → finds "1S72" key → returns 2 motifs
    └─ Data: [Kink-turn1, Kink-turn2]

T5: parser.py opens c_loop.json → finds "RNA_STRUCTURE" → returns 1 motif
    └─ Data: [C-loop1]

T6-T10: Repeat for remaining JSON files (sarcin_ricin, reverse_kink_turn, e_loop)
    └─ Total: 7 motifs collected

T11: For each motif:
    ├─ Get color from colors.py
    ├─ Format residues with _format_residues()
    ├─ Create PyMOL selection with selectors.py
    └─ Apply color

T12: Log summary to console with logger.py
    └─ Output: "Total Motifs Found: 7" + detailed [1], [2], ... list

T13: All motifs visible in PyMOL window with distinct colors
    └─ Pipeline complete


════════════════════════════════════════════════════════════════════════════════
FILES INVOLVED IN DATA PIPELINE
════════════════════════════════════════════════════════════════════════════════

INPUT FILES:
├─ motifs.csv (source data)
└─ motif_database/ (5 JSON files)
   ├─ kink_turn.json
   ├─ c_loop.json
   ├─ sarcin_ricin.json
   ├─ reverse_kink_turn.json
   └─ e_loop.json

PROCESSING FILES:
├─ gui.py (command interface)
├─ loader.py (main orchestrator)
├─ parser.py (JSON reading + fallback logic)
├─ selectors.py (PyMOL object creation)
├─ colors.py (color mapping)
└─ utils/logger.py (console output)

OUTPUT:
└─ PyMOL 3D visualization + Console logs
```

## Data Structure Details

### CSV Format (motifs.csv)
```
pdb_id,motif_type,chain_id,residues,partner_residues
1S72,KINK_TURN,0,1437;1438;1439;1440;1508,1437;1438;1439;1440;1508
2GDI,C_LOOP,A,1424;1436;1437;1438;1439;1440,1424;1425;1426;1427;1428;1429;1430
```

### JSON Storage Format
```json
{
  "RNA_STRUCTURE": [
    {
      "pdb": "1S72",
      "chain": "0",
      "residues": [1437, 1438, 1439, 1440, 1508],
      "partners": [1437, 1438, 1439, 1440, 1508]
    },
    {
      "pdb": "1S72",
      "chain": "0",
      "residues": [2004, 2005, 2006, 2007, 2014],
      "partners": [2004, 2005, 2006, 2007, 2014]
    }
  ]
}
```

### Internal Data Object
```python
{
    "id": "Kink-turn1",
    "motif_type": "KINK_TURN",
    "chain": "0",
    "residues": [1437, 1438, 1439, 1440, 1508],
    "residues_formatted": "1437-1440, 1508",
    "partners": [1437, 1438, 1439, 1440, 1508],
    "partners_formatted": "1437-1440, 1508",
    "color": (1.0, 0.0, 0.0),  # RGB for red
    "pymol_selection": "Kink-turn1 and chain 0 and resi 1437-1440+1508"
}
```

## Residue Formatting Logic

The `_format_residues()` function converts residue arrays into human-readable ranges:

**Input:** `[1437, 1438, 1439, 1440, 1508]`

**Processing:**
- Detect consecutive sequences: `[1437, 1438, 1439, 1440]` and `[1508]`
- Format consecutive: `1437-1440`
- Keep isolated: `1508`
- Join with commas: `1437-1440, 1508`

**Output:** `"1437-1440, 1508"`

**Purpose:** Shows motif structure - gaps in numbering indicate multi-part motifs (e.g., two loops connected by a stem)

---

This flowchart shows the complete journey of data from the CSV source through to final PyMOL visualization!
