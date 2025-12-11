# RNA Motif Visualizer - Usage Examples

This file contains ready-to-use PyMOL commands for the RNA Motif Visualizer plugin.

Copy and paste these commands directly into the PyMOL console.

---

## Basic Usage

### Load a Structure and Show All Motifs
```python
rna_load 1S72
rna_status
```

### Load from Local File
```python
rna_load /path/to/structure.pdb
# or on Windows:
rna_load C:\Users\YourName\Downloads\structure.cif
```

---

## Showing/Hiding Specific Motifs

### Show Only K-Turns
```python
rna_load 1S72
rna_toggle KTURN on
rna_toggle AMINOR off
rna_toggle GNRA off
rna_toggle KL_MOTIF off
rna_toggle SARCIN_RICIN off
rna_toggle KINK_TURN off
rna_toggle HAIRPIN off
rna_toggle BULGE off
rna_toggle INTERNAL_LOOP off
rna_toggle JUNCTION off
```

### Show Only GNRA Tetraloops
```python
rna_load 1S72
rna_toggle GNRA on
rna_toggle KTURN off
rna_toggle AMINOR off
```

### Show K-Turns and A-Minors Together
```python
rna_load 1S72
rna_toggle KTURN on
rna_toggle AMINOR on
rna_toggle GNRA off
rna_toggle KL_MOTIF off
rna_toggle SARCIN_RICIN off
```

---

## Zooming and Highlighting

### Zoom to K-Turns
```python
rna_load 1S72
rna_toggle KTURN on
select kturn_only, KTURN_ALL
zoom kturn_only
```

### Zoom to GNRA Tetraloops
```python
rna_load 1S72
rna_toggle GNRA on
select gnra_only, GNRA_ALL
zoom gnra_only
```

### Highlight A-Minors with Increased Stick Size
```python
rna_load 1S72
rna_toggle AMINOR on
show sticks, AMINOR_ALL
set stick_radius, 0.3, AMINOR_ALL
```

---

## Visualization Styles

### Show as Cartoon (Secondary Structure)
```python
rna_load 1S72
hide everything
show cartoon
rna_toggle KTURN on
show sticks, KTURN_ALL
color red, KTURN_ALL
```

### Show as Sticks and Cartoon
```python
rna_load 1S72
show cartoon
show sticks
rna_toggle GNRA on
color yellow, GNRA_ALL
```

### Show Structure with Surface
```python
rna_load 1S72
show cartoon
show surface
rna_toggle KTURN on
show sticks, KTURN_ALL
set transparency, 0.7
```

---

## Comparing Multiple Structures

### Load Two Structures
```python
rna_load 1S72
rna_status

# In a new window or session:
rna_load 2QWY
rna_status
```

### Load and Compare Motif Distribution
```python
# Load first
rna_load 1S72
print("=== Structure 1 ===")
rna_status

# Clear and load second
delete all
rna_load 2QWY
print("=== Structure 2 ===")
rna_status
```

---

## Working with Motif Objects Directly

### Select Individual Motif Type
```python
rna_load 1S72
select my_kturn, KTURN_ALL
color red, my_kturn
```

### Create Sub-Selection of One Motif
```python
rna_load 1S72
# Create custom selection for specific residues
select kturn_resi77_82, chain A and resi 77-82
color orange, kturn_resi77_82
```

### Hide Background, Show Only One Motif
```python
rna_load 1S72
hide everything
rna_toggle KTURN on
show sticks, KTURN_ALL
show cartoon, KTURN_ALL
center KTURN_ALL
zoom KTURN_ALL
```

---

## Color Customization

### Change Motif Color
```python
rna_load 1S72
# Change K-turn color to orange
rna_toggle KTURN on
color orange, KTURN_ALL
```

### Rainbow Colors for Multiple Motifs
```python
rna_load 1S72
rna_toggle KTURN on
rna_toggle AMINOR on
rna_toggle GNRA on
color red, KTURN_ALL
color blue, AMINOR_ALL
color yellow, GNRA_ALL
```

---

## Creating Publication Figures

### Simple, Clean Figure
```python
rna_load 1S72
hide everything
show cartoon, 1S72
rna_toggle KTURN on
show sticks, KTURN_ALL
color red, KTURN_ALL
bg_color white
png motif_figure.png, dpi=300
```

### High-Resolution Figure with Specific Angle
```python
rna_load 1S72
show cartoon
show sticks
rna_toggle GNRA on
color yellow, GNRA_ALL
orient
rotate x, 45
rotate y, 30
bg_color white
png gnra_figure.png, width=1024, height=768, dpi=300
```

### Figure with Multiple Motif Types
```python
rna_load 1S72
show cartoon
rna_toggle KTURN on
rna_toggle GNRA on
rna_toggle AMINOR on
color red, KTURN_ALL
color yellow, GNRA_ALL
color cyan, AMINOR_ALL
bg_color white
set transparency, 0
png multi_motif.png, dpi=300
```

---

## Batch Processing

### Process Multiple PDB IDs
```python
# In PyMOL console (one-liner compatible):
for pdb in ['1S72', '2QWY', '1GID']:
    cmd.delete('all')
    cmd.fetch(pdb)
    # Your analysis here
```

### Export Motif Information
```python
rna_load 1S72
rna_status()
# Copy output for analysis or documentation
```

---

## Advanced Selections

### Select All Motifs in a Specific Chain
```python
rna_load 1S72
# Select all motifs in chain A
select all_motifs_A, chain A and (KTURN_ALL or AMINOR_ALL or GNRA_ALL)
show sticks, all_motifs_A
color white, all_motifs_A
```

### Distance Analysis Between Motifs
```python
rna_load 1S72
rna_toggle KTURN on
rna_toggle AMINOR on
# Show distance
distance dist_k_a, KTURN_ALL, AMINOR_ALL
```

### Select Nearby Residues
```python
rna_load 1S72
rna_toggle KTURN on
# Select residues within 5 Angstroms of K-turns
select nearby, byres (all within 5 of KTURN_ALL)
show sticks, nearby
```

---

## Error Recovery

### If Plugin Doesn't Load
```python
# Restart PyMOL, then check console for messages
# If still issues, try:
import rna_motif_visualizer
print("Plugin imported successfully")
```

### If Motifs Don't Show
```python
# Verify structure loaded
get_names()  # Should show your structure name

# Verify motifs loaded
rna_status  # Should show motif info

# Try refreshing
rna_toggle KTURN off
rna_toggle KTURN on
```

### Clear Everything and Start Fresh
```python
delete all
# Now ready for new structure
rna_load 1S72
```

---

## Tips & Tricks

### Tip 1: Quick Motif Toggle Script
Create a text file with your favorite toggles:
```
rna_load 1S72
rna_toggle KTURN on
rna_toggle GNRA on
rna_toggle AMINOR off
rna_status
```
Then paste all at once into PyMOL console.

### Tip 2: Save Your View
```python
# After setting up visualization:
png my_scene.png
# Use File → Save Scene to preserve camera angle
save my_scene.pse
```

### Tip 3: Compare Structures Side-by-Side
```python
# Load in split screen:
# Window 1:
rna_load 1S72
rna_toggle KTURN on

# Window 2 (Window → Split Viewport):
rna_load 2QWY
rna_toggle KTURN on

# Rotate both together with mouse
```

### Tip 4: Create Animation
```python
rna_load 1S72
rna_toggle KTURN on
# Rotate structure
orient
for i in range(360):
    rotate x, 1
    png frame_%04d.png % i
```

---

## Troubleshooting Specific Errors

### "rna_load is not a valid PyMOL command"
→ Plugin didn't load. Restart PyMOL and check console for errors.

### "No motifs found for this structure"
→ Normal if PDB ID not in database. Add your own motif data!

### "Invalid PDB ID format"
→ PDB IDs must be exactly 4 characters. Use: `rna_load 1S72` (not `1s72a`)

### "File not found"
→ Use absolute paths: `/path/to/file.pdb` or `C:\full\path\file.pdb`

---

## Example Results

Running these commands produces:

```
Structure: 1S72
PDB ID: 1S72

Loaded Motifs (10):
  KTURN                 ( 2 instances) ✓ visible
  AMINOR                ( 2 instances) ✓ visible
  GNRA                  ( 2 instances) ✓ visible
  KL_MOTIF              ( 1 instances) ✓ visible
  SARCIN_RICIN          ( 1 instances) ✓ visible
  KINK_TURN             ( 1 instances) ✓ visible
  HAIRPIN               ( 2 instances) ✓ visible
  BULGE                 ( 2 instances) ✓ visible
  INTERNAL_LOOP         ( 2 instances) ✓ visible
  JUNCTION              ( 2 instances) ✓ visible
```

---

## More Examples

### Scientific Analysis Workflow
```python
# 1. Load structure
rna_load 1S72

# 2. Examine motif composition
rna_status

# 3. Focus on specific motif class
rna_toggle GNRA on
rna_toggle KTURN off

# 4. Analyze geometry
select gnra_study, GNRA_ALL
# Use PyMOL measurements tools

# 5. Save results
png gnra_analysis.png
```

### Teaching Demonstration
```python
# Show overall structure
rna_load 1S72
show cartoon

# Gradually reveal motifs
rna_toggle KTURN on
# Discuss K-turns...

rna_toggle GNRA on
# Discuss GNRA tetraloops...

rna_toggle AMINOR on
# Discuss A-minor interactions...
```

---

## Next Steps

- Try different structures (1S72, 2QWY, 1GID, 3GXA, 1RNK)
- Explore each motif type
- Create figures for publications
- Add your own motif annotations to the database
- Share findings with colleagues!

---

**Happy exploring!** 🧬✨
