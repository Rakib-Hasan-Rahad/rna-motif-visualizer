# RNA Motif Visualizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyMOL](https://img.shields.io/badge/PyMOL-Plugin-blue.svg)](https://pymol.org/)
[![Version](https://img.shields.io/badge/Version-2.1.0-green.svg)](#)

A powerful PyMOL plugin for visualizing RNA structural motifs. Automatically detects and highlights RNA motifs like hairpin loops, internal loops, junctions, GNRA tetraloops, kink-turns, and many others directly on your RNA structure.

**🚀 Now supports 3000+ PDB structures via online APIs!**

![RNA Motif Visualizer Banner](images/banner.png)
<!-- PLACEHOLDER: Add banner image showing the plugin in action -->

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔬 **Multi-Source Data** | Local database + BGSU API + Rfam API for comprehensive coverage |
| 🎨 **Automatic Coloring** | Each motif type gets distinct colors for easy identification |
| 📊 **Instance Explorer** | View individual motif instances with detailed residue information |
| 💡 **Smart Suggestions** | Contextual help guides you through each command |
| 💾 **Intelligent Caching** | API responses cached for 30 days for fast repeated access |
| 🔌 **Extensible** | Add your own motif databases easily |

---

## 📦 Installation

### Step 1: Download the Plugin

```bash
git clone https://github.com/Rakib-Hasan-Rahad/rna-motif-visualizer.git
```

Or [download the ZIP file](https://github.com/Rakib-Hasan-Rahad/rna-motif-visualizer/archive/refs/heads/main.zip) and extract it.

### Step 2: Install in PyMOL

1. Open **PyMOL**
2. Go to **Plugin** → **Plugin Manager**
3. Click the **Settings** tab
4. Click **Add new directory**
5. Navigate to and select the `rna_motif_visualizer` folder
6. Click **OK** and close Plugin Manager
7. **Restart PyMOL**

![Installation Steps](images/installation_steps.png)
<!-- PLACEHOLDER: Screenshot showing Plugin Manager settings -->

### Step 3: Verify Installation

You should see this welcome message when PyMOL starts:

![Installation Success](images/installation_success.png)
<!-- PLACEHOLDER: Screenshot of welcome message in PyMOL console -->

---

## 🚀 Quick Start

### Load a Structure

```
rna_load 1S72
```

That's it! The plugin will:
1. Download the structure from RCSB PDB
2. Detect all motifs from the database
3. Display them with different colors
4. Print a summary table with suggestions

![Quick Start Demo](images/quickstart_demo.png)
<!-- PLACEHOLDER: Screenshot showing loaded structure with colored motifs -->

### Follow the Suggestions

After each command, look at the console for **"Next steps"** suggestions:

```
==================================================
  MOTIF SUMMARY - 1S72
==================================================
  MOTIF TYPE            INSTANCES
--------------------------------------------------
  GNRA                         3
  HL                           5
  IL                           2
==================================================

  Next steps:
    rna_show GNRA              Highlight & view GNRA instances
    rna_summary                Display this summary again
    rna_all                    Show all motifs (default view)
```

![Console Suggestions](images/console_suggestions.png)
<!-- PLACEHOLDER: Screenshot of console output with suggestions -->

---

## 📖 Complete Command Reference

### Core Commands

| Command | Description | Example |
|---------|-------------|---------|
| `rna_load <PDB>` | Load structure and show motifs | `rna_load 1S72` |
| `rna_show <TYPE>` | Highlight specific motif type | `rna_show GNRA` |
| `rna_instance <TYPE> <NO>` | View single instance | `rna_instance GNRA 1` |
| `rna_all` | Show all motifs (reset view) | `rna_all` |
| `rna_summary` | Display motif summary table | `rna_summary` |

### Data Source Commands

| Command | Description | Example |
|---------|-------------|---------|
| `rna_source <MODE>` | Set data source mode | `rna_source bgsu` |
| `rna_source_info` | Show current source config | `rna_source_info` |
| `rna_refresh` | Force refresh from API | `rna_refresh` |

### Utility Commands

| Command | Description | Example |
|---------|-------------|---------|
| `rna_switch <DB>` | Switch database | `rna_switch rfam` |
| `rna_toggle <TYPE> on/off` | Toggle motif visibility | `rna_toggle HL off` |
| `rna_status` | Show current status | `rna_status` |
| `rna_databases` | List available databases | `rna_databases` |
| `rna_bg_color <COLOR>` | Change background color | `rna_bg_color white` |

---

## 🔄 Data Source Modes

The plugin can fetch motif data from multiple sources:

| Mode | Command | Description |
|------|---------|-------------|
| **Auto** | `rna_source auto` | Smart selection (default) - tries local first, then APIs |
| **Local** | `rna_source local` | Offline mode - bundled database only |
| **BGSU** | `rna_source bgsu` | BGSU RNA 3D Hub API (~3000+ structures) |
| **Rfam** | `rna_source rfam` | Rfam API (named motifs like GNRA, K-turn) |
| **All** | `rna_source all` | Combine results from all sources |

### Available Motifs by Source

| Source | Motif Types |
|--------|-------------|
| **Local/BGSU** | HL (Hairpin), IL (Internal), J3-J7 (Junctions) |
| **Rfam** | GNRA, UNCG, K-turn, T-loop, C-loop, U-turn, and more |

![Data Sources](images/data_sources.png)
<!-- PLACEHOLDER: Diagram showing data flow from different sources -->

---

## 🎨 Understanding the Display

### Motif Colors

Each motif type is assigned a distinct color:

| Motif Type | Color | Description |
|------------|-------|-------------|
| HL | Red | Hairpin Loops |
| IL | Orange | Internal Loops |
| J3 | Yellow | 3-way Junctions |
| J4 | Green | 4-way Junctions |
| GNRA | Forest Green | GNRA Tetraloops |
| K-turn | Marine Blue | Kink-turns |
| T-loop | Pink | T-loops |

![Color Legend](images/color_legend.png)
<!-- PLACEHOLDER: Visual color legend showing all motif colors -->

### PyMOL Object Panel

After loading, you'll see motif objects in the right panel:

![Object Panel](images/object_panel.png)
<!-- PLACEHOLDER: Screenshot of PyMOL object panel with motif objects -->

- **Type Objects**: `GNRA`, `HL`, `IL` - contain all instances of that type
- **Instance Objects**: `GNRA_1`, `GNRA_2` - individual instances (created after `rna_show`)

---

## 📊 Instance Explorer

### View All Instances of a Type

```
rna_show GNRA
```

This displays an instance table:

```
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
```

![Instance Table](images/instance_table.png)
<!-- PLACEHOLDER: Screenshot of instance table output in console -->

### View Single Instance

```
rna_instance GNRA 1
```

This will:
- Zoom to the instance
- Show detailed residue information
- Suggest next/previous instance navigation

![Instance View](images/instance_view.png)
<!-- PLACEHOLDER: Screenshot of zoomed instance with residue details -->

---

## 🗄️ Supported Databases

### RNA 3D Motif Atlas (BGSU)

From the BGSU RNA Group - geometrically defined motif families:

- **Hairpin loops (HL)**
- **Internal loops (IL)**
- **3-way to 7-way junctions (J3-J7)**

**Source**: https://rna.bgsu.edu/rna3dhub/motifs

### Rfam Motif Database

Curated RNA structural motifs from EMBL-EBI:

- **GNRA tetraloops**
- **UNCG tetraloops**
- **Kink-turns (K-turns)**
- **Sarcin-ricin loops**
- **T-loops, C-loops, U-turns**
- And more...

**Source**: https://rfam.org

---

## 💾 Caching System

API responses are cached locally for fast repeated access:

| Setting | Value |
|---------|-------|
| **Cache Location** | `~/.rna_motif_visualizer_cache/` |
| **Expiry** | 30 days |
| **Force Refresh** | `rna_refresh` |

To clear cache manually:
```bash
rm -rf ~/.rna_motif_visualizer_cache/
```

---

## 🔧 Adding Custom Databases

### Add RNA 3D Atlas Format Data

1. Navigate to `rna_motif_visualizer/motif_database/`
2. Add JSON files with motif data
3. Restart PyMOL

**JSON Format**:
```json
{
  "motif_id": "HL_12345.1",
  "alignment": {
    "HL_1S72_001": {
      "1": "1S72|1|0|G|100",
      "2": "1S72|1|0|A|101"
    }
  }
}
```

### Add Custom Colors

Edit `rna_motif_visualizer/colors.py`:

```python
MOTIF_COLORS = {
    'MY_MOTIF': (0.5, 0.8, 0.3),  # RGB values 0-1
}
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Plugin not appearing | Check you selected `rna_motif_visualizer` folder (not parent) |
| No motifs found | Try `rna_source all` or different database |
| API errors | Check internet connection, try `rna_source local` |
| Slow loading | First API call is slow, subsequent calls use cache |
| Colors look wrong | Update to latest version |

### Reset Everything

```python
# Clear all objects in PyMOL
cmd.delete("all")
cmd.reset()

# Then reload
rna_load 1S72
```

---

## 📚 Additional Documentation

| Document | Description |
|----------|-------------|
| **[TUTORIAL.md](TUTORIAL.md)** | Step-by-step tutorial with examples and expected outputs |
| **[DEVELOPER.md](DEVELOPER.md)** | Developer guide, architecture, and contribution guidelines |

---

## 🏗️ Project Structure

```
rna-motif-visualizer/
├── rna_motif_visualizer/
│   ├── __init__.py
│   ├── plugin.py           # Plugin entry point
│   ├── gui.py              # PyMOL commands
│   ├── loader.py           # Core motif loading logic
│   ├── colors.py           # Color definitions
│   ├── database/           # Database providers
│   │   ├── bgsu_api_provider.py
│   │   ├── rfam_api_provider.py
│   │   ├── cache_manager.py
│   │   └── source_selector.py
│   ├── motif_database/     # Local motif data
│   └── utils/              # Utility modules
├── images/                 # Documentation images
├── README.md               # This file
├── TUTORIAL.md             # User tutorial
├── DEVELOPER.md            # Developer guide
└── LICENSE
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

- **RNA 3D Motif Atlas** - BGSU RNA Group
- **Rfam Database** - EMBL-EBI
- **PyMOL** - Schrödinger, LLC

---

## 🤝 Contributing

Contributions welcome! See [DEVELOPER.md](DEVELOPER.md) for guidelines.

---

<p align="center">
  <b>Happy RNA Visualization! 🧬</b>
</p>

