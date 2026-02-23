# RNA Motif Visualizer

**A PyMOL plugin for automated visualization and comparative analysis of RNA structural motifs**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![PyMOL](https://img.shields.io/badge/PyMOL-3.0+-blue.svg)
![Python](https://img.shields.io/badge/Python-3.7+-green.svg)

---

## Overview

RNA Motif Visualizer is a PyMOL plugin designed for structural biologists and computational RNA researchers. It automates the detection, visualization, and comparative analysis of RNA structural motifs across 3000+ PDB structures. The plugin integrates multiple data sources (BGSU RNA 3D Hub, Rfam, FR3D, RNAMotifScan) to enable rapid annotation validation, multi-database comparison, and publication-quality image generation.

**Key innovation:** Load structure once, switch between annotation sources instantly—reducing interactive analysis time from minutes to seconds.

---

## 🎯 Use Cases

### 1. **High-Throughput Motif Validation**
*Scenario: Validate computational motif predictions on 3D structures*

- Load a ribosomal structure (e.g., 1S72, 4V88)
- Compare motif annotations from BGSU, Rfam, and custom prediction tools
- Highlight discrepancies between databases in seconds
- Export consensus motif definitions for publication

**Research Impact:** Accelerate validation pipelines for machine learning models predicting RNA motifs.

```
rmv_fetch 4V88              # Load ribosomal LSU
rmv_source 3                # Select BGSU (most comprehensive)
rmv_motifs
rmv_summary                 # View 200+ annotated motifs
rmv_show "SARCIN-RICIN"     # Visualize sarcin-ricin motif
rmv_save current            # Publication-quality image
```

---

### 2. **Comparative Multi-Database Analysis**
*Scenario: Assess motif definitions across Rfam, BGSU, and RNA 3D Atlas*

- Load structure with BGSU annotations (online API, real-time)
- Switch to Rfam for alternative nomenclature
- Switch to local RNA 3D Atlas for historical consistency
- Identify motif overlaps and gaps

**Research Impact:** Resolve structural ambiguities and improve motif taxonomy.

```
rmv_fetch 1S72
rmv_source 3                # BGSU API
rmv_motifs
rmv_summary GNRA            # 23 GNRA instances
rmv_show GNRA
cmd.hide("cartoon")         # Focus on motif

rmv_source 4                # Switch to Rfam (no re-download!)
rmv_motifs
rmv_summary GNRA            # Compare instances
rmv_show GNRA
```

---

### 3. **Custom Annotation Validation & Visualization**
*Scenario: Validate in-house predictions or third-party tool outputs (FR3D, RNAMotifScan)*

- Load local PDB file or fetch from RCSB
- Import custom motif annotations (FR3D XML, RNAMotifScan JSON, custom CSV)
- Overlay predictions on 3D structure
- Validate using chain ID and residue mapping
- Generate visual evidence for publication

**Research Impact:** Integrate computational pipelines; automate annotation QC; create reproducible workflows.

```
rmv_fetch 1S72
rmv_source 5                # FR3D annotations
rmv_motifs
rmv_summary                 # Your FR3D predictions
rmv_show "HL"               # View hairpin loops from your tool
rmv_save ALL                # Batch export all instances
```

---

### 4. **Interactive Structure Exploration for Education**
*Scenario: Teach students RNA motif taxonomy and 3D structure relationships*

- Load canonical structures (ribosomal subunits, tRNAs, snRNAs)
- Highlight all motifs of a specific type
- Zoom to individual instances with residue labels
- Switch between cartoon, sticks, surface representations
- Export labeled images for presentations/papers

**Research Impact:** Accelerate structural literacy; create teaching materials.

```
rmv_fetch 1S72              # 23S rRNA
rmv_source 3
rmv_motifs
rmv_show "KINK-TURN"        # Highlight K-turns
rmv_show "KINK-TURN" 3      # Details of 3rd instance
```

---

### 5. **Publication-Quality Image Generation**
*Scenario: Generate figures for structural biology papers*

- Fetch structure + motifs
- Select motif(s) of interest
- Render in high-quality cartoon with motif highlights
- Export publication-ready PNG/session files

**Research Impact:** Reduce manual model preparation; ensure figure reproducibility.

```
rmv_fetch 4V9D              # Ribosomal LSU
rmv_source 3
rmv_motifs
rmv_show "TRIPLE SHEARED"   # 3 instances
rmv_save current            # ~300 dpi high-res PNG
```

---

### 6. **Chain ID Format Handling for Legacy & mmCIF Data**
*Scenario: Work with structures using different chain ID conventions (auth vs. label)*

- Load structure with optional chain ID mode selection
- Seamlessly map custom annotations to correct chains
- Support both PDB (`auth_asym_id`) and mmCIF (`label_asym_id`) conventions

**Research Impact:** Enable analysis of complex multi-model structures; ensure annotation reproducibility.

```
rmv_fetch 1S72 cif_use_auth=0    # Use label chain IDs (mmCIF standard)
rmv_source 7                      # RNAMotifScanX (uses label IDs)
rmv_motifs
rmv_summary                       # Display in label chain format
```

---

## ✨ Key Features

| Feature | Benefit | Use Case |
|---------|---------|----------|
| **Multi-Source Integration** | Compare annotation standards (BGSU, Rfam, RNA 3D Atlas, custom) | Resolve motif definition disagreements |
| **Instant Source Switching** | Load structure once, switch databases without re-download | 10× faster multi-database analysis |
| **Custom Annotation Support** | Import FR3D XML, RNAMotifScan JSON, user-defined CSV | Validate computational predictions |
| **Dual Chain ID Modes** | Support auth_asym_id (PDB) and label_asym_id (mmCIF) | Handle complex PDB entries transparently |
| **Batch Image Export** | Generate publication-quality images programmatically | Automate figure generation |
| **Interactive Explorer** | Zoom to individual motif instances with residue details | Hands-on structure learning |
| **3000+ Structure Coverage** | BGSU API covers all known rRNA/RNA structures | Immediate access to canonical structures |
| **Smart Caching** | 30-day API cache; avoid redundant downloads | Offline-capable after first fetch |

---

## 📦 Installation

### Step 1: Download

```bash
git clone https://github.com/Rakib-Hasan-Rahad/rna-motif-visualizer.git
```

Or download the [ZIP file](https://github.com/Rakib-Hasan-Rahad/rna-motif-visualizer/archive/refs/heads/main.zip) and extract.

### Step 2: Install in PyMOL

1. Open **PyMOL**
2. Go to **Plugin → Plugin Manager**
3. Click the **Settings** tab
4. Click **Add new directory**
5. Navigate to and select the **`rna_motif_visualizer`** folder
6. Click **OK** and restart PyMOL

### Step 3: Verify Installation

You should see in the PyMOL terminal:

```
[2026-02-20 09:53:20] [SUCCESS] RNA Motif Visualizer GUI initialized
[2026-02-20 09:53:20] [INFO] Version 2.3.0
```

---

## 🚀 Quick Start

### 1. See All Available Commands

```
rmv_help
```

### 2. Load a Structure & Visualize Motifs

```
rmv_fetch 1S72           # Download 23S rRNA, fetch motifs
rmv_summary              # Show available motifs
rmv_show HAIRPIN LOOP    # Highlight hairpin loops
```

### 3. Explore Individual Instances

```
rmv_show GNRA 1          # Zoom to first GNRA instance
rmv_show GNRA 2          # Switch to second instance
```

### 4. Compare Data Sources

```
rmv_source 3             # BGSU API
rmv_source 4             # Rfam API (no re-download!)
```

### 5. Export Images

```
rmv_save current         # Save high-res PNG of current view
rmv_save ALL             # Batch export all motif instances
```

---

## 📖 Complete Command Reference

### Loading & Data Management

| Command | Description |
|---------|-------------|
| `rmv_fetch <PDB_ID>` | Fetch structure + load default motif data |
| `rmv_fetch <PDB_ID> cif_use_auth=0` | Load with mmCIF label chain IDs |
| `rmv_motifs` | Load motif data from selected source |
| `rmv_source <N>` | Select data source (1-7, see `rmv_sources`) |
| `rmv_sources` | List all available sources with descriptions |
| `rmv_load <FILE.pdb>` | Load local PDB file + auto-detect motifs |
| `rmv_refresh` | Force re-fetch from API (bypass cache) |

### Visualization & Navigation

| Command | Description |
|---------|-------------|
| `rmv_show <MOTIF_TYPE>` | Highlight all instances of motif type |
| `rmv_show <MOTIF_TYPE> <NO>` | Zoom to specific instance #NO |
| `rmv_all` | Show all motifs (reset view) |
| `rmv_toggle <MOTIF_TYPE> on/off` | Show/hide motif type |
| `rmv_color <MOTIF_TYPE> <COLOR>` | Change motif color at runtime |
| `rmv_colors` | Display color legend |
| `rmv_bg_color <COLOR>` | Change background color |

### Information & Diagnostics

| Command | Description |
|---------|-------------|
| `rmv_summary` | Show motif type counts |
| `rmv_summary <MOTIF_TYPE>` | Show instances of specific type |
| `rmv_chains` | Show chain IDs + CIF mode status |
| `rmv_status` | Current plugin status |
| `rmv_help` | Full command reference |

### Custom Annotations

| Command | Description |
|---------|-------------|
| `rmv_user <FILE>` | Load custom annotations (FR3D XML, JSON, CSV) |
| `rmv_user_pvalue <THRESHOLD>` | Filter annotations by p-value |

### Image Export

| Command | Description |
|---------|-------------|
| `rmv_save current` | Export current PyMOL view as PNG (~300 dpi) |
| `rmv_save ALL` | Batch export all motif instances |

---

## 🎨 Data Sources

### Online (Real-time, 3000+ Structures)

| Source | Command | Coverage | Update Frequency |
|--------|---------|----------|-----------------|
| **BGSU RNA 3D Hub** | `rmv_source 3` | ~3000+ PDB structures | Weekly |
| **Rfam** | `rmv_source 4` | Named motifs (GNRA, K-turn, etc.) | Monthly |

### Offline (Bundled, Pre-computed)

| Source | Command | Motif Types | Size |
|--------|---------|-------------|------|
| **RNA 3D Motif Atlas** | `rmv_source 1` | 7 types (HL, IL, J3-J7, PSEUDOKNOT) | ~5 MB |
| **Rfam Local** | `rmv_source 2` | 19 named motifs | ~2 MB |

### User-Provided (Custom Annotations)

| Source | Command | Format | Example |
|--------|---------|--------|---------|
| **FR3D** | `rmv_user fr3d.xml` | XML | [fr3d_example.xml](examples/fr3d_example.xml) |
| **RNAMotifScan** | `rmv_user rms.json` | JSON | [rms_example.json](examples/rms_example.json) |
| **Custom CSV** | `rmv_user motifs.csv` | CSV | [custom_example.csv](examples/custom_example.csv) |

---

## 🔗 Chain ID Handling

The plugin automatically handles both PDB and mmCIF chain ID conventions:

### Default Mode (auth_asym_id)
```
rmv_fetch 1S72          # Chains: 0, 9, A, B, ... (author-assigned)
```

### Label ID Mode (label_asym_id)
```
rmv_fetch 1S72 cif_use_auth=0    # Chains: A, AA, AB, ... (PDB-standardized)
```

**Use label mode when:**
- Working with mmCIF files where PDB standardization is required
- Using data sources annotated with label_asym_id (e.g., RNAMotifScanX)
- Comparing multi-chain complex structures

---

## 💾 Caching & Performance

API responses are cached for **30 days** at:
```
~/.rna_motif_visualizer_cache/
```

**Benefits:**
- Second load of same structure: <1 second
- Offline access after first fetch
- Reduced server load

**Clear cache manually:**
```bash
rm -rf ~/.rna_motif_visualizer_cache/
```

---

## 🧬 Supported Motif Types

### Structural Motifs (BGSU/RNA 3D Atlas)
- **Hairpin Loops (HL)**
- **Internal Loops (IL)**
- **Junctions:** 3-way (J3), 4-way (J4), 5-way (J5), 6-way (J6), 7-way (J7)
- **Pseudoknots**
- **Kissing Hairpins**

### Sequence-Based Motifs (Rfam)
- **GNRA Tetraloops** (GAAA, GGAA, GCAA, GGGA)
- **UNCG Tetraloops**
- **Kink-Turns (K-turns)**
- **T-loops**
- **C-loops**
- **U-turns**

### Composite/Complex Motifs
- **Sarcin-Ricin**
- **Kink-Turn + Bulge combinations**
- **Triple-sheared structures**
- **Non-canonical base pair platforms**

---

## 📊 Example Workflows

### Workflow 1: Validate Computational Predictions

```python
# In PyMOL:
rmv_fetch 1S72
rmv_source 5                    # Load FR3D annotations
rmv_motifs
rmv_show "INTERNAL LOOP"        # View your predictions
rmv_save ALL                    # Export for validation report
```

### Workflow 2: Compare Multiple Databases

```python
rmv_fetch 4V88                  # Ribosomal LSU
rmv_source 3
rmv_motifs
rmv_summary KINK-TURN           # BGSU: 12 instances
rmv_show KINK-TURN

# Now switch to Rfam
rmv_source 4
rmv_motifs
rmv_summary KINK-TURN           # Rfam: 8 instances (different definition)
rmv_show KINK-TURN

# Assess differences
```

### Workflow 3: Generate Publication Figures

```python
rmv_fetch 1S72
rmv_source 3
rmv_motifs
rmv_show "SARCIN-RICIN"
cmd.hide("ribbon")
cmd.show("sticks")
rmv_save current                # ~300 dpi PNG ready for journal
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Plugin not appearing | Verify you selected `rna_motif_visualizer` folder (not parent directory) in Plugin Manager |
| No motifs found | Try `rmv_source 1` (local) or check structure is in PDB database |
| API errors | Check internet connection; try `rmv_source 2` (local only) |
| Slow first load | Normal—API call + caching. Second load is instant |
| Chain ID mismatch in annotations | Use `rmv_fetch <ID> cif_use_auth=0` for label ID mode |
| Session not saving | Save as `.pse` (PyMOL Session) before `rmv_save` |

**Reset everything:**
```python
cmd.delete("all")
cmd.reset()
rmv_fetch 1S72
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [TUTORIAL.md](TUTORIAL.md) | Step-by-step walkthroughs with examples |
| [DEVELOPER.md](DEVELOPER.md) | Architecture, command implementation, how to extend |
| **README.md** | This file — overview and quick start |

---

## 🗂️ Project Structure

```
rna-motif-visualizer/
├── rna_motif_visualizer/
│   ├── __init__.py                  # Package init, version info
│   ├── plugin.py                    # PyMOL plugin entry point
│   ├── gui.py                       # Command handlers (18 commands)
│   ├── loader.py                    # Rendering & visualization logic
│   ├── colors.py                    # Motif color definitions
│   ├── database/
│   │   ├── base_provider.py         # Abstract data source interface
│   │   ├── bgsu_provider.py         # BGSU API integration
│   │   ├── rfam_provider.py         # Rfam API integration
│   │   ├── local_provider.py        # Bundled offline database
│   │   ├── user_annotations/        # FR3D, RNAMotifScan, custom CSVs
│   │   ├── cache.py                 # 30-day API response cache
│   │   └── motif_definitions.py     # Motif type taxonomy
│   ├── motif_database/              # Offline data (7 MB)
│   │   ├── atlas/                   # RNA 3D Motif Atlas (~5 MB)
│   │   └── rfam/                    # Rfam motifs (~2 MB)
│   └── utils/
│       ├── selectors.py             # PyMOL selection building
│       ├── chain_converter.py        # auth ↔ label chain mapping
│       └── logger.py                # Console logging
├── README.md                        # This file
├── TUTORIAL.md                      # Step-by-step guide
├── DEVELOPER.md                     # Developer guide
├── LICENSE                          # MIT License
└── .gitignore
```

---

## 🔄 Workflow: From Prediction to Publication

```
Step 1: Run computational tool (e.g., machine learning model for motif detection)
        ↓
Step 2: Export predictions to CSV/JSON
        ↓
Step 3: Load in RNA Motif Visualizer
        rmv_fetch <PDB_ID>
        rmv_user predictions.json
        
        ↓
Step 4: Validate against known motifs
        rmv_source 3        # BGSU reference
        rmv_motifs
        rmv_show <MOTIF>    # Compare visually
        
        ↓
Step 5: Generate publication figures
        rmv_save ALL        # Batch export all instances
        
        ↓
Step 6: Include in paper/supplementary materials
```

---

## 📄 Citation

If you use RNA Motif Visualizer in your research, please cite:

```bibtex
@software{rna_motif_visualizer_2026,
  title={RNA Motif Visualizer: Automated comparative analysis of RNA structural motifs},
  author={Rahad, Rakib Hasan},
  year={2026},
  url={https://github.com/Rakib-Hasan-Rahad/rna-motif-visualizer},
  license={MIT}
}
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

- **BGSU RNA 3D Hub** — Comprehensive RNA motif annotations and structure database
- **Rfam Database** — Conserved RNA family and motif definitions
- **RNA 3D Motif Atlas** — Historical RNA motif taxonomy and structure analysis
- **PyMOL** — Schrödinger, LLC; molecular visualization platform
- **RNAMotifScan & FR3D** — Community tools for motif annotation

---

## 🤝 Contributing

Contributions welcome! See [DEVELOPER.md](DEVELOPER.md) for:
- Architecture overview
- How to add new data sources
- How to extend motif types
- Code style guidelines

---

## 📧 Support

- **Issues & Bug Reports:** [GitHub Issues](https://github.com/Rakib-Hasan-Rahad/rna-motif-visualizer/issues)
- **Documentation:** [TUTORIAL.md](TUTORIAL.md) and [DEVELOPER.md](DEVELOPER.md)
- **Questions:** Open a GitHub Discussion

---

**Happy RNA Visualization! 🧬**

*Transform structural biology with automated, reproducible motif analysis.*
