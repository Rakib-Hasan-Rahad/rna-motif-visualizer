# RNA Motif Visualizer - Developer Guide & API Reference

## 📚 Architecture Overview

```
PyMOL Interface (cmd module)
        ↓
     GUI Layer (gui.py)
        ↓
  Visualization Manager (loader.py)
        ├── Structure Loader → PDB Download/Local Load
        └── Motif Loader
              ├── Database Parser (utils/parser.py)
              ├── Motif Selector (utils/selectors.py)
              └── Color Manager (colors.py)
```

---

## 🔧 Module Reference

### 1. `plugin.py` - Main Entry Point

**Function:** `__init_plugin__(app)`

Called when PyMOL loads the plugin.

```python
def __init_plugin__(app):
    """Initialize plugin in PyMOL."""
```

**Responsibilities:**
- Initialize logger
- Register PyMOL commands
- Display welcome message

---

### 2. `gui.py` - User Interface

**Main Class:** `MotifVisualizerGUI`

```python
class MotifVisualizerGUI:
    def __init__(self):
        """Initialize GUI components."""
    
    def load_structure_action(self, pdb_id_or_path: str, chain: str = '0', background_color: str = None) -> None:
        """Load structure and visualize motifs on specified chain."""
    
    def toggle_motif_action(self, motif_type: str, visible: bool) -> None:
        """Toggle visibility of a motif type."""
    
    def get_available_motifs(self) -> list:
        """Get list of available motif types."""
    
    def get_motif_info(self, motif_type: str) -> dict:
        """Get information about a motif type."""
    
    def print_status(self) -> None:
        """Print current status to console."""
```

**Registered PyMOL Commands:**
- `rna_load(pdb_id_or_path, chain='0', bg_color=None)` - Load structure with optional chain and background color
- `rna_toggle(motif_type, visible)` - Toggle visibility
- `rna_status()` - Show status

---

### 3. `loader.py` - Core Loading Logic

#### Class: `StructureLoader`

```python
class StructureLoader:
    def __init__(self, cmd):
        """Initialize with PyMOL cmd module."""
    
    def load_structure(self, pdb_id_or_path: str) -> str:
        """Load structure from PDB ID or local file."""
        # Returns: structure_name (str) or None
    
    def get_current_structure(self) -> str:
        """Get name of currently loaded structure."""
    
    def get_current_pdb_id(self) -> str:
        """Get PDB ID of current structure."""
```

#### Class: `MotifLoader`

```python
class MotifLoader:
    def __init__(self, cmd, database_dir: str):
        """Initialize motif loader."""
    
    def load_motifs(self, structure_name: str, pdb_id: str) -> dict:
        """Load all motifs for a structure."""
        # Returns: {motif_type: {'object_name': str, 'count': int, 'visible': bool}}
    
    def toggle_motif_type(self, motif_type: str, visible: bool) -> bool:
        """Toggle visibility of a motif type."""
    
    def get_loaded_motifs(self) -> dict:
        """Get dictionary of loaded motifs."""
    
    def clear_motifs(self) -> None:
        """Clear all motif objects."""
    
    def reload_motifs(self, structure_name: str, pdb_id: str) -> dict:
        """Reload motifs (clear and reload)."""
```

#### Class: `VisualizationManager`

High-level manager for entire workflow:

```python
class VisualizationManager:
    def __init__(self, cmd, database_dir: str):
        """Initialize visualization manager."""
    
    def setup_clean_visualization(self, structure_name: str, chain: str = '0', 
                                  background_color: str = None) -> None:
        """Set up clean RNA visualization: hide all, select chain, show cartoon, color uniformly."""
    
    def load_and_visualize(self, pdb_id_or_path: str, chain: str = '0', 
                          background_color: str = None) -> dict:
        """Complete workflow: load structure and visualize motifs on specified chain."""
    
    def get_structure_info(self) -> dict:
        """Get current structure and motif info."""
```

**Key Features:**
- Implements clean PyMOL visualization workflow
- Supports custom chain selection
- Allows custom background color for RNA backbone
- Overlays motifs with distinct colors on neutral background

---

### 4. `colors.py` - Color Management

```python
# Color dictionaries
MOTIF_COLORS: dict              # RGB tuples (0-1 range)
PYMOL_COLOR_NAMES: dict         # PyMOL color names
MOTIF_LEGEND: dict              # Description metadata

# Functions
def get_color(motif_type: str) -> tuple:
    """Get RGB color for a motif type."""

def get_color_name(motif_type: str) -> str:
    """Get PyMOL color name for a motif type."""

def set_motif_color_in_pymol(cmd, object_name: str, motif_type: str) -> None:
    """Set color for a PyMOL object."""
```

---

### 5. `utils/parser.py` - Data Parsing

#### Class: `MotifDatabaseParser`

```python
class MotifDatabaseParser:
    def __init__(self, database_dir: str):
        """Initialize parser."""
    
    def load_motif_file(self, motif_type: str) -> dict:
        """Load motif annotations from JSON file."""
    
    def get_motifs_for_pdb(self, pdb_id: str, motif_type: str) -> list:
        """Get motif instances for a PDB ID."""
    
    def list_available_motif_types(self) -> list:
        """List all available motif types."""
```

#### Class: `PDBParser`

```python
class PDBParser:
    @staticmethod
    def extract_pdb_id(filepath_or_id: str) -> str:
        """Extract PDB ID from file or return if already ID."""
    
    @staticmethod
    def is_valid_pdb_id(pdb_id: str) -> bool:
        """Check if string is valid PDB ID."""
```

#### Class: `SelectionParser`

```python
class SelectionParser:
    @staticmethod
    def create_selection_string(chain: str, residues: list) -> str:
        """Create PyMOL selection string from chain and residues."""
    
    @staticmethod
    def create_detailed_selection(chain: str, residues: list) -> str:
        """Create detailed PyMOL selection string."""
```

---

### 6. `utils/selectors.py` - PyMOL Selection Management

```python
class MotifSelector:
    def __init__(self, cmd):
        """Initialize with PyMOL cmd module."""
    
    def create_motif_object(self, structure_name: str, motif_type: str, 
                           motif_id: str, chain: str, residues: list) -> str:
        """Create single motif object in PyMOL."""
    
    def create_motif_class_object(self, structure_name: str, motif_type: str, 
                                 motif_list: list) -> str:
        """Create combined object for all motifs of a type."""
    
    def toggle_object_visibility(self, obj_name: str, visible: bool) -> None:
        """Toggle visibility of an object."""
    
    def delete_object(self, obj_name: str) -> None:
        """Delete an object."""
    
    def highlight_object(self, obj_name: str) -> None:
        """Highlight a motif object."""
    
    def get_all_motif_objects(self) -> list:
        """Get names of all motif objects."""
```

---

### 7. `utils/logger.py` - Logging System

```python
class PluginLogger:
    def __init__(self, use_pymol_console: bool = False):
        """Initialize logger."""
    
    def set_log_file(self, filepath: str) -> None:
        """Set optional log file path."""
    
    def info(self, message: str) -> None:
        """Log info message."""
    
    def warning(self, message: str) -> None:
        """Log warning message."""
    
    def error(self, message: str) -> None:
        """Log error message."""
    
    def debug(self, message: str) -> None:
        """Log debug message."""
    
    def success(self, message: str) -> None:
        """Log success message."""

# Global functions
def get_logger() -> PluginLogger:
    """Get global logger instance."""

def initialize_logger(use_pymol_console: bool = False, 
                     log_file: str = None) -> PluginLogger:
    """Initialize global logger."""
```

---

## 📊 Data Structures

### Motif Database JSON Format

```json
{
  "PDB_ID": [
    {
      "chain": "A",
      "residues": [77, 78, 79, 80, 81, 82],
      "motif_id": "K1",
      "description": "K-turn motif",
      "source": "Database name"
    }
  ]
}
```

### Loaded Motifs Dictionary

```python
{
  'KTURN': {
    'object_name': 'KTURN_ALL',
    'count': 2,
    'visible': True
  },
  'AMINOR': {
    'object_name': 'AMINOR_ALL',
    'count': 2,
    'visible': True
  }
}
```

### Structure Info Dictionary

```python
{
  'structure': 'structure_name',
  'pdb_id': '1S72',
  'motifs': {
    'KTURN': {...},
    'AMINOR': {...}
  }
}
```

---

## 🔌 Extending the Plugin

### Adding a New Motif Type

#### Step 1: Create Database File

Create `motif_database/mynewmotif.json`:

```json
{
  "1ABC": [
    {
      "chain": "A",
      "residues": [10, 11, 12, 13, 14, 15],
      "motif_id": "M1",
      "description": "My new motif type",
      "source": "My research"
    }
  ],
  "2DEF": [
    {
      "chain": "B",
      "residues": [20, 21, 22, 23, 24, 25],
      "motif_id": "M1",
      "description": "Another instance",
      "source": "My research"
    }
  ]
}
```

#### Step 2: Register Color in `colors.py`

```python
# Add to MOTIF_COLORS
MOTIF_COLORS = {
    'MYNEWMOTIF': (0.5, 0.8, 0.3),  # Your RGB color
    # ... existing entries
}

# Add to PYMOL_COLOR_NAMES
PYMOL_COLOR_NAMES = {
    'MYNEWMOTIF': 'springgreen',  # PyMOL color name
    # ... existing entries
}

# Add to MOTIF_LEGEND
MOTIF_LEGEND = {
    'MYNEWMOTIF': {
        'color': 'springgreen',
        'description': 'Description of your new motif'
    },
    # ... existing entries
}
```

#### Step 3: Use the New Motif

```python
# Plugin auto-discovers from JSON files!
rna_load 1ABC
rna_toggle MYNEWMOTIF on
rna_status
```

### Adding Custom PyMOL Commands

Edit `gui.py`, add to `initialize_gui()`:

```python
def my_custom_command(arg1, arg2):
    """My custom command."""
    gui = get_gui()
    # ... implementation

cmd.extend('rna_custom', my_custom_command)
```

Use in PyMOL:
```python
rna_custom arg1 arg2
```

### Custom Selection Logic

Modify `utils/selectors.py`:

```python
def create_custom_selection(self, structure_name: str, 
                          motif_type: str, custom_params: dict) -> str:
    """Create selection with custom parameters."""
    # ... implementation
```

---

## 🧪 Testing

### Manual Testing Workflow

```python
# Test 1: Load structure
rna_load 1S72
# Verify: structure appears in PyMOL viewport

# Test 2: Check motifs loaded
rna_status
# Verify: output shows loaded motif types and counts

# Test 3: Toggle visibility
rna_toggle KTURN off
# Verify: red motifs disappear

rna_toggle KTURN on
# Verify: red motifs reappear

# Test 4: Load different structure
rna_load 2QWY
# Verify: new structure loads with different motif counts

# Test 5: Load from local file
rna_load /path/to/local/file.pdb
# Verify: local file loads correctly
```

### Testing New Motif Types

```python
# After adding new motif:
rna_load 1ABC  # Where 1ABC is in your new JSON

# Check if detected
rna_status
# Should show: MYNEWMOTIF (X instances) ✓ visible

# Test toggle
rna_toggle MYNEWMOTIF off
rna_toggle MYNEWMOTIF on

# Verify color
# Should appear in custom color
```

---

## 🐛 Debugging

### Enable Debug Logging

In `gui.py` initialization:

```python
logger = get_logger()
logger.debug("Debug message")
```

Messages appear in PyMOL console (Windows → Python Console).

### Common Issues & Solutions

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| Motifs don't load | Check JSON format | Validate JSON syntax |
| Wrong colors | Check RGB values | Ensure 0-1 range |
| Selection fails | Check residue format | Verify chain ID exists |
| Object creation fails | Check PyMOL version | Ensure 1.8+ |

---

## 📈 Performance Considerations

- **Parsing:** ~50ms per motif file
- **Selection Creation:** ~10ms per motif type
- **Coloring:** ~5ms per object
- **Toggle:** ~1ms per object

Total for typical structure: <3 seconds

### Optimization Tips

1. **Lazy Loading:** Load motifs only when needed
2. **Caching:** Store parsed motif data
3. **Batch Operations:** Combine PyMOL commands
4. **Index JSON:** Pre-sort PDB IDs in database

---

## 🔄 Plugin Lifecycle

```
1. PyMOL Startup
    ↓
2. Load plugin (__init__.py)
    ↓
3. Call __init_plugin__() (plugin.py)
    ↓
4. Initialize logger (utils/logger.py)
    ↓
5. Initialize GUI (gui.py)
    ↓
6. Register commands (cmd.extend)
    ↓
7. Display welcome message
    ↓
8. Ready for user input
```

---

## 📞 Support & Contribution

For:
- **Bug Reports:** Include error message and PyMOL version
- **Feature Requests:** Describe use case and benefit
- **Contributions:** Follow existing code style and structure

---

## 📝 Code Style Guidelines

- Use **docstrings** for all functions/classes
- Follow **PEP 8** naming conventions
- Include **type hints** where possible
- Use **try-except** for PyMOL operations
- Log **all errors** with logger

---

**Happy developing!** 🚀
