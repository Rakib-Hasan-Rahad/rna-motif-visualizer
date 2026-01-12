"""
RNA Motif Visualizer - Color Configuration Module
Defines unique colors for each motif class for clear visualization.

Supports both RNA 3D Atlas and Rfam motif types with distinct, vibrant colors.

Author: Structural Biology Lab
Version: 2.0.0
"""

# ==============================================================================
# BACKGROUND COLOR CONFIGURATION
# ==============================================================================
# Color for non-motif residues (provides contrast with motif colors)
NON_MOTIF_COLOR = 'gray80'  # Light gray - great contrast with colorful motifs

# ==============================================================================
# MOTIF COLORS
# ==============================================================================
# Define colors for each motif type
# Format: RGB values normalized to 0-1 range
# Colors are vibrant and clearly differentiable from gray80 background

MOTIF_COLORS = {
    # ============================================
    # RNA 3D Motif Atlas motif classes
    # ============================================
    'HL': (1.0, 0.0, 0.0),                  # Bright red - Hairpin loops
    'IL': (0.0, 1.0, 1.0),                  # Bright cyan - Internal loops
    'J3': (1.0, 1.0, 0.0),                  # Bright yellow - 3-way junctions
    'J4': (1.0, 0.0, 1.0),                  # Bright magenta - 4-way junctions
    'J5': (0.0, 1.0, 0.0),                  # Bright green - 5-way junctions
    'J6': (1.0, 0.5, 0.0),                  # Bright orange - 6-way junctions
    'J7': (0.5, 0.5, 1.0),                  # Bright blue - 7-way junctions
    
    # ============================================
    # Rfam motif database - Common RNA motifs
    # ============================================
    # Tetraloops
    'GNRA': (0.0, 0.8, 0.4),                # Teal green
    'UNCG': (0.8, 0.4, 0.0),                # Brown orange
    'CUYG': (0.6, 0.0, 0.6),                # Purple
    
    # Loop motifs
    'T_LOOP': (1.0, 0.4, 0.7),              # Pink
    'T-LOOP': (1.0, 0.4, 0.7),              # Pink (alias)
    'C_LOOP': (0.4, 0.8, 1.0),              # Sky blue
    'C-LOOP': (0.4, 0.8, 1.0),              # Sky blue (alias)
    'U_TURN': (0.9, 0.7, 0.0),              # Gold
    'U-TURN': (0.9, 0.7, 0.0),              # Gold (alias)
    
    # K-turns and variants
    'K_TURN_1': (0.0, 0.6, 1.0),            # Bright blue
    'K-TURN-1': (0.0, 0.6, 1.0),            # Alias
    'K_TURN_2': (0.2, 0.4, 0.8),            # Medium blue
    'K-TURN-2': (0.2, 0.4, 0.8),            # Alias
    'PK_TURN': (0.4, 0.2, 0.8),             # Violet
    'PK-TURN': (0.4, 0.2, 0.8),             # Alias
    
    # Sarcin-ricin motifs
    'SARCIN_RICIN_1': (0.8, 0.2, 0.2),      # Dark red
    'SARCIN-RICIN-1': (0.8, 0.2, 0.2),      # Alias
    'SARCIN_RICIN_2': (1.0, 0.3, 0.3),      # Coral red
    'SARCIN-RICIN-2': (1.0, 0.3, 0.3),      # Alias
    
    # Junctions and angles
    'RIGHT_ANGLE_2': (0.5, 1.0, 0.5),       # Light green
    'RIGHT-ANGLE-2': (0.5, 1.0, 0.5),       # Alias
    'RIGHT_ANGLE_3': (0.3, 0.8, 0.3),       # Medium green
    'RIGHT-ANGLE-3': (0.3, 0.8, 0.3),       # Alias
    'DOCKING_ELBOW': (0.7, 0.5, 0.3),       # Tan
    'DOCKING-ELBOW': (0.7, 0.5, 0.3),       # Alias
    
    # Other structural motifs
    'TANDEM_GA': (0.9, 0.5, 0.9),           # Light magenta
    'TANDEM-GA': (0.9, 0.5, 0.9),           # Alias
    'TWIST_UP': (0.3, 0.7, 0.7),            # Turquoise
    'TWIST-UP': (0.3, 0.7, 0.7),            # Alias
    'DOMAIN_V': (0.8, 0.8, 0.2),            # Olive
    'DOMAIN-V': (0.8, 0.8, 0.2),            # Alias
    
    # Ribosome binding sites
    'RBS_E_COLI': (1.0, 0.6, 0.4),          # Salmon
    'RBS_B_SUBTILIS': (1.0, 0.5, 0.5),      # Light coral
    'RBS_H_PYLORI': (1.0, 0.4, 0.6),        # Rose
    
    # RNA-protein binding motifs
    'SRP_S_DOMAIN': (0.6, 0.8, 0.4),        # Yellow-green
    'AUF1_BINDING': (0.5, 0.6, 0.9),        # Periwinkle
    'HUR_BINDING': (0.7, 0.4, 0.6),         # Mauve
    'CSRA_BINDING': (0.4, 0.7, 0.5),        # Sage
    'ROQUIN_BINDING': (0.6, 0.5, 0.7),      # Lavender
    'VTS1_BINDING': (0.8, 0.6, 0.5),        # Dusty rose
    'CRC_BINDING': (0.5, 0.8, 0.7),         # Mint
    
    # Terminators
    'TERMINATOR1': (0.9, 0.3, 0.5),         # Raspberry
    'TERMINATOR2': (0.7, 0.3, 0.4),         # Burgundy
    
    # Other
    'ANYA': (0.6, 0.7, 0.8),                # Steel blue
    'TRIT': (0.8, 0.7, 0.5),                # Khaki
    'UMAC': (0.5, 0.5, 0.8),                # Slate blue
    'UAA_GAN': (0.7, 0.8, 0.6),             # Pale olive
    'VAPC_TARGET': (0.9, 0.6, 0.6),         # Light salmon
}

# Backup color for undefined motif types
DEFAULT_COLOR = (1.0, 0.5, 0.0)  # Bright orange

# PyMOL color names for common types
PYMOL_COLOR_NAMES = {
    # Atlas types
    'HL': 'red',
    'IL': 'cyan',
    'J3': 'yellow',
    'J4': 'magenta',
    'J5': 'green',
    'J6': 'orange',
    'J7': 'blue',
    # Rfam types
    'GNRA': 'teal',
    'T_LOOP': 'pink',
    'K_TURN_1': 'marine',
    'SARCIN_RICIN_1': 'firebrick',
}


def get_color(motif_type):
    """
    Get RGB color tuple for a motif type.
    
    Args:
        motif_type (str): Motif type identifier
    
    Returns:
        tuple: RGB color values (0-1 range)
    """
    # Normalize: uppercase and convert dashes to underscores
    normalized = str(motif_type).upper().replace('-', '_')
    return MOTIF_COLORS.get(normalized, DEFAULT_COLOR)


def get_color_name(motif_type):
    """
    Get PyMOL color name for a motif type.
    
    Args:
        motif_type (str): Motif type identifier
    
    Returns:
        str: PyMOL color name
    """
    normalized = str(motif_type).upper().replace('-', '_')
    return PYMOL_COLOR_NAMES.get(normalized, 'gray')


def set_motif_color_in_pymol(cmd, object_name, motif_type):
    """
    Set color for a PyMOL object based on motif type.
    
    Args:
        cmd: PyMOL cmd module
        object_name (str): Name of the PyMOL object
        motif_type (str): Type of motif
    """
    try:
        color = get_color(motif_type)
        # Create custom color name
        color_name = f'motif_{motif_type.replace("-", "_")}'
        cmd.set_color(color_name, color)
        cmd.color(color_name, object_name)
    except Exception as e:
        print(f"Warning: Could not set color for {object_name}: {e}")


# Summary of available motifs and their colors (for legend display)
MOTIF_LEGEND = {
    # RNA 3D Atlas
    'HL': {'color': 'red', 'description': 'Hairpin loops (Atlas)'},
    'IL': {'color': 'cyan', 'description': 'Internal loops (Atlas)'},
    'J3': {'color': 'yellow', 'description': '3-way junctions (Atlas)'},
    'J4': {'color': 'magenta', 'description': '4-way junctions (Atlas)'},
    'J5': {'color': 'green', 'description': '5-way junctions (Atlas)'},
    'J6': {'color': 'orange', 'description': '6-way junctions (Atlas)'},
    'J7': {'color': 'blue', 'description': '7-way junctions (Atlas)'},
    # Rfam
    'GNRA': {'color': 'teal', 'description': 'GNRA tetraloop (Rfam)'},
    'T_LOOP': {'color': 'pink', 'description': 'T-loop motif (Rfam)'},
    'C_LOOP': {'color': 'sky blue', 'description': 'C-loop motif (Rfam)'},
    'K_TURN_1': {'color': 'marine', 'description': 'K-turn variant 1 (Rfam)'},
    'K_TURN_2': {'color': 'blue', 'description': 'K-turn variant 2 (Rfam)'},
    'SARCIN_RICIN_1': {'color': 'firebrick', 'description': 'Sarcin-ricin loop (Rfam)'},
    'UNCG': {'color': 'brown', 'description': 'UNCG tetraloop (Rfam)'},
}


def set_background_color(color_name):
    """
    Change the non-motif background color.
    
    Args:
        color_name (str): PyMOL color name (e.g., 'gray80', 'white', 'lightgray')
    """
    global NON_MOTIF_COLOR
    NON_MOTIF_COLOR = color_name


def get_background_color():
    """Get the current non-motif background color."""
    return NON_MOTIF_COLOR


def register_all_colors(cmd):
    """
    Pre-register all motif colors in PyMOL.
    
    Args:
        cmd: PyMOL cmd module
    """
    for motif_type, color_rgb in MOTIF_COLORS.items():
        color_name = f'motif_{motif_type.replace("-", "_")}'
        try:
            cmd.set_color(color_name, color_rgb)
        except:
            pass


def print_color_legend(loaded_motifs=None):
    """
    Print a color legend to the console.
    
    Args:
        loaded_motifs: Optional dict of currently loaded motifs to show only relevant colors
    """
    print("\n" + "=" * 60)
    print("  RNA MOTIF COLOR LEGEND")
    print("=" * 60)
    
    if loaded_motifs:
        # Show only colors for loaded motifs
        print("  Currently loaded motifs:")
        print("-" * 60)
        print(f"  {'MOTIF TYPE':<15} {'COLOR':<15} {'RGB'}")
        print("-" * 60)
        
        for motif_type in sorted(loaded_motifs.keys()):
            color = get_color(motif_type)
            r, g, b = int(color[0]*255), int(color[1]*255), int(color[2]*255)
            color_name = PYMOL_COLOR_NAMES.get(motif_type.upper().replace('-', '_'), 'custom')
            print(f"  {motif_type:<15} {color_name:<15} ({r}, {g}, {b})")
    else:
        # Show all available colors
        print("\n  RNA 3D Atlas Motifs (HL, IL, Junctions):")
        print("-" * 60)
        print(f"  {'MOTIF':<12} {'COLOR':<12} {'RGB':<18} {'DESCRIPTION'}")
        print("-" * 60)
        
        atlas_motifs = ['HL', 'IL', 'J3', 'J4', 'J5', 'J6', 'J7']
        for mt in atlas_motifs:
            color = MOTIF_COLORS.get(mt, DEFAULT_COLOR)
            r, g, b = int(color[0]*255), int(color[1]*255), int(color[2]*255)
            desc = MOTIF_LEGEND.get(mt, {}).get('description', '')
            color_name = PYMOL_COLOR_NAMES.get(mt, 'custom')
            print(f"  {mt:<12} {color_name:<12} ({r:>3}, {g:>3}, {b:>3})  {desc}")
        
        print("\n  Rfam Named Motifs (Tetraloops, K-turns, etc.):")
        print("-" * 60)
        
        rfam_motifs = ['GNRA', 'UNCG', 'T_LOOP', 'C_LOOP', 'K_TURN_1', 'K_TURN_2', 'SARCIN_RICIN_1', 'U_TURN']
        for mt in rfam_motifs:
            if mt in MOTIF_COLORS:
                color = MOTIF_COLORS[mt]
                r, g, b = int(color[0]*255), int(color[1]*255), int(color[2]*255)
                desc = MOTIF_LEGEND.get(mt, {}).get('description', '')
                color_name = PYMOL_COLOR_NAMES.get(mt, 'custom')
                display_name = mt.replace('_', '-')
                print(f"  {display_name:<12} {color_name:<12} ({r:>3}, {g:>3}, {b:>3})  {desc}")
    
    print("\n" + "-" * 60)
    print("  Background (non-motif residues): " + get_background_color())
    print("=" * 60 + "\n")
