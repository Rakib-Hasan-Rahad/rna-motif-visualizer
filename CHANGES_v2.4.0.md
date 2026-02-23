# RNA Motif Visualizer — Changes v2.4.0

## Summary

Command renaming, next-step suggestion fixes, custom data path support for user annotation sources, and nucleotide column removal from summary tables.

---

## 1. Command Renames

### `rmv_motifs` → `rmv_load_motif`

- Renamed the motif data loading command from `rmv_motifs` to `rmv_load_motif` for clarity.
- All help text, suggestions, docstrings, and error messages updated.
- Registered as `cmd.extend('rmv_load_motif', load_motif_data)`.

### `rmv_source <N>` (source selection) → `rmv_db <N>`

- Source **selection** is now done via `rmv_db <N>` (previously `rmv_source <N>`).
- The new `select_database()` wrapper function handles:
  - ID-based selection: `rmv_db 3`
  - Multi-source combine: `rmv_db 1 3`
  - Filtering control: `rmv_db 6 off`, `rmv_db 6 C-LOOP 0.05`
  - Custom data path: `rmv_db 5 /path/to/data` (new feature, see below)
  - Legacy subcommands: `rmv_db combine`, `rmv_db user`, `rmv_db local`, `rmv_db web`

### `rmv_source` merged into `rmv_source info`

- The old standalone `rmv_source` (showing current source) is merged into `rmv_source info`:
  - `rmv_source info` — show currently selected source info
  - `rmv_source info <N>` — show detailed info about source N (with RMS/RMSX filtering features etc.)
- `rmv_source` without "info" now shows a usage hint directing to `rmv_source info`.
- This is the same behavior that `rmv_source info [N]` had before — it's now the only way to use `rmv_source`.

### Command Count

Total commands remain at **17**:

| Command | Description |
|---------|-------------|
| `rmv_fetch` | Load PDB structure |
| `rmv_load_motif` | Fetch motif data from source (was `rmv_motifs`) |
| `rmv_load` | Load structure with auto-visualization |
| `rmv_db` | Select data source by ID (was `rmv_source <N>`) |
| `rmv_source info` | Show current/detailed source info (requires "info" subcommand) |
| `rmv_sources` | List all available sources |
| `rmv_show` | Visualize motifs |
| `rmv_toggle` | Toggle motif visibility |
| `rmv_summary` | Show motif summary tables |
| `rmv_save` | Save motif images |
| `rmv_colors` | Show color legend |
| `rmv_color` | Change motif color |
| `rmv_bg_color` | Change background color |
| `rmv_chains` | Chain ID diagnostics |
| `rmv_user` | Load user annotations directly |
| `rmv_refresh` | Force refresh cache |
| `rmv_reset` | Reset plugin state |
| `rmv_help` | Show command reference |

---

## 2. Next-Step Suggestion Fixes

**Problem:** After selecting a source (e.g., `rmv_db 3`), the plugin showed `rmv_summary` and `rmv_show` as next steps. Running these before loading motifs caused errors.

**Fix:** All source handler methods now only suggest `rmv_load_motif` (and `rmv_fetch` if no PDB loaded) as next steps:

- `_handle_local_source_by_id` — fixed
- `_handle_web_source_by_id` — fixed
- `_handle_user_source_by_id` — fixed
- `_handle_user_source` (legacy) — fixed
- `set_source_mode` — fixed
- `fetch_motif_data_action` — removed duplicate `rmv_summary HL` suggestion
- `load_user_annotations_action` — removed premature `rmv_summary <TYPE>` suggestion

---

## 3. Custom Data Path Support (Sources 5-7)

**New Feature:** Users can specify a custom local data directory when selecting FR3D, RMS, or RMSX sources.

```
rmv_db 5 /path/to/fr3d/data       # FR3D with custom data directory
rmv_db 6 /path/to/rms/data        # RMS with custom data directory
rmv_db 7 ~/my_rmsx_data           # RMSX with home-relative path
```

**Implementation:**
- Added `self.user_data_path` attribute to GUI class (`__init__`)
- Path detection in `_handle_user_source_by_id`: recognizes paths starting with `/`, `~`, `./`, `..`
- Validates path exists as directory; warns if not found (falls back to default)
- `_fetch_from_single_source` and `load_user_annotations_action` use `self.user_data_path` when set to create `UserAnnotationProvider` with the custom directory
- Path is displayed in status message after source selection

---

## 4. Nucleotide Column Hidden from Summary

**Change:** Nucleotide columns removed from summary display.

### `rmv_summary <TYPE>` — Instance Table

Before:
```
  NO.    CHAIN      RESIDUE RANGES                                     NUCLEOTIDES
  1      0          0:2633-2637                                        GAAAG
```

After:
```
  NO.    CHAIN      RESIDUE RANGES
  1      0          0:2633-2637
```

### `rmv_show <TYPE> <NO>` — Single Instance Detail

Before:
```
  CHAIN    RESI     NUCLEOTIDE
  0        2633     G
  0        2634     A
```

After:
```
  CHAIN    RESI
  0        2633
  0        2634
```

**Note:** The `_get_nucleotides_for_strands` function is kept intact but commented out at the call site, so it can be restored or used for PDB-based nucleotide lookup in the future.

---

## Files Modified

| File | Changes |
|------|---------|
| `rna_motif_visualizer/gui.py` | Split `set_source()` into `select_database()` + `set_source()`, renamed `rmv_motifs`→`rmv_load_motif`, renamed `rmv_source <N>`→`rmv_db <N>`, fixed all next-step suggestions, added custom data path support, updated `print_help`, `reset_plugin`, startup message, all docstrings/error messages |
| `rna_motif_visualizer/loader.py` | Hid NUCLEOTIDES column from instance table and single instance info, updated `rmv_motifs` reference to `rmv_load_motif` |
| `rna_motif_visualizer/plugin.py` | Updated docstring and startup Quick Start to use `rmv_db` and `rmv_load_motif` |
| `rna_motif_visualizer/database/config.py` | Updated all `command` fields in `SOURCE_ID_MAP` from `rmv_source N` to `rmv_db N`, including `command_with_filtering` and `command_with_custom_pvalues` |

---

## Quick Start (Updated)

```
rmv_fetch 1S72          # Load PDB structure
rmv_db 3                # Select BGSU API
rmv_load_motif          # Fetch motif data
rmv_summary             # View summary
rmv_show HL             # Render hairpin loops
```
