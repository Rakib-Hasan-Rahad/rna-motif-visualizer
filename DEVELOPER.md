# RSMViewer — Developer Guide

Technical reference for developers working on the RSMViewer PyMOL plugin.

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
├── alignment.py           Medoid superimposition pipeline (rmv_super / rmv_align)
├── colors.py              90+ motif color definitions + custom color support
├── image_saver.py         PNG export with 8 representations
├── structure_exporter.py  mmCIF export (original coordinates from disk)
├── database/
│   ├── config.py          SOURCE_ID_MAP (8 sources), SourceMode, PluginConfig
│   ├── base_provider.py   ResidueSpec, MotifInstance, MotifType, BaseProvider ABC
│   ├── registry.py        DatabaseRegistry — lazily loads providers
│   ├── atlas_provider.py  Atlas JSON provider
│   ├── rfam_provider.py   Rfam Stockholm provider
│   ├── bgsu_api_provider.py  Hybrid HTML scraping + CSV fallback (~3000+ PDBs)
│   ├── rfam_api_provider.py  Rfam API (34 motif families, RM00001–RM00034)
│   ├── source_selector.py  Smart source selection with fallback chain
│   ├── source_registry.py  Source registry
│   ├── cascade_merger.py   Category-aware merge with Jaccard dedup (≥60%)
│   ├── homolog_enricher.py NR representative lookup for semantic enrichment
│   ├── cache_manager.py    30-day disk cache at ~/.rsmviewer_cache/
│   ├── converters.py       Format converters for provider outputs
│   ├── representative_set.py NR list loader
│   ├── nrlist_4.24_all.csv   BGSU NR representative list
│   └── user_annotations/
│       ├── user_provider.py  FR3D/RMS/RMSX/NoBIAS annotation loader
│       └── converters.py     User annotation format parsers
└── utils/
    ├── logger.py          PluginLogger with colored PyMOL console output
    ├── parser.py          PDB ID + selection string parsers
    └── selectors.py       3-layer chain ID protection for PyMOL selections
```

### Data Flow

```
rmv_fetch <PDB>  →  PyMOL cmd.fetch() / cmd.load()
                     →  store loaded_pdb / loaded_pdb_id
                     →  parse CIF for auth→label chain map (if cif_use_auth=0)

rmv_db <N>       →  set source mode + provider config in GUI state

rmv_load_motif   →  dispatch to:
                     ├── Single source (local/web):
                     │   └── fetch_motif_data_action()
                     │       └── source_selector → provider.get_motifs() → store
                     ├── User source (5–8):
                     │   └── load_user_annotations_action()
                     │       └── user_provider.load_annotations() → parse → store
                     └── Combine mode (multiple sources):
                         └── _load_combined_motifs()
                             └── fetch each → enrich → stamp → dedup → cascade merge → store

rmv_show <TYPE>  →  VisualizationManager.show_motif_type()
                     └── create PyMOL objects + color selections

rmv_view <TYPE>  →  gui.view_motif_action()
                     └── color residues in-place on structure (no objects)

rmv_super <TYPE> →  alignment.py → MedoidSuperimposer
                     └── pairwise RMSD matrix → medoid → cmd.super all onto medoid

rmv_save <TYPE>  →  ImageSaver.save_motif_images()
                     └── render + ray + png for each instance

rmv_save <TYPE> cif  →  StructureExporter.export_instance()
                     └── parse original CIF → filter _atom_site → write mmCIF
```

---

## 2. Project Structure

### Source Code Files

| File | Lines | Purpose |
|------|-------|---------|
| `gui.py` | ~4260 | Main GUI class, 22 command registrations (20 direct + 2 from alignment), state management |
| `loader.py` | ~2060 | StructureLoader, UnifiedMotifLoader, VisualizationManager |
| `alignment.py` | ~990 | Medoid superimposition pipeline (rmv_super / rmv_align) |
| `image_saver.py` | ~580 | PNG export for individual motif instances + current view |
| `structure_exporter.py` | ~520 | mmCIF export — extracts original coordinates from disk CIF |
| `colors.py` | ~420 | MOTIF_COLORS dict (90+ entries), custom overrides, dynamic pool, PyMOL color application |
| `plugin.py` | ~120 | Entry point, cif_use_auth lock, welcome banner |
| `__init__.py` | ~43 | Package metadata (version 1.0.0), lazy imports |

### Database Module

| File | Lines | Purpose |
|------|-------|---------|
| `config.py` | ~247 | SOURCE_ID_MAP (8 entries), SourceMode enum, PluginConfig dataclass |
| `base_provider.py` | ~362 | ABC for all providers: ResidueSpec, MotifInstance, MotifType, BaseProvider |
| `registry.py` | ~302 | DatabaseRegistry — discovers and registers providers |
| `atlas_provider.py` | ~278 | Parses bundled Atlas JSON files (7 motif types: HL, IL, J3–J7) |
| `rfam_provider.py` | ~251 | Parses bundled Rfam Stockholm/SEED files (19 motif types) |
| `bgsu_api_provider.py` | ~714 | Hybrid: HTML scraping from rna.bgsu.edu + CSV fallback for loop data |
| `rfam_api_provider.py` | ~346 | REST API calls to Rfam for 34 motif family annotations |
| `source_selector.py` | ~301 | Routes source selection to appropriate provider(s) |
| `source_registry.py` | ~141 | Source registry |
| `cascade_merger.py` | ~527 | Merges motifs from multiple sources with Jaccard deduplication |
| `homolog_enricher.py` | ~463 | Enriches generic motif names using NR homolog representatives |
| `cache_manager.py` | ~405 | Disk cache with 30-day expiry, version 2.1, auto-invalidation |
| `converters.py` | ~499 | Converts provider-specific output to unified MotifInstance format |
| `representative_set.py` | ~221 | Loads BGSU NR representative list for homolog lookup |

### User Annotations

| File | Lines | Purpose |
|------|-------|---------|
| `user_provider.py` | ~552 | Unified provider for FR3D, RMS, RMSX, NoBIAS |
| `converters.py` | ~787 | FR3D CSV parser, RMS tab parser, RMSX log parser, NoBIAS parser |

### Utils Module

| File | Lines | Purpose |
|------|-------|---------|
| `logger.py` | ~82 | `PluginLogger` — colored console output (info/warning/error/success/debug) |
| `parser.py` | ~147 | Parses PDB IDs, file paths, selection strings |
| `selectors.py` | ~366 | 3-layer chain ID protection: builds safe PyMOL selection strings |

---

## 3. Initialization Flow

When PyMOL loads the plugin (`__init_plugin__` in `plugin.py`):

1. **Logger setup** — `initialize_logger(use_pymol_console=True)`
2. **Welcome banner** — prints ASCII box with version (1.0.0), available sources, and quick start guide
3. **Chain ID lock** — `cmd.set("cif_use_auth", 1)` — ensures auth_asym_id by default
4. **Registry init** — `initialize_registry()` — registers Atlas and Rfam providers
5. **GUI init** — `initialize_gui()` — creates `MotifVisualizerGUI`, registers all 22 commands via `cmd.extend()`, and calls `register_alignment_commands()` for `rmv_super`/`rmv_align`

---

## 4. Command Reference

All commands are registered via `cmd.extend()`. 20 are registered directly in `gui.py`, 2 are registered in `alignment.py` via `register_alignment_commands()`.

### Loading & Data

#### `rmv_fetch <PDB_ID> [, cif_use_auth=0|1] [, bg_color=COLOR]`

Downloads and loads a PDB/mmCIF structure. Does NOT fetch motif data.

**Implementation:** `fetch_raw_pdb()` in `gui.py`

**Key behavior:**
- Accepts PDB IDs (4 alphanumeric characters) or local file paths (`.pdb`, `.cif`, `.mmcif`, `.pdb.gz`, `.cif.gz`, `.ent`, `.ent.gz`)
- Local paths detected by: path separators, `~` prefix, `.` prefix, or file extensions
- Regex-parses `cif_use_auth=` and `bg_color=` from raw input (PyMOL space-separation workaround)
- `cif_use_auth` accepts: `0`/`off`/`false`/`label` or `1`/`on`/`true`/`auth`
- Sets `cmd.set("cif_use_auth", val)` before `cmd.fetch()` / `cmd.load()`
- If `cif_use_auth=0`: calls `_build_auth_label_chain_mapping()` to parse CIF `_atom_site` loop
- Stores `loaded_pdb`, `loaded_pdb_id`, `auth_to_label_map` on GUI object
- When switching to a different PDB, clears stale motif data and `loaded_sources`
- Reports chains found (up to 20 displayed, remainder counted)

```
rmv_fetch 1S72
rmv_fetch 1S72, cif_use_auth=0
rmv_fetch 1S72, bg_color=white
rmv_fetch /path/to/local.cif
rmv_fetch ~/structures/1s72.pdb
```

---

#### `rmv_load_motif`

Fetches motif data from the currently selected source for the loaded PDB. Takes no arguments.

**Implementation:** `load_motif_data()` → dispatches to:
- `fetch_motif_data_action()` for curated sources (1–4)
- `load_user_annotations_action()` for user sources (5–8)
- `_load_combined_motifs()` for combine mode

**Prerequisites:** A PDB must be loaded (`rmv_fetch`) and a source selected (`rmv_db`).

---

#### `rmv_db <N> [N ...] [on|off] [MOTIF P_VALUE ...] [/path/to/data] [, jaccard_threshold=VALUE]`

Sets the active data source. Supports multi-source combine, P-value filtering, and custom data paths.

**Implementation:** `select_database()` → `_handle_source_by_id()` / `_handle_combine_sources()`

**Source IDs:**

| ID | Provider | Type |
|----|----------|------|
| 1 | RNA 3D Atlas | Local |
| 2 | Rfam | Local |
| 3 | BGSU RNA 3D Hub | Web API |
| 4 | Rfam API | Web API |
| 5 | FR3D | User annotations |
| 6 | RNAMotifScan (RMS) | User annotations + filtering |
| 7 | RNAMotifScanX (RMSX) | User annotations + filtering |
| 8 | NoBIAS | User annotations + filtering |

**Multi-source detection:** When remaining args after the first source ID contain another valid source ID, combine mode is triggered.

**Jaccard threshold parsing:** Values >1.0 treated as percentages (e.g., `80` → `0.80`). Trailing `%` stripped. Default: `0.60`.

**Custom paths:** Detected by presence of `/` or `\`. Stored per-source in `self.user_data_paths: Dict[int, str]`.

```
rmv_db 3                                    # Single source
rmv_db 8 7                                  # Combine NoBIAS + RMSX
rmv_db 8 7, jaccard_threshold=0.80          # Custom threshold
rmv_db 6 off                                # Disable filtering
rmv_db 6 SARCIN-RICIN 0.01                  # Custom P-value
rmv_db 7 /path/to/rmsx/data                 # Custom data path
```

---

#### `rmv_source info [N]`

Shows currently active source info (no args) or detailed info about source N.

**Implementation:** `set_source(mode='info')` → `_handle_source_info_command()`

---

#### `rmv_sources`

Lists all 8 available data sources with descriptions and coverage.

**Implementation:** `list_sources()` → `gui.print_sources()`

---

#### `rmv_refresh`

Force-refreshes motif data from API sources (bypasses 30-day cache).

**Implementation:** `refresh_motifs()` → `gui.refresh_motifs_action()`

---

#### `rmv_load <PDB_ID>`

**Legacy command.** Does NOT load anything — only prints a "RECOMMENDED WORKFLOW" guide directing users to `rmv_fetch` → `rmv_db` → `rmv_load_motif`.

---

### Visualization

#### `rmv_show <TYPE> [<INSTANCE_NO>] [, padding=N]`

Creates PyMOL objects for motif instances and renders them.

**Implementation:** `show_motif()` → `_resolve_motif_type_and_instance()` → `VisualizationManager.show_motif_type(padding=N)` or `.show_motif_instance(padding=N)`

**Key behavior:**
- Uses `_resolve_motif_type_and_instance()` to handle multi-word motif names (e.g., `"4-WAY JUNCTION (J4)"`)
- Creates PyMOL objects with source suffix: `HL_ALL_S3`, `HL_1_S3`
- Auto-deactivates all other PyMOL objects except the base PDB and new motif objects
- With instance number: creates separate object, zooms camera, prints residue details
- Supports comma-separated instance numbers: `rmv_show HL 1,3,5`
- Includes typo detection with "Did you mean…?" suggestions

**Source filtering (combine mode only):**

In combine mode, the last non-numeric token is checked as a source filter keyword via `_resolve_source_filter()`:

```
rmv_show K-TURN nobias       # Only NoBIAS-unique instances
rmv_show K-TURN shared       # Only shared instances
```

Supported keywords: `nobias`, `rmsx`, `rms`, `fr3d`, `rfam`, `atlas`, `bgsu`, `shared`, plus full source names.

---

#### `rmv_show ALL`

Creates PyMOL objects for every loaded motif type.

---

#### `rmv_view <TYPE> [<INSTANCE_NO>] | all | hide | all hide | <TYPE> hide`

Lightweight alternative — highlights motif residues directly on the structure **without** creating separate PyMOL objects.

**Implementation:** `view_motif()` → `gui.view_motif_action()`

- `rmv_view all` — colors all motif residues with unique type colors
- `rmv_view hide` / `rmv_view all hide` — resets all coloring to gray
- `rmv_view <TYPE> hide` — resets only that type's coloring
- `rmv_view <TYPE> <NO>` — zooms and creates a PyMOL selection

---

#### `rmv_toggle <TYPE> on|off`

Toggles visibility of a motif type's PyMOL objects.

**Implementation:** `toggle_motif()` → `gui.toggle_motif_action()`

Accepted values: `on`/`true`/`1`/`yes`/`show` or `off`/`false`/`0`/`no`/`hide`

---

#### `rmv_bg_color <COLOR>`

Changes the color of non-motif residues (default: `gray80`).

---

#### `rmv_color <TYPE> <COLOR>`

Changes the color of a specific motif type. Accepts PyMOL color names or RGB float values.

**Implementation:** `set_motif_color()` → `colors.set_custom_motif_color()` → re-applies via `set_motif_color_in_pymol()`

Custom colors take priority over predefined colors.

---

#### `rmv_colors`

Prints the color legend for all loaded (or default) motif types.

---

### Superimposition

#### `rmv_super <TYPE> [<INSTANCE_NOS>] [, <PDB_SRC1>, <PDB_SRC2>] [, padding=N]`

Medoid-based structural superimposition using `cmd.super()` (sequence-independent).

**Implementation:** `superimpose_motifs()` → `alignment.py` → `_run_medoid_pipeline()`

**Pipeline:**
1. Resolve motif name via alias table + fuzzy matching (exact → alias → reverse alias → substring)
2. Collect individual instance objects (auto-create if needed via `_batch_create_instance_objects()`)
3. Build N×N pairwise RMSD matrix using temporary copies
4. Identify medoid (instance with minimum average RMSD)
5. Superimpose all instances onto medoid
6. Color each instance uniquely (cycling 15 colors), medoid = green
7. Print formatted report with per-instance RMSD

**PDB_SRC tags:** Format `<PDB>_S<N>` (e.g., `1S72_S3`). Validated with intelligent error messages.

**Motif alias table (`MOTIF_ALIASES`):**

| User Input | Resolves To |
|------------|-------------|
| KTURN, K_TURN, KINK-TURN, KINK_TURN | K-TURN |
| CLOOP, C_LOOP | C-LOOP |
| SARCIN, SARCINRICIN, SARCIN_RICIN | SARCIN-RICIN |
| REVERSE-KTURN, REVERSE_KTURN, REVERSEKTURN, REVERSE_K_TURN | REVERSE-K-TURN |
| ELOOP, E_LOOP | E-LOOP |
| TLOOP, T_LOOP | T-LOOP |

**Resolution order:** Exact match → Forward alias → Reverse alias → Substring match

```
rmv_super KTURN                       # All K-TURN instances
rmv_super KTURN 1,3,5                 # Specific instances
rmv_super KTURN, 1S72_S3, 4V88_S3    # Cross-PDB
rmv_super KTURN, padding=3            # With flanking residues
```

---

#### `rmv_align <TYPE> [<INSTANCE_NOS>] [, <PDB_SRC1>, <PDB_SRC2>] [, padding=N]`

Same as `rmv_super` but uses `cmd.align()` (sequence-dependent). Better for closely related sequences.

---

### Information

#### `rmv_summary [TYPE] [INSTANCE_NO]`

Prints motif information to the console (no rendering).

**Implementation:** `motif_summary()` → dispatches to:
- No args: `gui.print_motif_summary()` — summary table of all types with counts
- TYPE only: `gui.show_motif_summary_for_type()` — instance table with source attribution
- TYPE + NO: `gui.show_motif_instance_summary()` — residue-level details

---

#### `rmv_chains [structure_name]`

Shows chain ID diagnostic information: structure name, `cif_use_auth` value, chain ID mode, total chain count, and all chains.

---

#### `rmv_loaded`

Lists all loaded PDB+source combination tags (e.g., `1S72_S3`, `4V88_S7`). Suggests usage with `rmv_super`/`rmv_align`.

---

#### `rmv_help`

Prints the full 22-command reference in box format.

---

### Save & Export

#### `rmv_save <ALL|TYPE|TYPE NO|current> [representation|cif] [filename]`

Saves motif instance images **or** exports motif structures as mmCIF.

**Implementation:** `save_motif_images()` → dispatches to:
- `ALL`: `gui.save_all_motif_images_action(representation)`
- `TYPE`: `gui.save_motif_type_images_action(type, representation)`
- `TYPE NO`: `gui.save_motif_instance_by_id_action(type, no, representation)`
- `current`: `gui.save_current_view_action(filename)` — 2400×1800, ~300 DPI
- `ALL cif`: `gui.export_all_motif_structures_action()`
- `TYPE cif`: `gui.export_motif_type_structures_action(type)`
- `TYPE NO cif`: `gui.export_motif_instance_by_id_action(type, no)`

**Representations (image save):** `cartoon` (default), `sticks`, `spheres`, `ribbon`, `lines`, `licorice`, `surface`, `cartoon+sticks`

**Output directories:**
- Images: `motif_images/<pdb_id>/<MOTIF_TYPE>/`
- Structures: `motif_structures/<pdb_id>/<MOTIF_TYPE>/`

**mmCIF export** extracts original coordinates from the on-disk CIF file (not PyMOL's internal coordinates). Implemented in `structure_exporter.py` → `MotifStructureExporter`.

**Why not `cmd.save()`?** PyMOL may modify coordinates slightly during loading (symmetry expansion, origin shifting). The exporter reads/writes the raw CIF text directly.

---

### User Annotations

#### `rmv_user <TOOL> <PDB_ID> | list`

Legacy command to load user annotations directly.

- `rmv_user fr3d 1S72` — Load FR3D annotations
- `rmv_user rnamotifscan 1A00` — Load RMS annotations
- `rmv_user list` — Show available annotation files

> **Preferred approach:** Use `rmv_db 5/6/7/8` + `rmv_load_motif` instead.

---

#### `rmv_reset`

Deletes all PyMOL objects (`cmd.delete('all')`) and resets all GUI state:
- Clears `loaded_pdb`, `loaded_pdb_id`, `current_source_mode`, `current_source_id`
- Resets filtering to defaults (on)
- Clears custom P-values and custom colors
- Resets `cif_use_auth` to 1
- Clears auth→label chain mapping and motif loader data

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
    score: float = 0.0      # P-value for RMS/RMSX/NoBIAS

@dataclass
class MotifType:
    name: str               # e.g., 'HL', 'GNRA', 'SARCIN-RICIN'
    instances: List[MotifInstance]
```

### Source 1 — RNA 3D Atlas (Local)

- **File:** `atlas_provider.py`
- **Data:** Bundled JSON files in `motif_database/RNA 3D motif atlas/` (e.g., `hl_4.5.json`, `il_4.5.json`)
- **Motif types:** HL, IL, J3, J4, J5, J6, J7
- **Auto-discovery:** Scans for versioned JSON files at startup

### Source 2 — Rfam (Local)

- **File:** `rfam_provider.py`
- **Data:** Bundled Stockholm/SEED alignment files in `motif_database/Rfam motif database/`
- **Motif types:** 19 named types (GNRA, UNCG, CUYG, K-TURN-1, K-TURN-2, pK-TURN, T-LOOP, C-LOOP, U-TURN, SARCIN-RICIN-1, SARCIN-RICIN-2, TANDEM-GA, etc.)

### Source 3 — BGSU RNA 3D Hub (Web API)

- **File:** `bgsu_api_provider.py`
- **Strategy:** Hybrid HTML scraping + CSV fallback
  1. Scrapes `http://rna.bgsu.edu/rna3dhub/pdb/{PDB}/motifs` for loop annotations
  2. Falls back to CSV download if HTML parsing fails
- **Coverage:** ~3000+ PDB structures
- **Cache:** 30 days via `cache_manager.py`

### Source 4 — Rfam API (Web)

- **File:** `rfam_api_provider.py`
- **Endpoint:** `https://rfam.org/motif/{RM_ID}/alignment` (Stockholm SEED format)
- **Coverage:** 34 motif families (RM00001–RM00034)
- **Cache:** 30 days

### Sources 5–8 — User Annotations

- **File:** `user_annotations/user_provider.py` + `user_annotations/converters.py`
- **Source 5 (FR3D):** Parses FR3D CSV output
- **Source 6 (RMS):** Parses RNAMotifScan tab-separated result files with P-value filtering
- **Source 7 (RMSX):** Parses RNAMotifScanX `result_*.log` files with P-value filtering
- **Source 8 (NoBIAS):** Parses NoBIAS `*_nobias.txt` files with P-value filtering (delegates to RMSX parser — same format)

**File locations (default):**
```
database/user_annotations/
├── fr3d/                    FR3D CSV files
├── RNAMotifScan/            RMS (motif-type subdirectories)
├── RNAMotifScanX/           RMSX (consensus subdirectories)
└── NoBIAS/                  NoBIAS (flat *_nobias.txt files)
```

**Custom paths stored per-source** in `gui.user_data_paths: Dict[int, str]`.

**RMSX file priority:** When multiple result files exist in a consensus directory:
1. `result_0_100_withbs.log` (highest)
2. `result_0_100.log`
3. `result_0_withbs.log`
4. `result_0.log` (lowest)

**Default P-value thresholds:**

| Motif | RMS | RMSX | NoBIAS |
|-------|-----|------|--------|
| KINK-TURN | 0.07 | 0.066 | 0.066 |
| C-LOOP | 0.04 | 0.044 | 0.044 |
| SARCIN-RICIN | 0.02 | 0.040 | 0.040 |
| REVERSE KINK-TURN | 0.14 | 0.018 | 0.018 |
| E-LOOP | 0.13 | 0.018 | 0.018 |

---

## 6. Chain ID System

The plugin implements a **4-layer chain ID handling system** to ensure consistency between PDB structures and motif annotation data.

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

Stored in `gui.auth_to_label_map` and used during motif data loading to remap residue chain IDs.

**Algorithm:**
1. Find CIF file in PyMOL's `fetch_path`
2. Locate `_atom_site.auth_asym_id` and `_atom_site.label_asym_id` column indices
3. Read data rows, extract unique (auth, label) pairs
4. Return `{auth: label}` dict

### Layer 4 — Runtime Diagnostics (`rmv_chains`)

Displays current chain mode and loaded chains for verification.

### Why This Matters

Motif databases (BGSU, Atlas, Rfam) use **auth_asym_id** chain IDs. When PyMOL loads with `cif_use_auth=0`, it uses **label_asym_id** as the `chain` property. Without the mapping, motif selections would target wrong residues/chains.

---

## 7. Multi-Source Pipeline

When combining sources (e.g., `rmv_db 8 7`):

### Step 1 — Fetch

Each source independently fetches motifs for the PDB:
```
NoBIAS → [K-TURN(6), SARCIN-RICIN(4), ...]
RMSX   → [K-TURN(5), C-LOOP(3), SARCIN-RICIN(4), ...]
```

### Step 2 — Enrich (`homolog_enricher.py`)

Generic motif names are enriched using NR homolog representative lookup:
```
Atlas HL_345 → matches BGSU GNRA_123 (same residues) → rename to GNRA
```

Uses `nrlist_4.24_all.csv` for representative set lookup. IFE format: `PDB_ID|Model|Chain` (handles multi-chain with `+`). Primary matching by `motif_group` ID; fallback via Jaccard residue similarity (threshold 0.85). Skips generic names (HL, IL, J3–J8) for enrichment.

### Step 3 — Source Stamping

Each instance is tagged with `_source_id` and `_source_label` metadata. This enables the SOURCE column in instance tables and the source attribution report in `rmv_summary`.

### Step 4 — Within-Source Deduplication

Exact duplicates within the same source are removed. Two instances are considered duplicates if they have the same set of `(chain, residue_number)` pairs.

### Step 5 — Cascade Merge (`cascade_merger.py`)

Sources are merged right-to-left with Jaccard deduplication:

**Key parameters:**
- Default Jaccard threshold: `0.60` (60% residue overlap = duplicate)
- Category-aware: only compares motifs within the same base category
- `MOTIF_CANONICAL_MAP` harmonizes variant names (KTURN → K-TURN, CLOOP → C-LOOP, etc.)
- Higher-priority source version kept on overlap

### Step 6 — Cross-Source Attribution

`_annotate_overlap()` adds `_also_found_in` metadata for instances found in multiple sources. `_deduplicate_subsets()` performs a final pass removing subset instances (asymmetric containment).

### Step 7 — Source Filter Resolution

In combine mode, `_resolve_source_filter()` (`gui.py`) categorizes merged instances as **unique** (single `_source_label`) or **shared** (`_also_found_in` not empty). Keywords (nobias, rmsx, shared, etc.) resolve to lists of instance numbers for per-source rendering.

### Storage

Merged motifs stored in `VisualizationManager.motif_loader.loaded_motifs`:
```python
{
    'K-TURN': {'count': 8, 'motif_details': [...], 'structure_name': '1s72', ...},
    'SARCIN-RICIN': {'count': 4, 'motif_details': [...], ...},
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

90+ entries including underscore and hyphen aliases (e.g., both `SARCIN_RICIN` and `SARCIN-RICIN`).

### Color Priority

1. **Custom** — user-set via `rmv_color` (stored in `CUSTOM_COLORS` dict)
2. **Predefined** — from `MOTIF_COLORS`
3. **Dynamic pool** — 20 visually distinct colors assigned at runtime (`_DYNAMIC_COLOR_POOL`)
4. **Hash** — MD5 hash-based deterministic color when pool exhausted

### Constants

- `NON_MOTIF_COLOR = 'gray80'` — background/non-motif residue color
- `DEFAULT_COLOR = (1.0, 0.5, 0.0)` — bright orange for unknown types

---

## 9. Image Export

### Image Saver (`image_saver.py`)

The `ImageSaver` class handles all PNG export:

- **Instance images:** Renders each motif instance in isolation (no background structure)
  - Default size: 800×600
  - Representations: cartoon, sticks, spheres, ribbon, lines, licorice, surface, cartoon+sticks
- **Current view:** Captures the PyMOL viewport as-is
  - Size: 2400×1800, ~300 DPI

### Structure Exporter (`structure_exporter.py`)

The `MotifStructureExporter` class exports motif instances as standalone mmCIF files:

1. Locates the **original CIF file** on disk via PyMOL's `fetch_path`
2. Parses `_atom_site` column headers to find `auth_asym_id` and `auth_seq_id` indices
3. Filters atom records to only those matching the motif's (chain, residue) pairs
4. Copies all metadata blocks (`_cell`, `_symmetry`, `_entity`, etc.) from source
5. Writes a self-contained `.cif` file loadable in PyMOL or any molecular viewer

### Output Folders

```
motif_images/
└── <pdb_id>/
    ├── <MOTIF_TYPE>/
    │   ├── <TYPE>-<NO>-<CHAIN>_<RESIDUES>.png
    │   └── ...
    └── ...

motif_structures/
└── <pdb_id>/
    ├── <MOTIF_TYPE>/
    │   ├── <TYPE>-<NO>-<CHAIN>_<RESIDUES>.cif
    │   └── ...
    └── ...
```

---

## 10. Caching

### Cache Manager (`cache_manager.py`)

- **Location:** `~/.rsmviewer_cache/`
- **Expiry:** 30 days
- **Version:** `CACHE_VERSION = "2.1"` — auto-invalidates old caches
- **Scope:** API responses from BGSU (source 3) and Rfam API (source 4)
- **Bypass:** `rmv_refresh` clears cache and re-fetches

---

## 11. Adding a New Data Source

To add a new data source (e.g., "Source 9 — MyDB"):

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

In `database/config.py`, add entry 9 with `name`, `type`, `category`, `subtype`, `description`, `coverage`, `mode`, and `command` fields.

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
| `current_source_id` | `int\|str` | Numeric source ID (1–8) or combined (e.g., '8_7') |
| `combined_source_ids` | `list` | Source IDs when combining |
| `user_rms_filtering_enabled` | `bool` | RMS P-value filtering on/off |
| `user_rmsx_filtering_enabled` | `bool` | RMSX P-value filtering on/off |
| `user_nobias_filtering_enabled` | `bool` | NoBIAS P-value filtering on/off |
| `user_rms_custom_pvalues` | `dict` | {motif_name: p_value} overrides |
| `user_rmsx_custom_pvalues` | `dict` | {motif_name: p_value} overrides |
| `user_nobias_custom_pvalues` | `dict` | {motif_name: p_value} overrides |
| `user_data_paths` | `dict` | Per-source custom data paths: {source_id: path_str} |
| `viz_manager` | `VisualizationManager` | Manages loading + rendering |

### `VisualizationManager` (`loader.py`)

Coordinates structure loading, motif loading, and visualization:

| Method | Purpose |
|--------|---------|
| `show_motif_type(type, padding=0)` | Render all instances of a motif type |
| `show_motif_instance(type, no, padding=0)` | Render + zoom to specific instance |
| `show_all_motifs()` | Reset to default colored view |
| `get_structure_info()` | Returns loaded PDB info + motif counts |
| `_deactivate_other_objects(keep_active)` | Auto-deactivate PyMOL objects except those in `keep_active` |
| `_format_source_label(metadata)` | Format `_source_label` + `_also_found_in` for display |

### `_build_auth_label_chain_mapping(pdb_id)` (`gui.py`)

Parses CIF file `_atom_site` loop to extract auth→label chain mapping. Used when `cif_use_auth=0`.

### `_resolve_motif_type_and_instance(full_arg, instance_arg)`

Handles multi-word motif type names (e.g., "4-WAY JUNCTION (J4) 1"):
1. Checks if args match a loaded motif type exactly
2. Tries splitting the last token as an instance number
3. Returns `(motif_type, instance_no_or_None)`

### `_resolve_source_filter(keyword, combined_source_ids)`

In combine mode, resolves keywords like `nobias`, `rmsx`, `shared` to lists of instance numbers matching that source or overlap category.

---

## Conventions

- **PDB IDs** are stored uppercase (`loaded_pdb_id`) but PyMOL object names are lowercase (`loaded_pdb`)
- **Source suffixes** appended to PyMOL object names: `_S3` (single), `_S_8_7` (combined)
- **Motif type names** are uppercase internally (e.g., `HL`, `GNRA`, `SARCIN-RICIN`)
- **Color aliases** cover both underscore and hyphen variants (e.g., `SARCIN_RICIN` and `SARCIN-RICIN`)
- **Chain ID convention** defaults to `auth_asym_id` (cif_use_auth=1)

---

*RSMViewer v1.0.0 — CBB LAB KU @Rakib Hasan Rahad*
