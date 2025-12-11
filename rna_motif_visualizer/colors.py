"""
RNA Motif Visualizer - Color Configuration Module
Defines unique colors for each motif class for clear visualization.
"""

# Define colors for each motif type
# Format: RGB values normalized to 0-1 range
MOTIF_COLORS = {
    'KTURN': (1.0, 0.2, 0.2),           # Bright red
    'AMINOR': (0.2, 0.8, 1.0),          # Cyan
    'GNRA': (1.0, 1.0, 0.0),            # Yellow
    'KL_MOTIF': (0.8, 0.2, 1.0),        # Magenta
    'SARCIN_RICIN': (0.2, 1.0, 0.5),    # Spring green
    'KINK_TURN': (1.0, 0.6, 0.0),       # Orange
    'HAIRPIN': (0.5, 1.0, 0.2),         # Lime green
    'BULGE': (1.0, 0.5, 0.8),           # Pink
    'INTERNAL_LOOP': (0.4, 0.8, 1.0),   # Light blue
    'JUNCTION': (1.0, 0.8, 0.2),        # Gold
}

# Backup colors if a motif type is not defined
DEFAULT_COLOR = (0.7, 0.7, 0.7)  # Gray

# PyMOL color names for reference
PYMOL_COLOR_NAMES = {
    'KTURN': 'red',
    'AMINOR': 'cyan',
    'GNRA': 'yellow',
    'KL_MOTIF': 'magenta',
    'SARCIN_RICIN': 'green',
    'KINK_TURN': 'orange',
    'HAIRPIN': 'lime',
    'BULGE': 'pink',
    'INTERNAL_LOOP': 'lightblue',
    'JUNCTION': 'gold',
}


def get_color(motif_type):
    """
    Get RGB color tuple for a motif type.
    
    Args:
        motif_type (str): Motif type identifier (e.g., 'KTURN')
    
    Returns:
        tuple: RGB color values (0-1 range)
    """
    return MOTIF_COLORS.get(motif_type, DEFAULT_COLOR)


def get_color_name(motif_type):
    """
    Get PyMOL color name for a motif type.
    
    Args:
        motif_type (str): Motif type identifier (e.g., 'KTURN')
    
    Returns:
        str: PyMOL color name
    """
    return PYMOL_COLOR_NAMES.get(motif_type, 'gray')


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
        cmd.set_color(f'motif_{motif_type}', color)
        cmd.color(f'motif_{motif_type}', object_name)
    except Exception as e:
        print(f"Warning: Could not set color for {object_name}: {e}")


# Summary of available motifs and their colors
MOTIF_LEGEND = {
    'KTURN': {'color': 'red', 'description': 'K-turn motifs'},
    'AMINOR': {'color': 'cyan', 'description': 'A-minor interactions'},
    'GNRA': {'color': 'yellow', 'description': 'GNRA tetraloops'},
    'KL_MOTIF': {'color': 'magenta', 'description': 'KL motifs'},
    'SARCIN_RICIN': {'color': 'green', 'description': 'Sarcin-ricin loops'},
    'KINK_TURN': {'color': 'orange', 'description': 'Kink-turn motifs'},
    'HAIRPIN': {'color': 'lime', 'description': 'Hairpin structures'},
    'BULGE': {'color': 'pink', 'description': 'Bulge loops'},
    'INTERNAL_LOOP': {'color': 'lightblue', 'description': 'Internal loops'},
    'JUNCTION': {'color': 'gold', 'description': 'RNA junctions'},
}
