# RNA Motif Visualizer - Installation & Quick Start Guide

## 📦 Installation Instructions

### Step 1: Locate Your PyMOL Plugins Directory

The location depends on your operating system:

**macOS:**
```bash
# Typically one of these locations:
~/.pymol/startup/
~/pymol/
/Applications/PyMOL.app/Contents/Resources/plugins/
```

**Linux:**
```bash
# Typically:
~/.pymol/startup/
~/.local/lib/pythonX.X/site-packages/pymol/plugins/
```

**Windows:**
```
%USERPROFILE%\AppData\Roaming\PyMOL\startup\
C:\Program Files\PyMOL\plugins\
C:\Users\<YourUsername>\AppData\Roaming\PyMOL\startup\
```

### Step 2: Copy the Plugin

1. If the directory doesn't exist, create it:
   ```bash
   mkdir -p ~/.pymol/startup/
   ```

2. Copy the entire `rna_motif_visualizer` folder to your plugins directory:
   ```bash
   cp -r rna_motif_visualizer ~/.pymol/startup/
   ```

### Step 3: Restart PyMOL

Close PyMOL completely and reopen it. The plugin will automatically load.

### Step 4: Verify Installation

Open PyMOL and check the console. You should see:
```
============================================================
RNA MOTIF VISUALIZER v1.0.0
============================================================
Ready to visualize RNA structural motifs!

Quick Start:
  1. Load a structure: rna_load 1S72
  2. Toggle motifs: rna_toggle KTURN on/off
  3. Check status: rna_status
============================================================
```

---

## 🚀 Quick Start (5 Minutes)

### Example 1: Load and Visualize Motifs

```python
# In PyMOL console (type these commands):

# Load a ribosomal RNA structure
rna_load 1S72

# Show status
rna_status
```

**Expected Output:**
```
============================================================
RNA MOTIF VISUALIZER - STATUS
============================================================
Structure: 1S72
PDB ID: 1S72

Loaded Motifs (5):
  KINK-TURN             ( 7 instances) ✓ visible
  C-LOOP                ( 4 instances) ✓ visible
  SARCIN-RICIN          (13 instances) ✓ visible
  REVERSE-KINK-TURN     ( 2 instances) ✓ visible
  E-LOOP                (10 instances) ✓ visible
============================================================
```

### Example 2: Toggle Motif Visibility

```python
# Hide all K-turns
rna_toggle KTURN off

# Show GNRA tetraloops
rna_toggle GNRA on

# Hide A-minors
rna_toggle AMINOR off
```

### Example 3: Load from Local File

```python
# Load structure from your computer
rna_load /path/to/your_structure.pdb

# Or on Windows:
rna_load C:\Users\YourName\Downloads\structure.cif
```

---

## 🎯 Common Tasks

### Task 1: Highlight Only One Motif Type

```python
# Load structure
rna_load 1S72

# Hide all motifs first
rna_toggle KTURN off
rna_toggle AMINOR off
rna_toggle GNRA off
rna_toggle KL_MOTIF off
rna_toggle SARCIN_RICIN off
rna_toggle KINK_TURN off
rna_toggle HAIRPIN off
rna_toggle BULGE off
rna_toggle INTERNAL_LOOP off
rna_toggle JUNCTION off

# Show only K-turns
rna_toggle KTURN on

# Zoom in on K-turns
select kturn_focus, KTURN_ALL
zoom kturn_focus
```

### Task 2: Compare Multiple Structures

```python
# Load first structure
rna_load 1S72

# Note down the motifs in status
rna_status

# Load second structure (new window)
rna_load 2QWY

# Compare motif distribution
rna_status
```

### Task 3: Create Publication Figure

```python
# Load structure
rna_load 1S72

# Show only specific motifs
rna_toggle GNRA on
rna_toggle KTURN on
rna_toggle AMINOR off

# Use PyMOL's cartoon mode
cartoon helix
cartoon loop

# Spin the structure
spin on  # Press space to stop

# Save image
png /path/to/figure.png, dpi=300
```

---

## 🔍 Troubleshooting

### Problem: "Plugin doesn't load"

**Check 1:** Verify file structure
```bash
# The folder should contain:
ls -la ~/.pymol/startup/rna_motif_visualizer/

# Should show:
# __init__.py
# plugin.py
# gui.py
# loader.py
# colors.py
# utils/
# motif_database/
# README.md
```

**Check 2:** Look for error messages
- Open PyMOL Console (Windows → Python Console)
- Check for red error text
- Copy and report errors

**Check 3:** Verify Python version
- PyMOL 1.8+ required
- PyMOL must include Python support

### Problem: "rna_load command not found"

**Solution:**
1. Ensure plugin loaded (check console at startup)
2. Restart PyMOL completely
3. Verify folder is in correct location
4. Check file permissions: `chmod -R 755 rna_motif_visualizer/`

### Problem: "Structure fails to load"

```python
# Check 1: Is PDB ID correct?
rna_load 1S72        # Good
rna_load 1s72        # Also good (case-insensitive)
rna_load NOTACODE    # Will fail

# Check 2: Internet connection
# If PDB ID from RCSB fails, try local file:
rna_load /path/to/structure.pdb

# Check 3: File path correct?
# Use absolute paths:
rna_load /Users/username/Downloads/1S72.pdb  # Good
rna_load ~/structure.pdb                       # May work
rna_load structure.pdb                         # May fail
```

### Problem: "No motifs found"

**This is normal!** Not all structures have annotated motifs in the database.

```python
# This will work (has data):
rna_load 1S72   # Ribosomal RNA

# This may show no motifs (not in database):
rna_load 1ABC   # Random PDB

# Add your own motifs to:
# motif_database/kturn.json
# motif_database/aminor.json
# etc.
```

### Problem: "Colors look wrong"

```python
# Reset colors:
reset
rna_load 1S72

# If still wrong, clear and reload:
delete *
rna_load 1S72
```

---

## 📚 Available Commands

| Command | Usage | Example |
|---------|-------|---------|
| `rna_load` | Load structure | `rna_load 1S72` |
| `rna_toggle` | Toggle motif visibility | `rna_toggle KTURN on` |
| `rna_status` | Show current status | `rna_status` |

### Command Syntax

```python
# Load structure (PDB ID or file path)
rna_load <PDB_ID_or_PATH>

# Examples:
rna_load 1S72
rna_load 2QWY
rna_load /path/to/structure.pdb

# Toggle motif visibility (on/off or yes/no or true/false)
rna_toggle <MOTIF_TYPE> <on|off>

# Examples:
rna_toggle KTURN on
rna_toggle AMINOR off
rna_toggle GNRA on

# Show current status
rna_status
```

---

## 🎨 Available Motif Types

| Type | Color | Keyboard |
|------|-------|----------|
| KTURN | 🔴 Red | `rna_toggle KTURN` |
| AMINOR | 🔵 Cyan | `rna_toggle AMINOR` |
| GNRA | 🟡 Yellow | `rna_toggle GNRA` |
| KL_MOTIF | 🟣 Magenta | `rna_toggle KL_MOTIF` |
| SARCIN_RICIN | 🟢 Green | `rna_toggle SARCIN_RICIN` |
| KINK_TURN | 🟠 Orange | `rna_toggle KINK_TURN` |
| HAIRPIN | 🟢 Lime | `rna_toggle HAIRPIN` |
| BULGE | 🔴 Pink | `rna_toggle BULGE` |
| INTERNAL_LOOP | 🔵 Light Blue | `rna_toggle INTERNAL_LOOP` |
| JUNCTION | 🟡 Gold | `rna_toggle JUNCTION` |

---

## 📖 Advanced Usage

### Using Python API

```python
# In a Python script or PyMOL session:

from rna_motif_visualizer import VisualizationManager
from pymol import cmd

# Initialize
db_path = "/path/to/motif_database"
viz = VisualizationManager(cmd, db_path)

# Load structure
motifs = viz.load_and_visualize("1S72")

# Print loaded motifs
for motif_type, info in motifs.items():
    print(f"{motif_type}: {info['count']} instances")

# Control motifs
viz.motif_loader.toggle_motif_type('KTURN', visible=True)

# Get current info
info = viz.get_structure_info()
print(f"Current structure: {info['structure']}")
print(f"PDB ID: {info['pdb_id']}")
```

### Batch Processing

```python
# Process multiple structures in a script

structures = ["1S72", "2QWY", "1GID", "3GXA", "1RNK"]

for pdb_id in structures:
    cmd.delete("all")  # Clear previous
    rna_load(pdb_id)
    rna_status()
    # Perform analysis...
    png(f"motif_{pdb_id}.png")
```

---

## 🐛 Getting Help

1. **Check PyMOL Console** for error messages (Windows → Python Console)
2. **Review README.md** in the plugin folder
3. **Verify file structure** matches expected layout
4. **Check JSON database** files are valid JSON (use online JSON validator)

---

## ✅ Verification Checklist

After installation, verify:

- [ ] PyMOL starts without errors
- [ ] Console shows plugin initialization message
- [ ] Commands are recognized (type `rna_load` → should be in menu)
- [ ] Can load structure: `rna_load 1S72` works
- [ ] Can toggle motifs: `rna_toggle KTURN on` works
- [ ] Can check status: `rna_status` shows motifs
- [ ] Motifs appear with correct colors

---

## 📝 Notes

- Plugin loads automatically on PyMOL startup
- Works offline with pre-downloaded structures
- Requires internet only for `fetch` command (PDB ID loading)
- Compatible with PyMOL 1.8+ (free and educational versions)
- No external dependencies (FR3D, DSSR, etc.) required

---

**Ready to visualize RNA motifs!** 🧬✨
