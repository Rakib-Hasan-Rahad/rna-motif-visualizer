# 🧬 RNA Motif Visualizer

**A PyMOL plugin for visualizing RNA structural motifs from multiple databases.**

[![Version](https://img.shields.io/badge/version-2.3.0-blue.svg)](DEVELOPER.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyMOL](https://img.shields.io/badge/PyMOL-2.x+-orange.svg)](https://pymol.org/)

<p align="center">
  <img src="images/banner.png" alt="RNA Motif Visualizer" width="700"/>
</p>

---

## What It Does

RNA Motif Visualizer loads any PDB structure into PyMOL, fetches RNA motif annotations from **7 different data sources**, and renders color-coded motifs directly on the 3D structure. It supports side-by-side comparison of annotations from multiple sources, user-uploaded results from FR3D/RMS/RMSX, and high-resolution image export.

### Use Cases

- **Visualize known RNA motifs** (hairpin loops, GNRA tetraloops, K-turns, sarcin-ricin, etc.) on any ribosomal or RNA structure
- **Compare motif annotations** from different databases to identify consensus or discrepancies
- **Validate computational results** by overlaying FR3D, RNAMotifScan, or RNAMotifScanX output on the 3D structure
- **Generate publication-quality images** of individual motif instances in multiple representations
- **Explore large RNA structures** interactively — load once, switch sources freely

---

## Features

| Feature | Description |
|---------|-------------|
| **7 Data Sources** | Atlas, Rfam, BGSU API, Rfam API, FR3D, RMS, RMSX |
| **Split Fetch Pipeline** | Load PDB first → select source → fetch motifs (fast loading) |
| **Multi-Source Combine** | Merge annotations from 2-3 sources with smart deduplication |
| **Source-Tagged Objects** | PyMOL objects tagged with source suffix (`_S3`, `_S7`) for comparison |
| **Label Chain ID Support** | `cif_use_auth=0` for annotations using label_asym_id |
| **P-Value Filtering** | Configurable thresholds for RMS/RMSX results |
| **30+ Motif Colors** | Distinct colors per motif type, fully customizable |
| **Image Export** | PNG export per-instance with 8 representation options |
| **High-Res Current View** | 2400×1800 @ 300 DPI capture of any PyMOL view |
| **30-Day API Cache** | Automatic caching of online results |
| **18 Commands** | Complete CLI interface — no GUI windows needed |

---

## Installation

### Requirements

- **PyMOL** 2.x or later (Incentive or Open-Source)
- **Python 3.8+** (bundled with PyMOL)
- Internet connection for online sources (BGSU API, Rfam API)

### Steps

1. **Download** this repository (or clone it):
   ```bash
   git clone https://github.com/your-repo/rna-motif-visualizer.git
   ```

2. **Open PyMOL** and go to:
   ```
   Plugin → Plugin Manager → Install New Plugin → Install from local file
   ```

3. **Select** the `rna_motif_visualizer` folder

4. **Restart PyMOL** — you'll see the welcome banner:

<p align="center">
  <img src="images/install_step4.png" alt="Welcome Banner" width="600"/>
</p>

---

## Quick Start

```
rmv_fetch 1S72           # Step 1: Load PDB structure
rmv_source 3             # Step 2: Select BGSU API (3000+ PDBs)
rmv_motifs               # Step 3: Fetch motif data
rmv_summary              # Step 4: View motif summary
rmv_show HL              # Step 5: Render hairpin loops
```

<p align="center">
  <img src="images/quickstart_demo.png" alt="Quick Start Demo" width="600"/>
</p>

For the full tutorial, see **[TUTORIAL.md](TUTORIAL.md)**.

---

## Data Sources

| ID | Source | Type | Coverage | Best For |
|----|--------|------|----------|----------|
| 1 | RNA 3D Atlas | Local | 759 PDBs | Offline loop analysis (HL, IL, junctions) |
| 2 | Rfam | Local | 173 PDBs | Offline named motifs (GNRA, K-turn, etc.) |
| 3 | **BGSU RNA 3D Hub** | Online API | **~3000+ PDBs** | **Most comprehensive — recommended** |
| 4 | Rfam API | Online | All Rfam families | Rfam-annotated motifs |
| 5 | FR3D | User files | Custom | Validating FR3D analysis output |
| 6 | RNAMotifScan (RMS) | User files | Custom | Validating RMS results with P-values |
| 7 | RNAMotifScanX (RMSX) | User files | Custom | Validating RMSX results with P-values |

```
rmv_sources              # List all sources with details
rmv_source 3             # Select a source
rmv_source 1 3           # Combine two sources
```

---

## Command Reference

### Loading & Data

| Command | Description |
|---------|-------------|
| `rmv_fetch <PDB>` | Load PDB structure (no motif data) |
| `rmv_fetch <PDB> cif_use_auth=0` | Load with label_asym_id chain IDs |
| `rmv_source <N>` | Select data source (1-7) |
| `rmv_source <N> <N>` | Combine multiple sources |
| `rmv_motifs` | Fetch motif data from selected source |
| `rmv_load <PDB>` | Legacy: load + fetch in one step |
| `rmv_refresh [PDB]` | Force API re-fetch (bypass cache) |

### Visualization

| Command | Description |
|---------|-------------|
| `rmv_show <TYPE>` | Highlight all instances of motif type |
| `rmv_show <TYPE> <N>` | Zoom to specific instance |
| `rmv_all` | Reset to full colored view |
| `rmv_toggle <TYPE> on/off` | Toggle motif visibility |
| `rmv_bg_color <COLOR>` | Change backbone color |
| `rmv_color <TYPE> <COLOR>` | Change motif color |
| `rmv_colors` | Show color legend |

### Information

| Command | Description |
|---------|-------------|
| `rmv_summary` | Motif types + instance counts |
| `rmv_summary <TYPE>` | Instance table for a motif type |
| `rmv_summary <TYPE> <N>` | Residue details for one instance |
| `rmv_status` | Plugin status |
| `rmv_sources` | List all data sources |
| `rmv_chains` | Chain ID diagnostics |
| `rmv_help` | Full command reference |

### Save & Export

| Command | Description |
|---------|-------------|
| `rmv_save ALL [rep]` | Save all motif images |
| `rmv_save <TYPE> [rep]` | Save all instances of a type |
| `rmv_save <TYPE> <N> [rep]` | Save specific instance |
| `rmv_save current [file]` | Save current view (2400×1800, 300 DPI) |

**Representations:** `cartoon`, `sticks`, `spheres`, `ribbon`, `lines`, `licorice`, `surface`, `cartoon+sticks`

### User Annotations (RMS/RMSX P-Value Control)

| Command | Description |
|---------|-------------|
| `rmv_source 6 off` | Disable RMS P-value filtering |
| `rmv_source 6 on` | Enable RMS P-value filtering |
| `rmv_source 6 MOTIF 0.01` | Set custom P-value threshold |
| `rmv_user <tool> <PDB>` | Legacy: load annotations directly |

---

## Color Customization

Each motif type has a distinct default color:

| Motif | Color | Motif | Color |
|-------|-------|-------|-------|
| HL | Red | GNRA | Teal Green |
| IL | Cyan | UNCG | Brown Orange |
| J3 | Yellow | K-TURN | Bright Blue |
| J4 | Magenta | SARCIN-RICIN | Dark Red |
| J5 | Green | T-LOOP | Pink |
| J6 | Orange | C-LOOP | Sky Blue |
| J7 | Blue | U-TURN | Gold |

Change any color at runtime:
```
rmv_color HL blue
rmv_color GNRA red
rmv_bg_color white
```

---

## Caching

API results (sources 3 and 4) are cached for **30 days** at:
```
~/.rna_motif_visualizer_cache/
```

To force a fresh fetch:
```
rmv_refresh 1S72
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `No motifs found` | Try a different source: `rmv_source 3` (BGSU has widest coverage) |
| `No structure loaded` | Run `rmv_fetch <PDB>` first |
| `No source selected` | Run `rmv_source <N>` before `rmv_motifs` |
| Chain IDs don't match annotations | Use `rmv_fetch <PDB> cif_use_auth=0` for label chain IDs |
| API timeout | Check internet; increase timeout in `database/config.py` (`request_timeout`) |
| Stale data | Run `rmv_refresh <PDB>` to bypass cache |
| Wrong colors | Run `rmv_color <TYPE> <COLOR>` to override |
| Plugin not loading | Verify the `rna_motif_visualizer` folder is in PyMOL's plugin path |
| `rmv_chains` shows unexpected chains | Verify `cif_use_auth` mode matches your annotation convention |

---

## Project Structure

```
rna_motif_visualizer/
├── __init__.py              Package metadata
├── plugin.py                Entry point (PyMOL __init_plugin__)
├── gui.py                   GUI class, 19 command registrations
├── loader.py                Structure loading & visualization pipeline
├── colors.py                30+ motif color definitions
├── image_saver.py           PNG export engine
├── database/
│   ├── config.py            Source ID map, plugin config
│   ├── base_provider.py     Provider abstract base class
│   ├── atlas_provider.py    RNA 3D Atlas (local)
│   ├── rfam_provider.py     Rfam (local)
│   ├── bgsu_api_provider.py BGSU RNA 3D Hub (online)
│   ├── rfam_api_provider.py Rfam API (online)
│   ├── source_selector.py   Source routing & fallback
│   ├── cascade_merger.py    Multi-source Jaccard dedup merge
│   ├── homolog_enricher.py  Motif name enrichment
│   ├── cache_manager.py     30-day disk cache
│   └── user_annotations/    FR3D, RMS, RMSX parsers
└── utils/
    ├── logger.py            Colored console logger
    ├── parser.py            Input string parsers
    └── selectors.py         Chain-safe PyMOL selection builder
```

For detailed architecture and method documentation, see **[DEVELOPER.md](DEVELOPER.md)**.

---

## Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | This file — overview, installation, quick start |
| [TUTORIAL.md](TUTORIAL.md) | Step-by-step tutorial with use cases |
| [DEVELOPER.md](DEVELOPER.md) | Developer reference — all commands, architecture, how to extend |

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**CBB LAB** — @Rakib Hasan Rahad

RNA Motif Visualizer v2.3.0 | Last Updated: 20 February 2026
