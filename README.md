# RNA Motif Visualizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyMOL](https://img.shields.io/badge/PyMOL-Plugin-blue.svg)](https://pymol.org/)
[![Version](https://img.shields.io/badge/Version-2.1.0-green.svg)](#)

A PyMOL plugin for visualizing RNA structural motifs. Automatically detects and highlights RNA motifs like hairpin loops, internal loops, junctions, GNRA tetraloops, kink-turns, and more directly on your RNA structure.

**🚀 Supports 3000+ PDB structures via BGSU and Rfam APIs!**

![RNA Motif Visualizer Banner](images/banner.png)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔬 **Multi-Source Data** | Local database + BGSU API + Rfam API |
| 🎨 **Automatic Coloring** | Each motif type gets distinct colors |
| 📊 **Instance Explorer** | View individual motif instances with details |
| 💡 **Smart Suggestions** | Contextual help after each command |
| 💾 **Intelligent Caching** | API responses cached for 30 days |
| 🎯 **Custom Colors** | Change motif colors at runtime |

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

### Step 3: Verify Installation

You should see a welcome message when PyMOL starts:

```
==================================================
RNA Motif Visualizer v2.1.0 - Loaded Successfully!
==================================================
```

---

## 🚀 Quick Start

### 1. See All Available Commands

```
rna_help
```

This shows a complete command reference organized by category.

### 2. Check Available Data Sources

```
rna_sources
```

Shows LOCAL (offline) and ONLINE (API) sources separately.

### 3. Select a Source

```
rna_source bgsu     # Use BGSU API (~3000+ structures)
rna_source local    # Use bundled offline database
rna_source auto     # Smart selection (default)
```

### 4. Load a Structure

```
rna_load 1S72
```

The plugin will:
1. Download the structure from RCSB PDB
2. Detect all motifs from the selected source
3. Display them with different colors
4. Print a summary with next steps

### 5. Explore Motifs

```
rna_show GNRA           # Highlight GNRA tetraloops
rna_instance GNRA 1     # Zoom to instance #1
rna_all                 # Show all motifs again
```

---

## 📖 Complete Command Reference

### Loading & Sources

| Command | Description |
|---------|-------------|
| `rna_load <PDB_ID>` | Load structure and visualize motifs |
| `rna_source` | Show current source mode & config |
| `rna_source <MODE>` | Set source (auto/local/bgsu/rfam/all) |
| `rna_sources` | Show all available sources (detailed) |
| `rna_switch <DB>` | Switch database (atlas/rfam) |
| `rna_refresh` | Force refresh from API (bypass cache) |

### Visualization

| Command | Description |
|---------|-------------|
| `rna_all` | Show all motifs (reset view) |
| `rna_show <TYPE>` | Highlight specific motif type |
| `rna_instance <TYPE> <NO>` | View single instance (zoom + details) |
| `rna_toggle <TYPE> on/off` | Toggle motif visibility |
| `rna_bg_color <COLOR>` | Change background color |
| `rna_color <TYPE> <COLOR>` | Change motif color |
| `rna_colors` | Show color legend |

### Information

| Command | Description |
|---------|-------------|
| `rna_summary` | Show motif types and instance counts |
| `rna_status` | Show current plugin status |
| `rna_help` | Show command reference |

---

## 🔄 Data Source Modes

| Mode | Command | Description |
|------|---------|-------------|
| **Auto** | `rna_source auto` | Smart selection (default) - tries local first, then APIs |
| **Local** | `rna_source local` | Offline mode - bundled database only |
| **BGSU** | `rna_source bgsu` | BGSU RNA 3D Hub API (~3000+ structures) |
| **Rfam** | `rna_source rfam` | Rfam API (named motifs like GNRA, K-turn) |
| **All** | `rna_source all` | Combine results from all sources |

### Motif Types by Source

| Source | Motif Types |
|--------|-------------|
| **Local/BGSU** | HL (Hairpin), IL (Internal), J3-J7 (Junctions) |
| **Rfam** | GNRA, UNCG, K-turn, T-loop, C-loop, U-turn |

---

## 🎨 Color Customization

### Default Colors

| Motif Type | Color | Description |
|------------|-------|-------------|
| HL | Red | Hairpin Loops |
| IL | Orange | Internal Loops |
| J3 | Yellow | 3-way Junctions |
| J4 | Green | 4-way Junctions |
| GNRA | Forest Green | GNRA Tetraloops |
| K-turn | Marine Blue | Kink-turns |

### Change Colors at Runtime

```
rna_color HL blue       # Change hairpin loops to blue
rna_color GNRA red      # Change GNRA to red
rna_colors              # View current color legend
```

**Available colors**: red, green, blue, yellow, cyan, magenta, orange, purple, pink, white, gray, lime, teal, salmon, forest, marine, slate

---

## 📊 Instance Explorer

### View All Instances of a Type

```
rna_show HL
```

Displays an instance table with chain and residue information.

### View Single Instance

```
rna_instance HL 1
```

Zooms to the instance and shows detailed residue info.

---

## 💾 Caching

API responses are cached for fast repeated access:

| Setting | Value |
|---------|-------|
| **Cache Location** | `~/.rna_motif_visualizer_cache/` |
| **Expiry** | 30 days |
| **Force Refresh** | `rna_refresh` |

Clear cache manually:
```bash
rm -rf ~/.rna_motif_visualizer_cache/
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Plugin not appearing | Check you selected `rna_motif_visualizer` folder |
| No motifs found | Try `rna_source all` or different database |
| API errors | Check internet, try `rna_source local` |
| Slow loading | First API call is slow, subsequent use cache |

### Reset Everything

```python
cmd.delete("all")
cmd.reset()
rna_load 1S72
```

---

## 🗂️ Project Structure

```
rna-motif-visualizer/
├── rna_motif_visualizer/
│   ├── plugin.py           # Plugin entry point
│   ├── gui.py              # PyMOL commands
│   ├── loader.py           # Core visualization logic
│   ├── colors.py           # Color definitions
│   ├── database/           # Data providers (BGSU, Rfam, cache)
│   ├── motif_database/     # Local motif data
│   └── utils/              # Utility modules
├── README.md
├── TUTORIAL.md
├── DEVELOPER.md
└── LICENSE
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[TUTORIAL.md](TUTORIAL.md)** | Step-by-step tutorial with examples |
| **[DEVELOPER.md](DEVELOPER.md)** | Architecture and contribution guide |

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

