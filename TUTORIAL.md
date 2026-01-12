# RNA Motif Visualizer - Tutorial

Step-by-step guide to using the RNA Motif Visualizer plugin in PyMOL.

---

## 📚 Table of Contents

1. [Getting Started](#1-getting-started)
2. [Data Sources](#2-data-sources)
3. [Loading Structures](#3-loading-structures)
4. [Exploring Motifs](#4-exploring-motifs)
5. [Instance Navigation](#5-instance-navigation)
6. [Customizing Colors](#6-customizing-colors)
7. [Common Workflows](#7-common-workflows)

---

## 1. Getting Started

### Verify Installation

After installing and restarting PyMOL, you should see:

```
==================================================
RNA Motif Visualizer v2.1.0 - Loaded Successfully!
==================================================
```

### View All Commands

```
rna_help
```

This displays a categorized command reference:

```
┌──────────────────────────────────────────────────────────────────────┐
│  LOADING & SOURCES                                                   │
├──────────────────────────────────────────────────────────────────────┤
│  rna_load <PDB_ID>           Load structure and visualize motifs     │
│  rna_source                  Show current source mode & config       │
│  rna_source <MODE>           Set source (auto/local/bgsu/rfam/all)   │
│  rna_sources                 Show all available sources (detailed)   │
│  rna_switch <DB>             Switch database (atlas/rfam)            │
│  rna_refresh [PDB_ID]        Force refresh from API (bypass cache)   │
├──────────────────────────────────────────────────────────────────────┤
│  VISUALIZATION                                                       │
├──────────────────────────────────────────────────────────────────────┤
│  rna_all                     Show all motifs (reset view)            │
│  rna_show <MOTIF_TYPE>       Highlight specific motif type           │
│  rna_instance <TYPE> <NO>    View single instance (zoom + details)   │
│  rna_toggle <TYPE> <on|off>  Toggle motif visibility                 │
│  rna_bg_color <COLOR>        Change background color (e.g., gray80)  │
│  rna_color <TYPE> <COLOR>    Change motif color (e.g., HL blue)      │
│  rna_colors                  Show color legend for motif types       │
├──────────────────────────────────────────────────────────────────────┤
│  INFORMATION                                                         │
├──────────────────────────────────────────────────────────────────────┤
│  rna_summary                 Show motif types and instance counts    │
│  rna_status                  Show current plugin status              │
│  rna_help                    Show this command reference             │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Data Sources

### Check Available Sources

```
rna_sources
```

This shows LOCAL and ONLINE sources separately:

```
======================================================================
  RNA MOTIF DATA SOURCES
======================================================================

  Current Mode: AUTO

----------------------------------------------------------------------
  LOCAL SOURCES (Offline - Bundled with Plugin)
----------------------------------------------------------------------
  • RNA 3D Motif Atlas (Local)
    ID: atlas
    Structures: 50 PDBs
    Motif Types: HL, IL, J3, J4, J5, J6, J7

----------------------------------------------------------------------
  ONLINE SOURCES (Require Internet)
----------------------------------------------------------------------
  • BGSU RNA 3D Hub API
    ID: bgsu_api
    Coverage: ~3000+ RNA structures

  • Rfam API
    ID: rfam_api
    Coverage: Named RNA motif families
======================================================================
```

### Check Current Source Status

```
rna_source
```

Shows current mode and configuration (without changing anything).

### Set Source Mode

```
rna_source bgsu     # Use BGSU API (~3000+ structures)
rna_source rfam     # Use Rfam API (named motifs)
rna_source local    # Use bundled offline database
rna_source auto     # Smart selection (default)
rna_source all      # Combine all sources
```

---

## 3. Loading Structures

### Basic Load

```
rna_load 1S72
```

Output:
```
[RNA Motif Visualizer] Loading 1S72...
[RNA Motif Visualizer] Downloading structure from RCSB PDB...
[RNA Motif Visualizer] Analyzing motifs from BGSU API...

==================================================
  MOTIF SUMMARY - 1S72
==================================================
  MOTIF TYPE            INSTANCES
--------------------------------------------------
  HL                          45
  IL                          32
  J3                           8
  J4                           2
--------------------------------------------------
  Total                       87
==================================================

  Next steps:
    rna_show HL                Highlight & view HL instances
    rna_summary                Display this summary again
```

### Load with Specific Background

```
rna_load 1S72 white
```

### Force Refresh from API

```
rna_refresh
```

Bypasses cache and fetches fresh data from APIs.

---

## 4. Exploring Motifs

### Show Specific Motif Type

```
rna_show HL
```

Output:
```
[RNA Motif Visualizer] Highlighting HL motifs...

======================================================================
  HL MOTIF INSTANCES
======================================================================
  Total Instances: 45
----------------------------------------------------------------------
  NO.    CHAIN      RESIDUE RANGE             NUCLEOTIDES
----------------------------------------------------------------------
  1      0          0:100-104                 GAAA
  2      0          0:250-254                 GUGA
  3      0          0:500-504                 GCAA
  ...
----------------------------------------------------------------------

  Next steps:
    rna_instance HL 1          View instance 1 in detail
    rna_show IL                Switch to IL motifs
    rna_all                    Show all motifs again
```

### Show All Motifs

```
rna_all
```

Resets view to show all motif types.

### Toggle Visibility

```
rna_toggle HL off    # Hide hairpin loops
rna_toggle HL on     # Show them again
```

---

## 5. Instance Navigation

### View Single Instance

```
rna_instance HL 1
```

Output:
```
[RNA Motif Visualizer] Showing HL instance 1...

======================================================================
  HL INSTANCE #1 DETAILS
======================================================================
  Chain: 0
  Residue Range: 0:100-104
----------------------------------------------------------------------
  Detailed Residues:
    Position 1: G (0:100)
    Position 2: A (0:101)
    Position 3: A (0:102)
    Position 4: A (0:103)
----------------------------------------------------------------------

  Next steps:
    rna_instance HL 2          View next instance
    rna_show HL                View all HL instances
    rna_all                    Return to full view
```

The camera zooms to the instance location.

### Navigate Between Instances

```
rna_instance HL 2    # Next instance
rna_instance HL 3    # Third instance
rna_instance HL 1    # Back to first
```

---

## 6. Customizing Colors

### View Current Colors

```
rna_colors
```

Output:
```
======================================================================
  MOTIF COLOR LEGEND
======================================================================
  MOTIF TYPE          COLOR
----------------------------------------------------------------------
  HL                  Red (1.00, 0.40, 0.40)
  IL                  Orange (1.00, 0.60, 0.20)
  J3                  Yellow (1.00, 0.80, 0.20)
  J4                  Green (0.20, 0.80, 0.20)
  GNRA                Forest Green (0.20, 0.60, 0.20)
  K-turn              Marine Blue (0.10, 0.40, 0.60)
======================================================================
```

### Change Motif Color

```
rna_color HL blue       # Change hairpin loops to blue
rna_color GNRA red      # Change GNRA tetraloops to red
rna_color IL cyan       # Change internal loops to cyan
```

Available colors:
- Basic: red, green, blue, yellow, cyan, magenta
- Extended: orange, purple, pink, white, gray, lime, teal, salmon
- PyMOL: forest, marine, slate, firebrick, deepolive

### Change Background Color

```
rna_bg_color white
rna_bg_color gray80
rna_bg_color black
```

---

## 7. Common Workflows

### Quick Analysis

```
rna_help                 # See all commands
rna_sources              # Check available sources
rna_source bgsu          # Use BGSU API
rna_load 1S72            # Load structure
rna_summary              # See motif counts
```

### Detailed Motif Exploration

```
rna_load 1S72
rna_show HL              # Focus on hairpin loops
rna_instance HL 1        # Examine first instance
rna_instance HL 2        # Next instance
rna_all                  # Back to full view
```

### Compare Sources

```
rna_source local
rna_load 1S72
rna_summary              # Note counts from local

rna_source bgsu
rna_load 1S72
rna_summary              # Compare with BGSU API

rna_source all
rna_load 1S72
rna_summary              # Combined results
```

### Publication Figure

```
rna_load 1S72
rna_show GNRA
rna_instance GNRA 1
rna_color GNRA red       # Custom color
rna_bg_color white       # White background
ray 2400, 2400
png "gnra_tetraloop.png"
```

---

## 📝 Command Quick Reference

| Action | Command |
|--------|---------|
| See all commands | `rna_help` |
| Check sources | `rna_sources` |
| Set source | `rna_source bgsu` |
| Load structure | `rna_load 1S72` |
| Show all motifs | `rna_all` |
| Focus on type | `rna_show HL` |
| View instance | `rna_instance HL 1` |
| See summary | `rna_summary` |
| Change color | `rna_color HL blue` |
| Force refresh | `rna_refresh` |
| Check status | `rna_status` |

---

## 🆘 Need Help?

- See [README.md](README.md) for installation
- See [DEVELOPER.md](DEVELOPER.md) for technical details
- Open an issue on GitHub for bugs

---

<p align="center">
  <b>Happy Exploring! 🔬</b>
</p>
