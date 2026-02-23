# RNA Motif Visualizer — Developer Guide

Technical reference for developers working on the RNA Motif Visualizer PyMOL plugin.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Project Structure](#2-project-structure)
3. [Initialization Flow](#3-initialization-flow)
4. [Command Reference](#4-command-reference)
5. [Data Sources & Providers](#5-data-sources--providers)
6. [Chain ID System](#6-chain-id-system)
7. [Multi-Source Pipeline](#7-multi-source-pipeline)
8. [Color System](#8-color-system)
9. [Image Export](#9-image-export)
10. [Caching](#10-caching)
11. [Adding a New Data Source](#11-adding-a-new-data-source)
12. [Key Classes & Methods](#12-key-classes--methods)

---

## 1. Architecture Overview

```
PyMOL
├── plugin.py              Entry point (__init_plugin__)
├── gui.py                 Command registration & GUI state (MotifVisualizerGUI)
├── loader.py              Visualization pipeline (StructureLoader, UnifiedMotifLoader, VisualizationManager)
├── colors.py              30+ motif color definitions + custom color support
├── image_saver.py         PNG export with multiple representations
├── database/
│   ├── config.py          SOURCE_ID_MAP (7 sources), SourceMode, PluginConfig
│   ├── base_provider.py   ResidueSpec, MotifInstance, MotifType, BaseProvider ABC
│   ├── registry.py        DatabaseRegistry — lazily loads providers
│   ├── atlas_provider.py  Atlas JSON provider (759 PDBs)
│   ├── rfam_provider.py   Rfam Stockholm provider (173 PDBs)
│   ├── bgsu_api_provider.py  Hybrid HTML scraping + CSV fallback (~3000+ PDBs)
│   ├── rfam_api_provider.py  Rfam API (GNRA, UNCG, K-turn, etc.)
│   ├── source_selector.py  Smart source selection with fallback chain
│   ├── cascade_merger.py   Right-to-left merge with Jaccard dedup (≥60%)
│   ├── homolog_enricher.py NR representative lookup for semantic enrichment
│   ├── cache_manager.py    30-day disk cache at ~/.rna_motif_visualizer_cache/
│   ├── converters.py       Format converters for provider outputs
│   ├── motif_merger.py     Legacy merger (superseded by cascade_merger)
│   ├── source_registry.py  Alternate registry (deprecated)
│   ├── representative_set.py NR list loader
│   ├── nrlist_4.24_all.csv   BGSU NR representative list
│   └── user_annotations/
│       ├── user_provider.py  FR3D/RMS/RMSX annotation loader
│       └── converters.py     User annotation format parsers
└── utils/
    ├── logger.py          PluginLogger with colored PyMOL console output
    ├── parser.py          PDB ID + selection string parsers
    └── selectors.py       3-layer chain ID protection for PyMOL selections
```

### Data Flow

```
rmv_fetch <PDB>  →  PyMOL cmd.fetch()  →  store loaded_pdb / loaded_pdb_id
                                         →  parse CIF for auth→label chain map (if cif_use_auth=0)

rmv_db <N>       →  set source mode + provider config in GUI state

rmv_load_motif   →  dispatch to:
                     ├── Local/Web:  fetch_motif_data_action()
                     │   └── source_selector → provider.get_motifs() → enrich → merge → store
                     └── User:  load_user_annotations_action()
                         └── user_provider.load_annotations() → parse → store

rmv_show <TYPE>  →  VisualizationManager.show_motif_type()
                     └── create PyMOL objects + color selections

rmv_save <TYPE>  →  ImageSaver.save_motif_images()
                     └── render + ray + png for each instance
```

---

## 2. Project Structure

### Source Code Files

| File | Lines | Purpose |
|------|-------|---------|
| `gui.py` | ~3100 | Main GUI class, all 18 command registrations, state management |
| `loader.py` | ~1640 | StructureLoader, UnifiedMotifLoader, VisualizationManager |
| `plugin.py` | ~120 | Entry point, cif_use_auth lock, welcome banner |
| `colors.py` | ~330 | MOTIF_COLORS dict, custom overrides, PyMOL color application |
| `image_saver.py` | ~580 | PNG export for individual motif instances + current view |
| `__init__.py` | ~45 | Package metadata, lazy imports |
| `atlas_loader.py` | legacy | Old atlas loader (superseded by database/atlas_provider.py) |
| `pdb_motif_mapper.py` | legacy | Old PDB-to-motif mapper |

### Database Module

| File | Purpose |
|------|---------|
| `config.py` | SOURCE_ID_MAP (7 entries), SourceMode enum, PluginConfig dataclass |
| `base_provider.py` | ABC for all providers: ResidueSpec, MotifInstance, MotifType, BaseProvider |
| `registry.py` | DatabaseRegistry — discovers and registers providers |
| `atlas_provider.py` | Parses bundled Atlas JSON files (759 PDBs, 7 motif types: HL, IL, J3-J7) |
| `rfam_provider.py` | Parses bundled Rfam Stockholm files (173 PDBs, 19 motif types) |
| `bgsu_api_provider.py` | Hybrid: HTML scraping from rna.bgsu.edu + CSV fallback for loop data |
| `rfam_api_provider.py` | REST API calls to Rfam for motif family annotations |
| `source_selector.py` | Routes source selection to appropriate provider(s) |
| `cascade_merger.py` | Merges motifs from multiple sources with Jaccard deduplication |
| `homolog_enricher.py` | Enriches generic motif names using NR homolog representatives |
| `cache_manager.py` | Disk cache with 30-day expiry at `~/.rna_motif_visualizer_cache/` |
| `converters.py` | Converts provider-specific output to unified MotifInstance format |
| `representative_set.py` | Loads BGSU NR representative list for homolog lookup |

### Utils Module

| File | Purpose |
|------|---------|
| `logger.py` | `PluginLogger` — colored console output via `cmd.feedback` |
| `parser.py` | Parses PDB IDs, file paths, selection strings |
| `selectors.py` | 3-layer chain ID protection: builds safe PyMOL selection strings |

---

## 3. Initialization Flow

When PyMOL loads the plugin (`__init_plugin__` in `plugin.py`):

1. **Logger setup** — `initialize_logger(use_pymol_console=True)`
2. **Chain ID lock** — `cmd.set("cif_use_auth", 1)` — ensures auth_asym_id by default
3. **Registry init** — `initialize_registry()` — registers Atlas and Rfam providers
4. **GUI init** — `initialize_gui()` — creates `MotifVisualizerGUI` and registers all 18 commands
5. **Welcome banner** — prints version, sources, quick start

---

## 4. Command Reference

All 18 commands are registered in `gui.py` via `cmd.extend()`.

### Loading & Data

#### `rmv_fetch <PDB_ID> [cif_use_auth=0] [bg_color=COLOR]`

Downloads and loads a PDB/mmCIF structure. Does NOT fetch motif data.

**Implementation:** `fetch_raw_pdb()` → `gui.fetch_raw_pdb()` in `gui.py`

**Key behavior:**
- Regex-parses `cif_use_auth=` and `bg_color=` from raw input string (PyMOL space-separation workaround)
- Validates PDB ID: exactly 4 alphanumeric characters
- Sets `cmd.set("cif_use_auth", val)` before `cmd.fetch()`
- If `cif_use_auth=0`: calls `_build_auth_label_chain_mapping()` to parse CIF `_atom_site` loop
- Stores `loaded_pdb`, `loaded_pdb_id`, `auth_to_label_map` on GUI object
- Clears previously loaded motifs

**Example:**
```
rmv_fetch 1S72
rmv_fetch 1S72 cif_use_auth=0
rmv_fetch 1S72, bg_color=white
```

---

#### `rmv_load_motif`

Fetches motif data from the currently selected source for the loaded PDB.

**Implementation:** `load_motif_data()` → dispatches to `fetch_motif_data_action()` or `load_user_annotations_action()`

**Key behavior:**
- Requires both `loaded_pdb_id` and `current_source_mode` to be set
- For local/web sources: calls `fetch_motif_data_action(pdb_id)` which uses `source_selector`
- For user sources: calls `load_user_annotations_action(tool, pdb_id)`
- Applies `auth_to_label_map` chain remapping when `cif_use_auth=0`

**Example:**
```
rmv_load_motif
```

---

#### `rmv_load <PDB_ID> [, bg_color=COLOR] [, database=atlas|rfam]`

Legacy one-step command: loads structure AND fetches motifs from previously selected source.

**Implementation:** `load_structure()` → `gui.load_structure_action()`

**Example:**
```
rmv_load 1S72
rmv_load 1S72, database=atlas, bg_color=white
```

---

#### `rmv_refresh [PDB_ID]`

Force-refreshes motif data from API sources (bypasses 30-day cache).

**Implementation:** `refresh_motifs()` → `gui.refresh_motifs_action()`

**Example:**
```
rmv_refresh
rmv_refresh 4V9F
```

---

### Source Selection

#### `rmv_db <N> [N ...] [on|off] [MOTIF P_VALUE ...] [/path/to/data]`

Sets the active data source by ID number (1-7). Supports multi-source combine, P-value filtering, and custom data paths.

**Implementation:** `select_database()` → `gui._handle_source_by_id()` / `gui._handle_combine_sources()`

**Source IDs:**
| ID | Provider | Type |
|----|----------|------|
| 1 | RNA 3D Atlas | Local |
| 2 | Rfam | Local |
| 3 | BGSU RNA 3D Hub | Web API |
| 4 | Rfam API | Web API |
| 5 | FR3D | User annotations |
| 6 | RNAMotifScan (RMS) | User annotations |
| 7 | RNAMotifScanX (RMSX) | User annotations |

**Multi-source:**
```
rmv_db 1 3               # Combine Atlas + BGSU
rmv_db 1 3 4             # Combine three sources
```

**P-value filtering (RMS/RMSX only):**
```
rmv_db 6 off                          # Disable filtering
rmv_db 6 on                           # Enable filtering
rmv_db 6 SARCIN-RICIN 0.01            # Custom P-value threshold
rmv_db 7 C-LOOP_CONSENSUS 0.05        # RMSX custom threshold
```

**Custom data path (sources 5-7):**
```
rmv_db 5 /path/to/fr3d/data           # FR3D with custom directory
rmv_db 6 ~/my_rms_data                # RMS with home-relative path
rmv_db 7 /path/to/rmsx/data           # RMSX with custom directory
```

**Info subcommand (via rmv_source):**
```
rmv_source info              # Show currently active source
rmv_source info 3            # Detailed info about BGSU source
```

---

#### `rmv_source info [N]`

Shows currently active source info, or detailed info about a specific source by ID.

**Implementation:** `set_source(mode='info')` → `gui._handle_source_info_command()` / `gui._print_active_source_info()`

Without an ID: shows the currently active source with its status, filtering settings, and loaded PDB.
With an ID: shows detailed info for that specific source.

---

#### `rmv_sources`

Lists all 7 available data sources with descriptions and coverage.

**Implementation:** `list_sources()` → `gui.print_sources()`

---

### Visualization

#### `rmv_show <TYPE> [<INSTANCE_NO>]`

Highlights and colors a motif type on the loaded structure. If an instance number
is provided, zooms to that specific instance and creates an individual PyMOL object.

**Implementation:** `show_motif()` → `_resolve_motif_type_and_instance()` → `VisualizationManager.show_motif_type()` or `.show_motif_instance()`

**Key behavior:**
- Uses `_resolve_motif_type_and_instance()` to handle multi-word motif names (e.g., "4-WAY JUNCTION (J4)")
- Creates PyMOL objects with source suffix: `HL_ALL_S3`, `HL_1_S3`
- Colors motif residues using `colors.py` definitions
- Sets non-motif residues to `NON_MOTIF_COLOR` (gray80)
- With instance number: creates separate object, zooms camera, prints residue details

**Example:**
```
rmv_show HL              # Show all hairpin loops
rmv_show GNRA 1          # Zoom to GNRA instance #1
rmv_show HL 3            # Zoom to hairpin loop instance #3
rmv_show 4-WAY JUNCTION (J4)    # Multi-word motif type
```

---

#### `rmv_show ALL`

Resets the view to show all loaded motifs on the gray backbone.

**Implementation:** `show_all()` → `VisualizationManager.show_all_motifs()`

---

#### `rmv_toggle <TYPE> on|off`

Toggles visibility of a motif type's PyMOL objects.

**Implementation:** `toggle_motif()` → `gui.toggle_motif_action()`

**Example:**
```
rmv_toggle HL off
rmv_toggle HL on
```

---

#### `rmv_bg_color <COLOR>`

Changes the color of non-motif residues (the "background" backbone).

**Implementation:** `set_bg_color()` → `gui.set_background_color()`

**Example:**
```
rmv_bg_color white
rmv_bg_color lightgray
rmv_bg_color gray80       # Default
```

---

#### `rmv_color <TYPE> <COLOR>`

Changes the color of a specific motif type.

**Implementation:** `set_motif_color()` → `colors.set_custom_motif_color()` → re-applies via `set_motif_color_in_pymol()`

**Example:**
```
rmv_color HL blue
rmv_color GNRA red
```

---

#### `rmv_colors`

Prints the color legend for all loaded (or default) motif types.

**Implementation:** `show_colors()` → `colors.print_color_legend()`

---

### Information

#### `rmv_summary [TYPE] [INSTANCE_NO]`

Prints motif information to the console (no rendering).

**Implementation:** `motif_summary()` → dispatches to:
- No args: `gui.print_motif_summary()` — summary table of all types
- TYPE only: `gui.show_motif_summary_for_type()` — instance table for one type
- TYPE + NO: `gui.show_motif_instance_summary()` — residue details for one instance

**Note:** Nucleotide columns are hidden from summary output.

**Example:**
```
rmv_summary                   # All motif types table
rmv_summary HL                # All HL instances
rmv_summary SARCIN-RICIN 1    # Instance #1 details
```

---

#### `rmv_source info [N]`

Shows the currently active source (no args) or detailed info about source N.

**Implementation:** `set_source()` → `gui._handle_source_info_command()` → `_print_active_source_info()` or `_print_single_source_info()`

---

#### `rmv_reset`

Deletes all PyMOL objects and resets the plugin to default state (source, PDB, colors, filters, chain mode).

**Implementation:** `reset_plugin()` → `cmd.delete('all')` + resets all `gui.*` state attributes

---

#### `rmv_chains [structure_name]`

Shows chain ID diagnostic information.

**Implementation:** `show_chain_diagnostics()` → reads `gui.cif_use_auth`, calls `cmd.get_chains()`

**Example:**
```
rmv_chains
rmv_chains 1s72
```

Output:
```
Structure: 1S72  |  cif_use_auth = 0 (label_asym_id)  |  Chains: 293
Label chains:  A AA AB AC ...
```

---

#### `rmv_help`

Prints the full command reference box.

**Implementation:** `show_help()` → `gui.print_help()`

---

### Save & Export

#### `rmv_save <ALL|TYPE|TYPE NO|current> [representation] [filename]`

Saves motif instance images to disk.

**Implementation:** `save_motif_images()` → dispatches to:
- `ALL`: `gui.save_all_motif_images_action(representation)`
- `TYPE`: `gui.save_motif_type_images_action(type, representation)`
- `TYPE NO`: `gui.save_motif_instance_by_id_action(type, no, representation)`
- `current`: `gui.save_current_view_action(filename)` — 2400×1800, 300 DPI

**Representations:** `cartoon` (default), `sticks`, `spheres`, `ribbon`, `lines`, `licorice`, `surface`, `cartoon+sticks`

**Output directory:** `motif_images/<pdb_id>/<MOTIF_TYPE>/`

**Example:**
```
rmv_save ALL                     # All motifs, cartoon
rmv_save ALL sticks              # All motifs, sticks
rmv_save HL                      # All HL instances, cartoon
rmv_save HL 3 spheres            # HL instance 3, spheres
rmv_save current                 # Current view, auto filename
rmv_save current my_view.png     # Current view, custom filename
```

---

### User Annotations

#### `rmv_user <TOOL> <PDB_ID>`

Legacy command to load user annotations directly (before `rmv_source` was available).

**Implementation:** `load_user_annotations()` → `gui.load_user_annotations_action()`

**Example:**
```
rmv_user fr3d 1S72
rmv_user rnamotifscan 1A00
rmv_user list                    # Show available annotation files
```

> **Note:** Prefer using `rmv_db 5/6/7` + `rmv_load_motif` instead.

---

## 5. Data Sources & Providers

### Provider Architecture

All providers inherit from `BaseProvider` (in `base_provider.py`):

```python
class BaseProvider(ABC):
    @abstractmethod
    def get_motifs(self, pdb_id: str) -> List[MotifType]: ...
    
    @abstractmethod
    def get_available_pdb_ids(self) -> List[str]: ...
    
    @abstractmethod
    def get_available_motif_types(self) -> List[str]: ...
```

### Core Data Types

```python
@dataclass
class ResidueSpec:
    chain: str              # Chain ID (e.g., 'A')
    number: int             # Residue sequence number
    nucleotide: str = ''    # One-letter code (A, U, G, C)

@dataclass
class MotifInstance:
    residues: List[ResidueSpec]
    annotation: str = ''    # Optional label
    score: float = 0.0      # P-value for RMS/RMSX

@dataclass
class MotifType:
    name: str               # e.g., 'HL', 'GNRA', 'SARCIN-RICIN'
    instances: List[MotifInstance]
```

### Source 1 — RNA 3D Atlas (Local)

- **File:** `atlas_provider.py`
- **Data:** Bundled JSON files in `motif_database/`
- **Coverage:** 759 PDB structures
- **Motif types:** HL, IL, J3, J4, J5, J6, J7

### Source 2 — Rfam (Local)

- **File:** `rfam_provider.py`
- **Data:** Bundled Stockholm alignment files in `motif_database/`
- **Coverage:** 173 PDB structures
- **Motif types:** GNRA, UNCG, CUYG, K-TURN, T-LOOP, C-LOOP, U-TURN, SARCIN-RICIN, TANDEM-GA, etc. (19 types)

### Source 3 — BGSU RNA 3D Hub (Web API)

- **File:** `bgsu_api_provider.py`
- **Strategy:** Hybrid HTML scraping + CSV fallback
  1. Scrapes `http://rna.bgsu.edu/rna3dhub/nrlist` for loop annotations
  2. Falls back to CSV download if HTML parsing fails
- **Coverage:** ~3000+ PDB structures
- **Cache:** 30 days via `cache_manager.py`

### Source 4 — Rfam API (Web)

- **File:** `rfam_api_provider.py`
- **Endpoint:** Rfam REST API
- **Coverage:** All Rfam-annotated motif families
- **Cache:** 30 days

### Sources 5-7 — User Annotations

- **File:** `user_annotations/user_provider.py` + `user_annotations/converters.py`
- **Source 5 (FR3D):** Parses FR3D output format
- **Source 6 (RMS):** Parses RNAMotifScan result files with P-value filtering
- **Source 7 (RMSX):** Parses RNAMotifScanX result files with P-value filtering

**File location:** `database/user_annotations/{fr3d,RNAMotifScan,RNAMotifScanX}/`

**RMS/RMSX directory structure:**
```
RNAMotifScan/
├── c_loop/
│   └── Res_1s72          # Result file for PDB 1S72
├── sarcin_ricin/
│   └── Res_1s72
├── k_turn/
│   └── Res_1s72
└── ...
```

---

## 6. Chain ID System

The plugin implements a **4-layer chain ID handling system** to ensure chain IDs are consistent between the PDB structure in PyMOL and the motif annotation data.

### Layer 1 — Startup Lock (`plugin.py`)

```python
cmd.set("cif_use_auth", 1)
```

Sets the default chain ID convention to `auth_asym_id` at plugin startup.

### Layer 2 — Fetch-Time Override (`gui.py` → `fetch_raw_pdb`)

When `cif_use_auth=0` is specified:
```python
cmd.set("cif_use_auth", 0)
gui.cif_use_auth = 0
```

### Layer 3 — CIF File Parsing (`gui.py` → `_build_auth_label_chain_mapping`)

When `cif_use_auth=0`, the plugin parses the CIF file `_atom_site` loop to build a mapping:

```python
{auth_asym_id: label_asym_id}  # e.g., {'0': 'A', '9': 'B'}
```

This is stored in `gui.auth_to_label_map` and used during motif data loading to remap residue chain IDs.

### Layer 4 — Runtime Diagnostics (`rmv_chains`)

Displays current chain mode and loaded chains for verification.

### Why This Matters

Motif databases (BGSU, Atlas, Rfam) use **auth_asym_id** chain IDs. When PyMOL loads with `cif_use_auth=0`, it uses **label_asym_id** as the `chain` property. Without the mapping, motif selections would target wrong chains.

---

## 7. Multi-Source Pipeline

When combining sources (e.g., `rmv_db 1 3`):

### Step 1 — Fetch

Each source independently fetches motifs for the PDB:
```
Atlas → [HL(35), IL(19), J3(18), ...]
BGSU  → [HL(42), IL(23), J3(21), GNRA(15), SARCIN-RICIN(8), ...]
```

### Step 2 — Enrich (`homolog_enricher.py`)

Generic motif names are enriched using NR homolog representative lookup:
```
Atlas HL_345 → matches BGSU GNRA_123 (same residues) → rename to GNRA
```

Uses `nrlist_4.24_all.csv` for representative set lookup.

### Step 3 — Cascade Merge (`cascade_merger.py`)

Sources are merged right-to-left (later sources have higher priority):
```
merge(Atlas, BGSU) = Atlas ∪ BGSU - duplicates
```

**Deduplication:** Jaccard similarity ≥ 0.60 on residue sets = duplicate. The instance from the higher-priority (right-most) source is kept.

### Step 4 — Store

Merged motifs are stored in `VisualizationManager.motif_loader.loaded_motifs` as a dict:
```python
{
    'HL': {'count': 42, 'motif_details': [...], 'structure_name': '1s72', ...},
    'GNRA': {'count': 15, 'motif_details': [...], ...},
    ...
}
```

---

## 8. Color System

### Color Definitions (`colors.py`)

Colors are defined as RGB tuples normalized to 0–1:
```python
MOTIF_COLORS = {
    'HL': (1.0, 0.0, 0.0),      # Red
    'IL': (0.0, 1.0, 1.0),      # Cyan
    'J3': (1.0, 1.0, 0.0),      # Yellow
    'GNRA': (0.0, 0.8, 0.4),    # Teal green
    ...
}
```

### Fallback Color

Any motif type not in `MOTIF_COLORS` gets `DEFAULT_COLOR = (1.0, 0.5, 0.0)` (bright orange).

### Custom Colors

Users can override colors at runtime via `rmv_color`. Custom colors are stored in `CUSTOM_COLORS` dict and take precedence over `MOTIF_COLORS`.

### Background Color

Non-motif residues are colored `NON_MOTIF_COLOR = 'gray80'`. Changeable via `rmv_bg_color`.

---

## 9. Image Export

### Image Saver (`image_saver.py`)

The `ImageSaver` class handles all PNG export:

- **Instance images:** Renders each motif instance in isolation (no background structure)
  - Default size: 800×600
  - Representations: cartoon, sticks, spheres, ribbon, lines, licorice, surface, cartoon+sticks
- **Current view:** Captures the PyMOL viewport as-is
  - Size: 2400×1800, 300 DPI (high-res)

### Output Folder

```
motif_images/
└── <pdb_id>/
    ├── <MOTIF_TYPE>/
    │   ├── <TYPE>_instance_1.png
    │   ├── <TYPE>_instance_2.png
    │   └── ...
    └── current_view_<timestamp>.png
```

---

## 10. Caching

### Cache Manager (`cache_manager.py`)

- **Location:** `~/.rna_motif_visualizer_cache/`
- **Expiry:** 30 days (configurable via `CachePolicy.cache_days`)
- **Scope:** API responses from BGSU (source 3) and Rfam API (source 4)
- **Bypass:** `rmv_refresh` sets `FreshnessPolicy.FORCE_REFRESH`

### Cache Key Format

Files are stored with a hash of the PDB ID + source identifier.

---

## 11. Adding a New Data Source

To add a new data source (e.g., "Source 8 — MyDB"):

### Step 1 — Create Provider

Create `database/mydb_provider.py`:

```python
from .base_provider import BaseProvider, MotifType, MotifInstance, ResidueSpec

class MyDBProvider(BaseProvider):
    def get_motifs(self, pdb_id: str) -> list:
        # Fetch/parse motif data for pdb_id
        # Return list of MotifType objects
        ...
    
    def get_available_pdb_ids(self) -> list:
        return [...]
    
    def get_available_motif_types(self) -> list:
        return [...]
```

### Step 2 — Register in SOURCE_ID_MAP

In `database/config.py`, add:

```python
SOURCE_ID_MAP[8] = {
    'name': 'MyDB',
    'type': 'web',       # or 'local' or 'user'
    'category': 'ONLINE SOURCES',
    'subtype': 'mydb',
    'description': 'My custom database',
    'coverage': 'N PDB structures',
    'mode': 'web',
    'command': 'rmv_db 8',
}
```

### Step 3 — Wire into Source Selector

In `database/source_selector.py`, add routing for the new source subtype.

### Step 4 — Register Provider

In `database/registry.py`, register the provider so it's discovered during initialization.

### Step 5 — Add Color Support

Add any new motif type names to `MOTIF_COLORS` in `colors.py`. Unknown types fall back to orange.

---

## 12. Key Classes & Methods

### `MotifVisualizerGUI` (`gui.py`)

The central state object. Key attributes:

| Attribute | Type | Purpose |
|-----------|------|---------|
| `loaded_pdb` | `str` | PyMOL object name of loaded structure |
| `loaded_pdb_id` | `str` | PDB ID (uppercase, e.g., "1S72") |
| `cif_use_auth` | `int` | 1 = auth_asym_id, 0 = label_asym_id |
| `auth_to_label_map` | `dict` | {auth_chain: label_chain} mapping |
| `current_source_mode` | `str` | 'local', 'web', 'user', 'combine' |
| `current_source_id` | `int\|str` | Numeric source ID (1-7) or combined (e.g., '1_3') |
| `combined_source_ids` | `list` | Source IDs when combining |
| `user_rms_filtering_enabled` | `bool` | RMS P-value filtering on/off |
| `user_rmsx_filtering_enabled` | `bool` | RMSX P-value filtering on/off |
| `user_rms_custom_pvalues` | `dict` | {motif_name: p_value} overrides |
| `user_rmsx_custom_pvalues` | `dict` | {motif_name: p_value} overrides |
| `user_data_path` | `str\|None` | Custom data directory for FR3D/RMS/RMSX |
| `viz_manager` | `VisualizationManager` | Manages loading + rendering |

### `VisualizationManager` (`loader.py`)

Coordinates structure loading, motif loading, and visualization:

| Method | Purpose |
|--------|---------|
| `show_motif_type(type)` | Render all instances of a motif type |
| `show_motif_instance(type, no)` | Render + zoom to specific instance |
| `show_all_motifs()` | Reset to default colored view |
| `get_structure_info()` | Returns loaded PDB info + motif counts |

### `_build_auth_label_chain_mapping(pdb_id)` (`gui.py`)

Parses CIF file `_atom_site` loop to extract auth→label chain mapping. Used when `cif_use_auth=0`.

**Algorithm:**
1. Find CIF file in PyMOL's `fetch_path`
2. Locate `_atom_site.auth_asym_id` and `_atom_site.label_asym_id` column indices
3. Read data rows, extract unique (auth, label) pairs
4. Return `{auth: label}` dict

### `_resolve_motif_type_and_instance(full_arg, instance_arg)`

Handles multi-word motif type names (e.g., "4-WAY JUNCTION (J4) 1"):
1. Checks if args match a loaded motif type exactly
2. Tries splitting the last token as an instance number
3. Returns `(motif_type, instance_no_or_None)`

---

## Conventions

- **PDB IDs** are stored uppercase (`loaded_pdb_id`) but PyMOL object names are lowercase (`loaded_pdb`)
- **Source suffixes** (e.g., `_S3`) are appended to PyMOL object names to distinguish sources
- **Motif type names** are always uppercase internally (e.g., `HL`, `GNRA`, `SARCIN-RICIN`)
- **Colors** use both underscore and hyphen aliases (e.g., `SARCIN_RICIN_1` and `SARCIN-RICIN-1`)
- **Chain ID convention** defaults to `auth_asym_id` (cif_use_auth=1)

---

*RNA Motif Visualizer — CBB LAB @Rakib Hasan Rahad*
