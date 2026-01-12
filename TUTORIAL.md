# RNA Motif Visualizer - Complete Tutorial

This tutorial walks you through every command with examples and expected outputs.

---

## 📚 Table of Contents

1. [Getting Started](#1-getting-started)
2. [Loading Your First Structure](#2-loading-your-first-structure)
3. [Exploring Motif Types](#3-exploring-motif-types)
4. [Navigating Instance Details](#4-navigating-instance-details)
5. [Using Different Data Sources](#5-using-different-data-sources)
6. [Advanced Features](#6-advanced-features)
7. [Tips & Tricks](#7-tips--tricks)

---

## 1. Getting Started

### Verify Installation

After installing the plugin and restarting PyMOL, you should see:

```
==================================================
RNA Motif Visualizer v2.1.0 - Loaded Successfully!
==================================================

Available commands:
  rna_load <pdb_id>          Load structure and display motifs
  rna_show <motif_type>      Show specific motif type
  rna_instance <type> <no>   View single motif instance
  rna_all                    Show all motifs
  rna_summary                Display motif summary
  rna_source <mode>          Set data source (auto/local/bgsu/rfam/all)
  
Type 'rna_load 1S72' to get started!
==================================================
```

![Welcome Message](images/tutorial_welcome.png)
<!-- PLACEHOLDER: Screenshot of welcome message -->

**If you don't see this**, the plugin isn't installed correctly. See [README.md](README.md#installation) for help.

---

## 2. Loading Your First Structure

### Step 2.1: Load a Structure

Type in PyMOL console:

```
rna_load 1S72
```

**What happens:**
1. Plugin downloads the PDB structure (if not already loaded)
2. Searches all databases for motifs in this structure
3. Creates PyMOL objects for each motif type
4. Colors motifs distinctly
5. Displays a summary table

**Expected Output:**

```
[RNA Motif Visualizer] Loading 1S72...
[RNA Motif Visualizer] Downloading structure from RCSB PDB...
[RNA Motif Visualizer] Analyzing motifs from local database...
[RNA Motif Visualizer] Analyzing motifs from BGSU API...
[RNA Motif Visualizer] Analyzing motifs from Rfam API...

==================================================
  MOTIF SUMMARY - 1S72
==================================================
  MOTIF TYPE            INSTANCES
--------------------------------------------------
  GNRA                         3
  HL                          15
  IL                          12
  J3                           4
  J4                           2
  K-turn                       1
  T-loop                       2
--------------------------------------------------
  Total                       39
==================================================

  Next steps:
    rna_show GNRA              Highlight & view GNRA instances
    rna_show HL                Highlight & view HL instances
    rna_show IL                Highlight & view IL instances
    rna_summary                Display this summary again
    rna_all                    Show all motifs (default view)
```

![Loaded Structure](images/tutorial_loaded.png)
<!-- PLACEHOLDER: Screenshot of loaded structure with colored motifs -->

### Step 2.2: Understand the Display

- **Colored regions** = Detected motifs
- **Each color** = Different motif type
- **Grey regions** = Non-motif RNA backbone

Look at the **Object Panel** (right side):
- `1S72` - The full structure
- `GNRA`, `HL`, `IL`, etc. - Motif type objects

---

## 3. Exploring Motif Types

### Step 3.1: Show a Specific Motif Type

To focus on GNRA tetraloops:

```
rna_show GNRA
```

**Expected Output:**

```
[RNA Motif Visualizer] Highlighting GNRA motifs...

======================================================================
  GNRA MOTIF INSTANCES
======================================================================
  Total Instances: 3
----------------------------------------------------------------------
  NO.    CHAIN      RESIDUE RANGE             NUCLEOTIDES
----------------------------------------------------------------------
  1      A          A:100-104                 GAAA
  2      A          A:250-254                 GUGA  
  3      B          B:50-54                   GCAA
----------------------------------------------------------------------

  Next steps:
    rna_instance GNRA 1        View instance 1 in detail
    rna_instance GNRA 2        View instance 2 in detail
    rna_instance GNRA 3        View instance 3 in detail
    rna_show HL                Switch to HL motifs
    rna_all                    Show all motifs again
```

**What changes:**
- GNRA motifs are highlighted
- Other motifs are dimmed (but still visible)
- Camera zooms to show all GNRA instances

![GNRA Highlighted](images/tutorial_gnra.png)
<!-- PLACEHOLDER: Screenshot of GNRA motifs highlighted -->

### Step 3.2: Try Different Motif Types

```
rna_show HL     # Hairpin loops
rna_show IL     # Internal loops
rna_show J3     # 3-way junctions
rna_show K-turn # Kink-turns
```

Each command produces a similar instance table specific to that motif type.

### Step 3.3: Return to Full View

```
rna_all
```

**Expected Output:**

```
[RNA Motif Visualizer] Showing all motifs...

All motif types are now visible.

  Next steps:
    rna_show GNRA              Focus on GNRA motifs
    rna_summary                View summary table
```

---

## 4. Navigating Instance Details

### Step 4.1: View an Individual Instance

First, show a motif type:

```
rna_show GNRA
```

Then view a specific instance:

```
rna_instance GNRA 1
```

**Expected Output:**

```
[RNA Motif Visualizer] Showing GNRA instance 1...

======================================================================
  GNRA INSTANCE #1 DETAILS
======================================================================
  Chain: A
  Residue Range: A:100-104
  Nucleotides: G-A-A-A
----------------------------------------------------------------------
  Detailed Residues:
    Position 1: G (A:100)
    Position 2: A (A:101)
    Position 3: A (A:102)
    Position 4: A (A:103)
----------------------------------------------------------------------

  Next steps:
    rna_instance GNRA 2        View next instance
    rna_show GNRA              View all GNRA instances
    rna_all                    Return to full view
```

**What happens:**
- Camera zooms to this specific instance
- Only this instance is highlighted
- Residue details are displayed

![Instance Detail](images/tutorial_instance.png)
<!-- PLACEHOLDER: Screenshot of zoomed instance -->

### Step 4.2: Navigate Between Instances

```
rna_instance GNRA 2  # Next instance
rna_instance GNRA 3  # Third instance
rna_instance GNRA 1  # Back to first
```

### Step 4.3: Out of Range Error

```
rna_instance GNRA 99
```

**Expected Output:**

```
[RNA Motif Visualizer] Error: Instance 99 not found for GNRA
Available instances: 1-3

  Try: rna_instance GNRA 1
```

---

## 5. Using Different Data Sources

### Step 5.1: Check Current Source

```
rna_source_info
```

**Expected Output:**

```
==================================================
  DATA SOURCE CONFIGURATION
==================================================
  Current Mode: AUTO
  
  Source Priority:
    1. Local database (bundled)
    2. BGSU RNA 3D Hub API
    3. Rfam API
    
  Cache Status: Active
  Cache Location: ~/.rna_motif_visualizer_cache/
  Cache Expiry: 30 days
==================================================
```

### Step 5.2: Switch to BGSU API Only

```
rna_source bgsu
```

**Expected Output:**

```
[RNA Motif Visualizer] Data source set to: BGSU

This mode uses the BGSU RNA 3D Hub API directly.
Coverage: ~3000+ PDB structures with hairpin loops,
internal loops, and junction motifs.

Reload your structure to apply: rna_load 1S72
```

### Step 5.3: Switch to Rfam API

```
rna_source rfam
```

**Expected Output:**

```
[RNA Motif Visualizer] Data source set to: RFAM

This mode uses the Rfam API for named motifs.
Available motifs: GNRA, UNCG, K-turn, T-loop, C-loop,
U-turn, Sarcin-ricin loop, and more.

Reload your structure to apply: rna_load 1S72
```

### Step 5.4: Use All Sources Together

```
rna_source all
rna_load 1S72
```

This combines motifs from all sources, giving you the most comprehensive view.

### Step 5.5: Use Local Only (Offline Mode)

```
rna_source local
```

Use this when you don't have internet access.

### Step 5.6: Force Refresh from API

```
rna_refresh
```

**Expected Output:**

```
[RNA Motif Visualizer] Refreshing from APIs (bypassing cache)...
[RNA Motif Visualizer] BGSU API: Fetching fresh data...
[RNA Motif Visualizer] Rfam API: Fetching fresh data...
[RNA Motif Visualizer] Cache updated.

Motifs refreshed. Run rna_summary to see updated counts.
```

---

## 6. Advanced Features

### Step 6.1: View Summary Anytime

```
rna_summary
```

This redisplays the motif summary table without reloading.

### Step 6.2: Toggle Motif Visibility

```
rna_toggle HL off    # Hide hairpin loops
rna_toggle HL on     # Show them again
rna_toggle IL off    # Hide internal loops
```

### Step 6.3: Switch Between Databases

```
rna_databases        # List available databases
rna_switch atlas     # Switch to RNA 3D Atlas format
rna_switch rfam      # Switch to Rfam format
```

### Step 6.4: Check Current Status

```
rna_status
```

**Expected Output:**

```
==================================================
  RNA MOTIF VISUALIZER STATUS
==================================================
  Version: 2.1.0
  Loaded Structure: 1S72
  Source Mode: AUTO
  Cache: Active (30 day expiry)
  
  Motif Objects:
    GNRA: 3 instances (visible)
    HL: 15 instances (visible)
    IL: 12 instances (visible)
    J3: 4 instances (hidden)
==================================================
```

### Step 6.5: Change Background Color

```
rna_bg_color white   # White background
rna_bg_color black   # Black background (default)
rna_bg_color grey    # Grey background
```

---

## 7. Tips & Tricks

### Tip 1: Use Tab Completion

PyMOL supports tab completion. Type `rna_` and press Tab to see all commands.

### Tip 2: Follow the Suggestions

After each command, check the console for **"Next steps"** suggestions. They guide you through the workflow.

### Tip 3: Quick Reset

```
cmd.delete("all")    # Clear everything
rna_load 1S72        # Start fresh
```

### Tip 4: Compare Structures

```
# Load first structure
rna_load 1S72

# Clear motif objects but keep structure
cmd.delete("GNRA HL IL J*")

# Load second structure
rna_load 3J2B

# Now you can compare
```

### Tip 5: Save Your View

```
# After positioning the view nicely
cmd.png("my_motif_view.png", dpi=300)
```

### Tip 6: Get Help on Any Command

```
help rna_load
help rna_show
```

### Tip 7: Keyboard Shortcuts

Standard PyMOL shortcuts work:
- `Ctrl+R` - Reset view
- `Ctrl+Z` - Undo
- `F` - Focus on selection

---

## 🎯 Common Workflows

### Workflow 1: Quick Analysis

```
rna_load 1S72
rna_summary
```

Just see what motifs are present.

### Workflow 2: Detailed Motif Exploration

```
rna_load 1S72
rna_show GNRA
rna_instance GNRA 1
rna_instance GNRA 2
rna_instance GNRA 3
rna_all
```

Examine each GNRA tetraloop in detail.

### Workflow 3: Compare Motif Sources

```
rna_source local
rna_load 1S72
rna_summary          # Note the counts

rna_source bgsu
rna_load 1S72
rna_summary          # Compare with BGSU

rna_source all
rna_load 1S72
rna_summary          # See combined results
```

### Workflow 4: Publication Figure

```
rna_load 1S72
rna_show GNRA
rna_instance GNRA 1
rna_bg_color white
ray 2400, 2400
png "gnra_tetraloop.png"
```

---

## 📝 Command Quick Reference

| Action | Command |
|--------|---------|
| Load structure | `rna_load 1S72` |
| Show all motifs | `rna_all` |
| Focus on type | `rna_show GNRA` |
| View instance | `rna_instance GNRA 1` |
| See summary | `rna_summary` |
| Change source | `rna_source bgsu` |
| Force refresh | `rna_refresh` |
| Hide motif type | `rna_toggle HL off` |
| Check status | `rna_status` |

---

## 🆘 Need Help?

- See [README.md](README.md) for installation and troubleshooting
- See [DEVELOPER.md](DEVELOPER.md) for technical details
- Open an issue on GitHub for bugs

---

<p align="center">
  <b>Happy Exploring! 🔬</b>
</p>
