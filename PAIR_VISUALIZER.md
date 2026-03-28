# RNA Base-Pair Visualizer (`rmv_pair`)

A PyMOL command for visualizing individual RNA base pairs with **Leontis-Westhof edge labels** (Watson-Crick, Hoogsteen, Sugar).

---

## Quick Start

```
rmv_pair 3j6y_2S_681_2S_696
```

This single command will:
1. Fetch PDB `3j6y` (if not already loaded)
2. Auto-detect the nucleotide identities (e.g. U, C) from the structure
3. Remove solvent molecules
4. Create a new PyMOL object containing only residues 681 and 696 from chain 2S
5. Display both residues as sticks (residue 681 in yellow, 696 in cyan)
6. Place **W**, **H**, **S** edge labels on each base at the correct atomic positions
7. Zoom the camera to the pair

---

## Descriptor Format

```
pdbid_chain1_resnum1_chain2_resnum2
```

| Field      | Description                          | Example |
|------------|--------------------------------------|---------|
| `pdbid`    | 4-character PDB identifier           | `3j6y`  |
| `chain1`   | Chain ID for residue 1 (can be multi-character) | `2S`    |
| `resnum1`  | Residue number for residue 1         | `681`   |
| `chain2`   | Chain ID for residue 2               | `2S`    |
| `resnum2`  | Residue number for residue 2         | `696`   |

Nucleotide identities (A, G, C, U) are **auto-detected** from the PDB structure.

### Examples

```
# Same chain, different residues
rmv_pair 3j6y_2S_681_2S_696

# Different chains
rmv_pair 1s72_A_100_B_200

# Simple single-character chain
rmv_pair 5lzs_5_1582_5_1610
```

---

## Command Options

```
rmv_pair <descriptor> [, label_size=24] [, label_color=black]
         [, color1=yellow] [, color2=cyan]
         [, zoom_buffer=8] [, bg_style=cartoon]
```

| Option        | Default    | Description                                     |
|---------------|------------|-------------------------------------------------|
| `label_size`  | `24`       | Font size for W/H/S labels                      |
| `label_color` | `black`    | Color of the edge labels                        |
| `color1`      | `yellow`   | Stick color for residue 1                       |
| `color2`      | `cyan`     | Stick color for residue 2                       |
| `zoom_buffer` | `8`        | Zoom buffer in Angstroms around the pair         |
| `bg_style`    | `cartoon`  | Background structure display (`cartoon` or `none`) |

### Customization Examples

```
# Larger labels, red/blue coloring
rmv_pair 3j6y_2S_681_2S_696, label_size=30, color1=red, color2=blue

# Hide background structure entirely
rmv_pair 3j6y_2S_681_2S_696, bg_style=none

# White labels on dark background
rmv_pair 3j6y_2S_681_2S_696, label_color=white
```

---

## Batch Mode

To visualize multiple base pairs at once, create a text file with one descriptor per line:

```
# File: my_pairs.txt
# Pairs from 3j6y
3j6y_2S_681_2S_696
3j6y_2S_700_2S_715

# Pairs from 5lzs
5lzs_5_1582_5_1610
```

Then run:

```
rmv_pair_batch /path/to/my_pairs.txt
```

Lines starting with `#` are treated as comments and blank lines are ignored.

---

## Edge Label Definitions

The **W** (Watson-Crick), **H** (Hoogsteen), and **S** (Sugar) labels are placed at the centroid of the atoms that define each edge, following the Leontis-Westhof classification.

### Adenine (A)
| Edge | Atoms              |
|------|---------------------|
| W    | N1, C2, N6         |
| H    | C5, C6, N7, C8     |
| S    | N3, C2             |

### Guanine (G)
| Edge | Atoms              |
|------|---------------------|
| W    | O6, N1, N2         |
| H    | C5, N7, C8         |
| S    | N3, C2, N2         |

### Cytosine (C)
| Edge | Atoms              |
|------|---------------------|
| W    | N3, O2, N4         |
| H    | C5, C6             |
| S    | N1, C2, O2         |

### Uracil (U)
| Edge | Atoms              |
|------|---------------------|
| W    | O4, N3, O2         |
| H    | C5, C6             |
| S    | N1, C2, O2         |

---

## What Gets Created in PyMOL

For a command like `rmv_pair 3j6y_2S_681_2S_696`, the following PyMOL objects are created:

| Object Name                       | Type        | Description                    |
|-----------------------------------|-------------|--------------------------------|
| `pair_3j6y_2S_681_696`           | Object      | Stick representation of the pair |
| `lbl_3j6y_2S_681_W`              | Pseudoatom  | Watson-Crick label for resi 681 |
| `lbl_3j6y_2S_681_H`              | Pseudoatom  | Hoogsteen label for resi 681    |
| `lbl_3j6y_2S_681_S`              | Pseudoatom  | Sugar label for resi 681        |
| `lbl_3j6y_2S_696_W`              | Pseudoatom  | Watson-Crick label for resi 696 |
| `lbl_3j6y_2S_696_H`              | Pseudoatom  | Hoogsteen label for resi 696    |
| `lbl_3j6y_2S_696_S`              | Pseudoatom  | Sugar label for resi 696        |

You can toggle visibility of any of these objects in the PyMOL object panel.

---

## Troubleshooting

| Problem                          | Solution                                              |
|----------------------------------|-------------------------------------------------------|
| "no atoms found for selection"   | Verify chain ID and residue number exist in the PDB   |
| "could not detect residue name"  | The residue may not be a standard nucleotide (A/G/C/U) |
| Labels not visible               | Try `set label_size, 30` or change `label_color`      |
| Wrong edge positions             | Ensure the residue is a standard RNA base (A/G/C/U)   |
| Chain ID with spaces             | The plugin handles multi-character chains like `2S` automatically |
| Fetch fails                      | Check internet connection; or `fetch <pdbid>` manually first |
