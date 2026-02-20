# RNA Motif Visualizer — Architecture Changes Report

**Date:** 20 February 2026  
**Version:** 2.2.0 → 2.3.0  
**Author:** CBB LAB @Rakib Hasan Rahad  

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Split Fetch Pipeline](#2-split-fetch-pipeline)
3. [Label ID Support (cif_use_auth)](#3-label-id-support-cif_use_auth)
4. [Chain ID Handling — Complete Architecture](#4-chain-id-handling--complete-architecture)
5. [Files Modified](#5-files-modified)
6. [Command Reference (New Workflow)](#6-command-reference-new-workflow)
7. [Testing Guide](#7-testing-guide)

---

## 1. Executive Summary

Two major architectural changes were implemented in v2.3.0:

| Change | Purpose |
|--------|---------|
| **Split Fetch Pipeline** | Separates PDB loading from motif data fetching, improving perceived latency and enabling free source-switching |
| **Label ID Support** | Adds `cif_use_auth=0` option so users whose annotations use `label_asym_id` (system chain IDs) can work with them natively |

### Before (v2.2.0)
```
rmv_source 3          # Select source
rmv_fetch 1S72        # Downloads PDB + fetches motifs (one slow step)
```

### After (v2.3.0)
```
rmv_fetch 1S72        # Downloads PDB only (fast, ~2-3 seconds)
rmv_source 3          # Select source (instant)
rmv_motifs            # Fetch motif data from source
```

The PDB structure is loaded once and reused across source switches — no re-downloading.

---

## 2. Split Fetch Pipeline

### 2.1 Motivation

In v2.2.0, `rmv_fetch` did everything in one step: download the PDB, fetch motif data from the selected source, parse it, and create PyMOL objects. This had two problems:

1. **Latency** — Users waited for the entire pipeline before seeing anything in PyMOL
2. **Rigidity** — Switching sources required re-running `rmv_fetch`, which re-downloaded the PDB

### 2.2 New Architecture

The pipeline is now split into three independent stages:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   rmv_fetch     │ ──► │   rmv_source    │ ──► │   rmv_motifs    │
│  (PDB only)     │     │  (select DB)    │     │ (fetch motifs)  │
│                 │     │                 │     │                 │
│ • Downloads CIF │     │ • Instant       │     │ • Fetches from  │
│ • Loads into    │     │ • Sets mode     │     │   current src   │
│   PyMOL         │     │   + source ID   │     │ • Parses data   │
│ • Shows chains  │     │ • No PDB work   │     │ • Creates objs  │
│ • Stores state  │     │                 │     │ • Shows summary │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        ▼                                               ▼
   gui.loaded_pdb                              gui.loaded_motifs
   gui.loaded_pdb_id                           PyMOL objects
   gui.cif_use_auth                            (with _S{N} suffix)
```

### 2.3 Key Design Decision: PDB Object Has No Source Suffix

```
PDB structure name:   1s72           (always lowercase PDB ID, shared)
Motif object name:    HL_ALL_S3      (source-tagged with _S3, _S7, etc.)
Instance object name: HL_1_S3        (source-tagged)
```

This means:
- The PDB object `1s72` is loaded once and never recreated
- Switching `rmv_source 3` → `rmv_source 7` → `rmv_motifs` reuses the same PDB
- Motif objects carry source tags so multi-source compare still works

### 2.4 Implementation Details

#### `fetch_raw_pdb()` (gui.py ~L2097)
**New signature:** `fetch_raw_pdb(pdb_id='', background_color='', cif_use_auth='')`

What it does now:
1. Parses `cif_use_auth` parameter (0/off/false/label → 0, else 1)
2. Stores `gui.cif_use_auth = cif_auth_val`
3. Sets PyMOL's `cmd.set("cif_use_auth", val)` before download
4. Calls `cmd.fetch(pdb_id, structure_name)` — downloads CIF from RCSB
5. Stores `gui.loaded_pdb = structure_name` and `gui.loaded_pdb_id = pdb_id.upper()`
6. Clears `gui.viz_manager.motif_loader.loaded_motifs = {}`
7. Shows chains and context-aware next-step suggestions

What it **no longer** does:
- ~~Calls `fetch_motif_data_action()`~~
- ~~Calls `load_user_annotations_action()`~~
- ~~Creates any motif objects~~

#### `load_motif_data()` (gui.py ~L2195) — **NEW**
**Registered as:** `cmd.extend('rmv_motifs', load_motif_data)`

What it does:
1. Checks `gui.loaded_pdb_id` exists → error if no PDB loaded
2. Checks `gui.current_source_mode` exists → error if no source selected
3. Dispatches to:
   - `gui.load_user_annotations_action()` for user annotation sources (FR3D, RMS, RMSX)
   - `gui.fetch_motif_data_action()` for all other sources (Atlas, Rfam, BGSU, etc.)

#### `fetch_motif_data_action()` (gui.py ~L105)
Updated to use:
```python
structure_name = self.loaded_pdb or pdb_id.lower()
```
Instead of computing a source-suffixed name. The PDB object is shared.

#### Source handler next-step suggestions
All 4 source handlers (local, web, user, multi) now show context-aware suggestions:
- If PDB is already loaded → `rmv_motifs   Fetch motif data for {PDB}`
- If no PDB loaded → `rmv_fetch <PDB_ID>` then `rmv_motifs`

---

## 3. Label ID Support (cif_use_auth)

### 3.1 Background: auth_asym_id vs label_asym_id

mmCIF files contain two chain ID systems:

| Field | Name | Example (1S72) | Used By |
|-------|------|-----------------|---------|
| `auth_asym_id` | Author chain ID | 0, 9, A, B, C... | PDB files, BGSU, Atlas, most tools |
| `label_asym_id` | System chain ID | AA, BA, CA, DA... | Some computational pipelines |

PyMOL's `cif_use_auth` setting controls which one becomes the `chain` property:
- `cif_use_auth=1` (default) → chain = auth_asym_id
- `cif_use_auth=0` → chain = label_asym_id

### 3.2 New Feature

Users can now load structures with label_asym_id chains:

```
rmv_fetch 1S72 cif_use_auth=0    # Chains become AA, BA, CA...
```

The setting is:
- **Stored** in `gui.cif_use_auth` for downstream use
- **Applied** via `cmd.set("cif_use_auth", val)` before the CIF download
- **Respected** by `rmv_chains` diagnostics (no longer hardcodes auth)
- **Used** by chain mapping logic in `load_user_annotations_action()`

### 3.3 When Label Mode Applies

| Scenario | cif_use_auth |
|----------|-------------|
| `rmv_fetch 1S72` | 1 (auth, default) |
| `rmv_fetch 1S72 cif_use_auth=0` | 0 (label) |
| Local PDB file via `rmv_load` | Always 1 (PDB format only has auth) |
| After switching with no re-fetch | Keeps previous value |

---

## 4. Chain ID Handling — Complete Architecture

This is the comprehensive chain ID protection system built across multiple versions. It uses a **3-layer defense** plus a **runtime mapping layer** to ensure motif annotations (which use auth_asym_id) correctly map to the chains PyMOL exposes.

### 4.1 The Problem

RNA structures like 1S72 have complex chain layouts:
- **59 chains** in the mmCIF file
- Auth IDs: `0, 9, A, B, C, D, ...`
- Label IDs: `AA, BA, CA, DA, ...`

Motif annotation sources (BGSU, Atlas, FR3D, RMS, RMSX) all reference chains using **auth_asym_id**. If PyMOL loads the structure with label_asym_id, every residue selection like `chain A and resi 2694` would fail because the chain is now `CA` instead of `A`.

### 4.2 Layer 1 — Plugin Startup Lock

**File:** `plugin.py` → `__init_plugin__()`  
**When:** Plugin loads into PyMOL (before any user commands)

```python
# Layer 1: Lock chain ID convention to auth_asym_id
cmd.set("cif_use_auth", 1)
logger.debug("Chain ID convention locked: cif_use_auth=1 (auth_asym_id)")
```

This ensures that even if the user had previously changed the setting in their PyMOL session, the plugin starts with a known-good state. Auth chains are the universal convention used by all motif databases.

### 4.3 Layer 2 — Fetch-Time Enforcement

**File:** `gui.py` → `fetch_raw_pdb()`  
**When:** Every time the user loads a PDB structure

```python
# Handle cif_use_auth parameter
cif_auth_val = 1  # Default: auth_asym_id
if cif_use_auth:
    cif_str = str(cif_use_auth).strip()
    if cif_str in ('0', 'off', 'false', 'label'):
        cif_auth_val = 0

gui.cif_use_auth = cif_auth_val

# Set cif_use_auth BEFORE fetching the CIF
cmd.set("cif_use_auth", cif_auth_val)
cmd.fetch(pdb_arg, structure_name)
```

Key points:
- The setting is applied **before** `cmd.fetch()` so PyMOL interprets chain IDs correctly during CIF parsing
- The value is stored in `gui.cif_use_auth` for downstream chain mapping
- Default is always 1 (auth) unless the user explicitly passes `cif_use_auth=0`

### 4.4 Layer 3 — Runtime Diagnostics

**File:** `gui.py` → `show_chain_diagnostics()` (rmv_chains command)  
**When:** User runs `rmv_chains` to inspect chain IDs

```python
# Read current cif_use_auth from GUI state
cif_auth_val = getattr(gui, 'cif_use_auth', 1)
chain_mode = "auth_asym_id" if cif_auth_val == 1 else "label_asym_id"
chain_label = "Auth chains" if cif_auth_val == 1 else "Label chains"

# Display actual chains from PyMOL
chains = cmd.get_chains(structure_name)
print(f"Structure: {structure_name.upper()}  |  cif_use_auth = {cif_auth_val} ({chain_mode})  |  Chains: {len(chains)}")
print(f"{chain_label}: {' '.join(chains)}")
```

In v2.3.0, this layer was updated to:
- **Read** `gui.cif_use_auth` dynamically instead of hardcoding `1`
- **Display** "Label chains" vs "Auth chains" based on the actual mode
- **Not reset** the setting — respects the user's choice if they used `cif_use_auth=0`

### 4.5 Layer 4 — Chain Mapping at Motif Load Time (Runtime Mapping)

**File:** `gui.py` → `load_user_annotations_action()`  
**When:** User annotations (FR3D/RMS/RMSX) are loaded

This is the most complex layer. Annotation files from FR3D, RMS, and RMSX reference chains using their own conventions:

| Tool | Chain Convention | Example |
|------|-----------------|---------|
| FR3D | Numeric: 1, 2, 3... | `1` = first chain |
| RMS/RMSX | "0" for primary chain | `0` = first RNA chain |
| BGSU/Atlas | Auth IDs directly | `A`, `0`, `9` |

The mapping logic queries PyMOL for the actual loaded chains and creates a mapping dictionary:

```python
actual_chains = cmd.get_chains(structure_name)

if tool == 'fr3d':
    # Map numeric → actual: {1: 'A', 2: 'B', 3: 'C', ...}
    for idx, actual_chain in enumerate(sorted(actual_chains), 1):
        chain_mapping[str(idx)] = actual_chain

elif tool in ['rnamotifscan', 'rnamotifscanx']:
    # Map '0' → first chain
    sorted_chains = sorted(actual_chains)
    chain_mapping['0'] = sorted_chains[0]
    
    # In label mode, map sequential auth IDs to label chains
    if gui.cif_use_auth == 0 and len(sorted_chains) > 1:
        for idx, label_chain in enumerate(sorted_chains):
            chain_mapping[str(idx)] = label_chain
```

**How it works in practice:**

Auth mode (`cif_use_auth=1`):
```
PyMOL chains: [0, 9, A, B, C, D, ...]
Annotation says: chain "0" resi 2694
Mapping: "0" → "0"  ✓ (exact match, annotation works)
```

Label mode (`cif_use_auth=0`):
```
PyMOL chains: [AA, BA, CA, DA, ...]
Annotation says: chain "0" resi 2694
Mapping: "0" → "AA"  ✓ (mapped to first label chain)
Annotation says: chain "A"
Mapping: needs extra entries → creates sequential map
```

### 4.6 Complete Chain ID Flow Diagram

```
Plugin Load (Layer 1)
    │
    ▼  cmd.set("cif_use_auth", 1)
    │
User runs: rmv_fetch 1S72 [cif_use_auth=0]
    │
    ▼  Layer 2: Parse param, store gui.cif_use_auth
    │           cmd.set("cif_use_auth", val)
    │           cmd.fetch("1S72", "1s72")
    │
    ▼  PyMOL loads CIF, chain property = auth or label
    │
User runs: rmv_chains (Layer 3)
    │
    ▼  Reads gui.cif_use_auth, shows actual chains
    │  "Auth chains: 0 9 A B C..." or "Label chains: AA BA CA..."
    │
User runs: rmv_source 7 → rmv_motifs
    │
    ▼  Layer 4: Chain mapping at motif load time
    │  Queries cmd.get_chains() for actual loaded chains
    │  Maps annotation chain IDs → actual PyMOL chain IDs
    │  Creates selection strings with correct chains
    │
    ▼  Motifs render correctly regardless of chain ID mode
```

### 4.7 Why All 4 Layers Are Needed

| Layer | Protects Against |
|-------|-----------------|
| **1 — Startup Lock** | User's PyMOL session having `cif_use_auth=0` from previous work |
| **2 — Fetch-Time** | CIF being parsed with wrong chain convention |
| **3 — Diagnostics** | User confusion about which chains are active |
| **4 — Runtime Mapping** | Annotation tools using different chain ID schemes than PyMOL |

Without Layer 4, label_asym_id mode would be impossible — annotations reference auth IDs but PyMOL's chains would be label IDs. The mapping bridges this gap dynamically at query time.

---

## 5. Files Modified

### gui.py (12 changes)

| # | Change | Location |
|---|--------|----------|
| 1 | Added `self.cif_use_auth = 1` state variable | `__init__` ~L62 |
| 2 | Rewrote `fetch_raw_pdb()` — PDB only + cif_use_auth param | ~L2097 |
| 3 | Added `load_motif_data()` — rmv_motifs handler | ~L2195 |
| 4 | Registered `cmd.extend('rmv_motifs', ...)` | ~L2237 |
| 5 | Updated `fetch_motif_data_action()` — uses `self.loaded_pdb` | ~L105 |
| 6 | Updated `load_user_annotations_action()` — uses `self.loaded_pdb` + label chain mapping | ~L510 |
| 7 | Updated all 4 source handler next-step suggestions (context-aware) | ~L1506, 1540, 1582, 1660 |
| 8 | Updated `print_help()` LOADING section — added rmv_motifs, cif_use_auth=0 | ~L1085 |
| 9 | Updated QUICK EXAMPLES — 5 new examples reflecting split workflow | ~L1135 |
| 10 | Updated Quick Start logger lines at bottom | ~L2793 |
| 11 | Updated `rmv_chains` diagnostics — dynamic cif_use_auth display | ~L2761 |
| 12 | Version bump 2.2.0 → 2.3.0 | docstring L11 |

### plugin.py (3 changes)

| # | Change | Location |
|---|--------|----------|
| 1 | Version 2.2.0 → 2.3.0 | docstring L6, banner ~L100 |
| 2 | Date → 20 February 2026 | banner ~L98 |
| 3 | Quick Start: rmv_fetch → rmv_source → rmv_motifs order + rmv_motifs added | banner ~L108 |

### loader.py — No changes needed

Chain IDs flow from residue tuples which are already chain-mapped upstream in gui.py. The display layer automatically shows whichever chain IDs are in the data.

---

## 6. Command Reference (New Workflow)

### Standard Workflow
```
rmv_fetch 1S72              # Step 1: Load PDB structure (fast)
rmv_source 3                # Step 2: Select BGSU API
rmv_motifs                  # Step 3: Fetch motif data
rmv_summary                 # Step 4: View available motifs
rmv_show HL                 # Step 5: Render hairpin loops
rmv_instance HL 1           # Step 6: View specific instance
```

### Switch Sources (no re-download)
```
rmv_source 7                # Switch to RMSX
rmv_motifs                  # Fetch from new source (PDB already loaded)
rmv_show SARCIN-RICIN       # Objects tagged _S7
```

### Multi-Source Compare
```
rmv_source combine 3 7      # Combine BGSU + RMSX
rmv_motifs                  # Fetch from both sources
rmv_summary                 # Shows merged data
```

### Label Chain Mode
```
rmv_fetch 1S72 cif_use_auth=0   # Load with label_asym_id (AA, BA, CA...)
rmv_chains                       # Verify: shows "Label chains: AA BA CA..."
rmv_source 7                     # Select RMSX
rmv_motifs                       # Chain mapping handles auth→label translation
```

### Save High-Res Images
```
rmv_save ALL                # Save all motifs (2400×1800, 300 DPI)
rmv_save current            # Save current PyMOL view
```

---

## 7. Testing Guide

### Test 1: Basic Split Pipeline
```
rmv_fetch 1S72              → Should load PDB, show 59 chains, NOT load motifs
rmv_source 3                → Should show "BGSU API selected"
rmv_motifs                  → Should fetch ~41 motif types
rmv_summary                 → Should display summary table
```

### Test 2: Source Switching
```
rmv_fetch 1S72
rmv_source 3
rmv_motifs                  → Objects tagged _S3
rmv_source 7
rmv_motifs                  → Objects tagged _S7 (no PDB re-download)
```

### Test 3: Error Cases
```
rmv_motifs                  → "No PDB structure loaded"
rmv_fetch 1S72
rmv_motifs                  → "No source selected"
```

### Test 4: Label Mode
```
rmv_fetch 1S72 cif_use_auth=0   → Chains: AA, BA, CA, DA...
rmv_chains                       → Shows "Label chains" (not "Auth chains")
rmv_source 7
rmv_motifs                       → Chain mapping translates "0" → "AA"
```

### Test 5: Auth Mode (default)
```
rmv_fetch 1S72                   → Chains: 0, 9, A, B, C...
rmv_chains                       → Shows "Auth chains" with cif_use_auth=1
```

---

*End of report — v2.3.0 architectural changes, 20 February 2026*
