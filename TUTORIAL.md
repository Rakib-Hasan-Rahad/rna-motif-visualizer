# RNA Motif Visualizer — Tutorial

A complete step-by-step guide for using the RNA Motif Visualizer PyMOL plugin (v2.3.0).

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Basic Workflow](#2-basic-workflow)
3. [Exploring Motifs](#3-exploring-motifs)
4. [Viewing Instances](#4-viewing-instances)
5. [Working with Data Sources](#5-working-with-data-sources)
6. [Multi-Source Comparison](#6-multi-source-comparison)
7. [User Annotations (FR3D / RMS / RMSX)](#7-user-annotations-fr3d--rms--rmsx)
8. [Customizing Colors](#8-customizing-colors)
9. [Saving Images](#9-saving-images)
10. [Label Chain IDs (Advanced)](#10-label-chain-ids-advanced)
11. [Tips and Tricks](#11-tips-and-tricks)

---

## 1. Getting Started

### Prerequisites

- **PyMOL** (Incentive or Open-Source, version 2.x or later)
- **Python 3.8+** (bundled with PyMOL)
- Internet connection (for BGSU API and Rfam API sources only)

### Installation

1. Open PyMOL
2. Go to **Plugin → Plugin Manager → Install New Plugin → Install from local file**
3. Select the `rna_motif_visualizer` folder (or the ZIP archive)
4. Restart PyMOL

After launching PyMOL, you should see:

```
================================================================================
                    🧬 RNA MOTIF VISUALIZER 🧬

 Version 2.3.0
 Last Updated: 20 February 2026
================================================================================
```

Run `rmv_help` at any time to see all available commands.

---

## 2. Basic Workflow

The plugin uses a **3-step workflow**: **Load → Source → Motifs**.

### Step 1 — Load a PDB Structure

```
rmv_fetch 1S72
```

This downloads the structure from RCSB PDB and loads it into PyMOL:

```
[SUCCESS] Loaded structure 1S72 as '1s72'
[INFO] Chain ID mode: auth_asym_id (default)
[INFO] Chains found: 0, 9, A, B, C, D, ...
```

> **Note:** Only the structure is loaded at this point — no motif data yet. This makes loading fast and lets you pick a data source first.

### Step 2 — Select a Data Source

```
rmv_source 3
```

This selects BGSU RNA 3D Hub API — the most comprehensive source with 3000+ structures. Available sources:

| ID | Source | Type | Coverage |
|----|--------|------|----------|
| 1 | RNA 3D Atlas | Local (offline) | 759 PDBs |
| 2 | Rfam | Local (offline) | 173 PDBs |
| 3 | **BGSU RNA 3D Hub** | Online API | **~3000+ PDBs** |
| 4 | Rfam API | Online API | All Rfam families |
| 5 | FR3D | User annotations | Custom |
| 6 | RNAMotifScan | User annotations | Custom |
| 7 | RNAMotifScanX | User annotations | Custom |

Run `rmv_sources` to see detailed information about each source.

### Step 3 — Fetch Motif Data

```
rmv_motifs
```

This retrieves motif data from the selected source for your loaded PDB:

```
[SUCCESS] Found 223 motifs in 1S72 (source: bgsu_api)
[SUCCESS] Loaded 35 HAIRPIN LOOP (HL) motifs
[SUCCESS] Loaded 23 GNRA motifs
[SUCCESS] Loaded 8 SARCIN-RICIN motifs
...
[SUCCESS] Loaded 41 motif types from 1S72
```

### Step 4 — View the Summary

```
rmv_summary
```

Displays a table of all detected motif types and instance counts:

```
==================================================
  MOTIF SUMMARY - 1S72
==================================================
  MOTIF TYPE              INSTANCES
--------------------------------------------------
  HAIRPIN LOOP (HL)              35
  GNRA                           23
  INTERNAL LOOP (IL)             19
  3-WAY JUNCTION (J3)            18
  ...
--------------------------------------------------
  TOTAL                         223
==================================================
```

### Step 5 — Visualize Motifs

```
rmv_show HL
```

This creates PyMOL objects, colors the hairpin loop residues, and displays them on the gray structure background.

### The Complete Pipeline (5 Lines)

```
rmv_fetch 1S72       # Load PDB
rmv_source 3         # Select BGSU
rmv_motifs           # Fetch data
rmv_summary          # View summary
rmv_show HL          # Render hairpin loops
```

---

## 3. Exploring Motifs

### View All Motif Types

```
rmv_summary
```

Prints a count of each motif type found in the loaded PDB.

### View Instances of a Specific Motif Type

```
rmv_summary SARCIN-RICIN
```

Shows a detailed table of all instances of that motif type:

```
====================================================================
  SARCIN-RICIN MOTIF INSTANCES
====================================================================
  NO.    CHAIN      RESIDUE RANGES           NUCLEOTIDES
--------------------------------------------------------------------
  1      A          A:158-164, A:171-178     AGAACUGCUCAGUAU
  2      A          A:210-216, A:224-229     UUAGUAAUGAACG
  3      A          A:290-296, A:355-362     CCGACCGCCAGUACG
  ...
--------------------------------------------------------------------
```

### View a Single Instance in Detail

```
rmv_summary SARCIN-RICIN 1
```

Prints full residue-level details for instance #1 (per-residue chain, index, nucleotide).

### Render a Motif Type on Structure

```
rmv_show HL           # Show all hairpin loops
rmv_show GNRA         # Show all GNRA tetraloops
rmv_show SARCIN-RICIN # Show all sarcin-ricin motifs
```

### Render a Specific Instance

```
rmv_show GNRA 1       # Show and color only instance 1 of GNRA
```

### Reset View

```
rmv_all               # Reset view: show all motifs on gray structure
```

---

## 4. Viewing Instances

### Zoom Into a Single Instance

```
rmv_show GNRA 1
```

This will:
- Create an individual PyMOL object for the instance
- Zoom the camera to that instance
- Print residue-level details (chain, residue numbers, nucleotides)

### Navigate Between Instances

```
rmv_show GNRA 1    # View instance 1
rmv_show GNRA 2    # View instance 2
rmv_show GNRA 3    # View instance 3
rmv_all                # Back to full view
```

### Toggle Motif Visibility

```
rmv_toggle HL off      # Hide hairpin loops
rmv_toggle HL on       # Show them again
```

---

## 5. Working with Data Sources

### Local Sources (Offline — No Internet Needed)

Sources 1 and 2 are bundled with the plugin:

```
rmv_source 1           # RNA 3D Atlas — 759 PDBs, motif types: HL, IL, J3-J7
rmv_motifs

rmv_source 2           # Rfam — 173 PDBs, motif types: GNRA, UNCG, K-turn, T-loop, C-loop, etc.
rmv_motifs
```

### Online Sources (API — Internet Required)

Sources 3 and 4 query online databases:

```
rmv_source 3           # BGSU RNA 3D Hub — ~3000+ PDBs (most comprehensive source)
rmv_motifs

rmv_source 4           # Rfam API — all Rfam-annotated motif families
rmv_motifs
```

> **Caching:** API results are cached for 30 days in `~/.rna_motif_visualizer_cache/`. Use `rmv_refresh` to bypass the cache and force a fresh fetch.

### Switch Sources Without Reloading PDB

One of the most powerful features — the PDB structure stays loaded while you switch sources:

```
rmv_fetch 1S72         # Load once
rmv_source 3           # BGSU
rmv_motifs             # Fetch from BGSU → 41 motif types

rmv_source 1           # Switch to Atlas
rmv_motifs             # Fetch from Atlas → 7 motif types (no PDB re-download)

rmv_source 2           # Switch to Rfam
rmv_motifs             # Fetch from Rfam
```

### Check Source Information

```
rmv_sources            # List all 7 sources, their types, and coverage
rmv_source info 3      # Detailed information about BGSU source
rmv_status             # Current plugin status: loaded PDB, active source, motif counts
```

---

## 6. Multi-Source Comparison

Combine data from multiple sources. The plugin merges results with smart deduplication.

### Basic Two-Source Combine

```
rmv_fetch 1S72
rmv_source 1 3         # Combine Atlas [1] + BGSU [3]
rmv_motifs             # Fetches from both → deduplicates → merged
rmv_summary            # Unified summary from both sources
```

### Three-Source Combine

```
rmv_source 1 3 4       # Atlas + BGSU + Rfam API
rmv_motifs
rmv_summary
```

### How Merging Works

1. **Fetch** — motifs are fetched from each source independently
2. **Enrich** — generic names (e.g., "HL") get enriched to specific names (e.g., "GNRA") using NR homolog representative lookup
3. **Cascade Merge** — right-to-left merging with Jaccard deduplication (≥60% residue overlap = duplicate, kept once)

### Source-Tagged PyMOL Objects

When you switch sources and re-run `rmv_show`, each source gets its own PyMOL objects tagged with a suffix:

```
rmv_source 3
rmv_motifs
rmv_show SARCIN-RICIN     # Creates: SARCIN_RICIN_ALL_S3, SARCIN_RICIN_1_S3, ...

rmv_source 7
rmv_motifs
rmv_show SARCIN-RICIN     # Creates: SARCIN_RICIN_ALL_S7, SARCIN_RICIN_1_S7, ...
```

This allows direct PyMOL comparison:

```
align SARCIN_RICIN_3_S3, SARCIN_RICIN_3_S7
```

---

## 7. User Annotations (FR3D / RMS / RMSX)

Use your own motif annotation files from FR3D, RNAMotifScan (RMS), or RNAMotifScanX (RMSX).

### Directory Setup

Place your annotation files in:

```
rna_motif_visualizer/database/user_annotations/
├── fr3d/                    # FR3D output files
│   └── <output_files>
├── RNAMotifScan/            # RMS files (organized by motif type)
│   ├── c_loop/
│   │   └── Res_1s72
│   ├── sarcin_ricin/
│   │   └── Res_1s72
│   ├── k_turn/
│   │   └── Res_1s72
│   └── ...
└── RNAMotifScanX/           # RMSX files (same structure as RMS)
    ├── c_loop/
    │   └── Res_1s72
    └── ...
```

### Load User Annotations

```
rmv_fetch 1S72

rmv_source 5           # FR3D
rmv_motifs

rmv_source 6           # RNAMotifScan (RMS)
rmv_motifs

rmv_source 7           # RNAMotifScanX (RMSX)
rmv_motifs
```

### P-Value Filtering (RMS/RMSX Only)

RNAMotifScan and RNAMotifScanX include P-values in their output. The plugin uses these to filter results.

```
# Turn filtering off (show ALL results including high P-values)
rmv_source 6 off

# Turn filtering back on (use default thresholds)
rmv_source 6 on

# Set a custom P-value threshold for a specific motif type
rmv_source 6 SARCIN-RICIN 0.01
rmv_source 7 C-LOOP 0.05
```

When filtering is on, only motif instances with P-value ≤ threshold are shown.

---

## 8. Customizing Colors

### View Current Color Assignments

```
rmv_colors
```

Shows the color legend for all loaded motif types.

### Change a Motif's Color

```
rmv_color HL blue        # Hairpin loops → blue
rmv_color GNRA red       # GNRA tetraloops → red
rmv_color IL marine      # Internal loops → marine blue
```

### Change Background (Non-Motif) Color

```
rmv_bg_color white       # White backbone
rmv_bg_color lightgray   # Light gray backbone
rmv_bg_color gray80      # Default (gray80)
```

### Default Color Assignments

| Motif Type | Default Color |
|-----------|---------------|
| HL (Hairpin Loop) | Red |
| IL (Internal Loop) | Cyan |
| J3 (3-Way Junction) | Yellow |
| J4 (4-Way Junction) | Magenta |
| J5 (5-Way Junction) | Green |
| J6 (6-Way Junction) | Orange |
| J7 (7-Way Junction) | Blue |
| GNRA | Teal Green |
| UNCG | Brown Orange |
| K-TURN | Bright Blue |
| SARCIN-RICIN | Dark Red |
| T-LOOP | Pink |
| C-LOOP | Sky Blue |
| U-TURN | Gold |

Any motif type not in this table gets a unique auto-assigned color (bright orange fallback).

---

## 9. Saving Images

### Save All Motif Instances

```
rmv_save ALL                  # Default representation (cartoon)
rmv_save ALL sticks           # Sticks representation
rmv_save ALL spheres          # Spheres representation
rmv_save ALL cartoon+sticks   # Combined representation
```

Images are saved to `motif_images/<PDB_ID>/<MOTIF_TYPE>/` inside the plugin directory.

### Save a Specific Motif Type

```
rmv_save HL                   # All hairpin loop instances as cartoon
rmv_save GNRA sticks          # All GNRA instances as sticks
```

### Save a Specific Instance

```
rmv_save GNRA 1               # Instance 1 as cartoon
rmv_save GNRA 1 spheres       # Instance 1 as spheres
```

### Save the Current PyMOL View

```
rmv_save current              # High-res: 2400×1800, 300 DPI
rmv_save current my_view      # Save to custom filename
```

### Available Representations

| Representation | Description |
|---------------|-------------|
| `cartoon` | Default — shows secondary structure (default) |
| `sticks` | Ball-and-stick atomic detail |
| `spheres` | Space-filling model |
| `ribbon` | Simplified ribbon trace |
| `lines` | Wire frame |
| `licorice` | Thick stick model |
| `surface` | Molecular surface |
| `cartoon+sticks` | Combined view |

### Output Folder Structure

```
motif_images/
└── 1s72/
    ├── HL/
    │   ├── HL_instance_1.png
    │   ├── HL_instance_2.png
    │   └── ...
    ├── GNRA/
    │   ├── GNRA_instance_1.png
    │   └── ...
    └── current_view.png
```

---

## 10. Label Chain IDs (Advanced)

### Background

PDB/CIF files contain two types of chain identifiers:

- **auth_asym_id**: Chain IDs assigned by the authors (e.g., `0`, `9`, `A`, `B`). This is the default.
- **label_asym_id**: System-assigned chain IDs (e.g., `A`, `AA`, `BA`, `CA`). Used by some annotation tools.

### When to Use Label Mode

Use `cif_use_auth=0` when:
- Your user annotations (FR3D/RMS/RMSX) use label chain IDs
- You need label_asym_id chains for your analysis
- Your PDB has unusual auth chain IDs that conflict with annotation tools

### Loading with Label Chain IDs

```
rmv_fetch 1S72 cif_use_auth=0
```

The plugin will:
1. Set PyMOL to use `label_asym_id` as the chain property
2. Parse the CIF file to build an `auth → label` chain mapping
3. Automatically remap motif data (which uses auth chains) to label chains

### Verify Chain Mode

```
rmv_chains
```

Output:

```
Structure: 1S72  |  cif_use_auth = 0 (label_asym_id)  |  Chains: 293
Label chains: A AA AB AC AD ...
```

### Example: Auth vs. Label

Default mode (`cif_use_auth=1`):
```
rmv_fetch 1S72
rmv_summary SARCIN-RICIN
# Shows: Chain 0:158-164, 9:75-81
```

Label mode (`cif_use_auth=0`):
```
rmv_fetch 1S72 cif_use_auth=0
rmv_summary SARCIN-RICIN
# Shows: Chain A:158-164, B:75-81
```

---

## 11. Tips and Tricks

### Force API Refresh (Bypass Cache)

```
rmv_refresh 1S72       # Re-fetch from API, ignore 30-day cache
```

### Check Plugin Status

```
rmv_status             # Loaded PDB, source, chain mode, motif counts
```

### Quick Full Pipeline

```
rmv_fetch 1S72 && rmv_source 3 && rmv_motifs && rmv_show HL
```

Or one command at a time:
```
rmv_fetch 1S72
rmv_source 3
rmv_motifs
rmv_show HL
```

### Compare Two Sources Side by Side

```
rmv_fetch 1S72
rmv_source 3           # BGSU
rmv_motifs
rmv_show HL            # Creates: HL_ALL_S3

rmv_source 1           # Switch to Atlas
rmv_motifs
rmv_show HL            # Creates: HL_ALL_S1 (BGSU objects persist)
```

### Complete Exploration Workflow

```
rmv_fetch 1S72
rmv_source 3
rmv_motifs

rmv_summary                    # What motifs are available?
rmv_summary GNRA               # How many GNRA instances?
rmv_show GNRA                  # Color them on structure
rmv_show GNRA 1                # Zoom to instance 1
rmv_show GNRA 2                # Zoom to instance 2
rmv_all                        # Reset view
rmv_save GNRA sticks           # Save all GNRA images as sticks
rmv_save current               # Save current view
```

### The Legacy `rmv_load` Command

If you prefer to load everything in one step (structure + motifs from previously selected source):

```
rmv_source 3
rmv_load 1S72          # Loads PDB + fetches motifs all at once
```

### Reset Everything

```
delete all             # PyMOL command: delete all objects
rmv_fetch 1S72         # Start fresh
```

---

## Quick Reference Card

| Step | Command | Purpose |
|------|---------|---------|
| Load | `rmv_fetch <PDB>` | Download and load structure |
| Source | `rmv_source <N>` | Select data source (1-7) |
| Motifs | `rmv_motifs` | Fetch motif data |
| Summary | `rmv_summary` | View motif counts |
| Summary | `rmv_summary <TYPE>` | View instances of a type |
| Summary | `rmv_summary <TYPE> <N>` | View single instance details |
| Render | `rmv_show <TYPE>` | Render all instances of a type |
| Render | `rmv_show <TYPE> <N>` | Render a specific instance |
| Zoom | `rmv_show <TYPE> <N>` | Zoom to instance |
| Reset | `rmv_all` | Reset to full view |
| Save | `rmv_save ALL` | Save all motif images |
| Save | `rmv_save current` | Save current view (high-res) |
| Help | `rmv_help` | Full command reference |
| Info | `rmv_sources` | List all data sources |
| Info | `rmv_status` | Plugin status |
| Info | `rmv_chains` | Chain ID diagnostics |
| Color | `rmv_color <TYPE> <COLOR>` | Change motif color |
| Color | `rmv_colors` | View color legend |
| Toggle | `rmv_toggle <TYPE> on/off` | Toggle visibility |
| Background | `rmv_bg_color <COLOR>` | Change backbone color |
| Refresh | `rmv_refresh [PDB]` | Force API cache refresh |

---

*RNA Motif Visualizer v2.3.0 — CBB LAB @Rakib Hasan Rahad*
