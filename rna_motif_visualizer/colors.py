"""
RNA Motif Visualizer - Color Configuration Module
Defines unique colors for each motif class for clear visualization.
"""

# ==============================================================================
# BACKGROUND COLOR CONFIGURATION
# ==============================================================================
# Color for non-motif residues (provides contrast with motif colors)
# Options: 'gray80', 'white', 'lightgray', 'gray', or custom RGB values
NON_MOTIF_COLOR = 'gray80'  # Light gray - great contrast with colorful motifs

# You can also use PyMOL color names like:
# 'white', 'gray', 'gray40', 'gray60', 'gray80', 'lightgray'
# ==============================================================================

# Define colors for each motif type
# Format: RGB values normalized to 0-1 range
# Colors are vibrant and clearly differentiable from gray80 background
MOTIF_COLORS = {
    # RNA 3D Motif Atlas motif classes
    'HL': (1.0, 0.0, 0.0),                  # Bright red
    'IL': (0.0, 1.0, 1.0),                  # Bright cyan
    'J3': (1.0, 1.0, 0.0),                  # Bright yellow
    'J4': (1.0, 0.0, 1.0),                  # Bright magenta
    'J5': (0.0, 1.0, 0.0),                  # Bright green
    'J6': (1.0, 0.5, 0.0),                  # Bright orange
    'J7': (0.5, 0.5, 1.0),                  # Bright blue
}

# Backup colors if a motif type is not defined
DEFAULT_COLOR = (1.0, 0.5, 0.0)  # Bright orange

# PyMOL color names for reference
PYMOL_COLOR_NAMES = {
    'HL': 'red',
    'IL': 'cyan',
    'J3': 'yellow',
    'J4': 'magenta',
    'J5': 'green',
    'J6': 'orange',
    'J7': 'blue',
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
    'HL': {'color': 'red', 'description': 'Hairpin loops (Atlas)'},
    'IL': {'color': 'cyan', 'description': 'Internal loops (Atlas)'},
    'J3': {'color': 'yellow', 'description': '3-way junctions (Atlas)'},
    'J4': {'color': 'magenta', 'description': '4-way junctions (Atlas)'},
    'J5': {'color': 'green', 'description': '5-way junctions (Atlas)'},
    'J6': {'color': 'orange', 'description': '6-way junctions (Atlas)'},
    'J7': {'color': 'blue', 'description': '7-way junctions (Atlas)'},
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
