# Developer Documentation

This document explains the architecture of the RNA Motif Visualizer plugin. It is meant for developers who want to understand how the code works, add new features, or integrate new database formats.

---

## Project Structure

```
rna-motif-visualizer/
├── README.md                 # User documentation
├── DEVELOPER.md              # This file
├── LICENSE                   # MIT license
├── test_atlas_validation.py  # Testing script
├── images/                   # Screenshots for documentation
│   ├── 1.png
│   ├── 2.png
│   └── 3.png
└── rna_motif_visualizer/     # Main plugin package
    ├── __init__.py           # Package marker (imports plugin entry point)
    ├── plugin.py             # PyMOL plugin entry point
    ├── gui.py                # Command registration and user interface
    ├── loader.py             # Structure loading and visualization logic
    ├── colors.py             # Color definitions for motif types
    ├── atlas_loader.py       # Legacy Atlas loader (kept for compatibility)
    ├── pdb_motif_mapper.py   # Legacy mapper (kept for compatibility)
    ├── utils/                # Utility modules
    │   ├── __init__.py
    │   ├── logger.py         # Logging to PyMOL console
    │   ├── parser.py         # PDB ID extraction and selection strings
    │   └── selectors.py      # PyMOL selection and object creation
    ├── database/             # Database abstraction layer
    │   ├── __init__.py       # Package exports
    │   ├── base_provider.py  # Abstract base classes and data structures
    │   ├── registry.py       # Central registry for managing providers
    │   ├── atlas_provider.py # RNA 3D Atlas implementation
    │   ├── rfam_provider.py  # Rfam database implementation
    │   └── converters.py     # Format converters (JSON, Stockholm)
    └── motif_database/       # Bundled motif data
        ├── RNA 3D motif atlas/
        │   ├── hl_4.5.json
        │   ├── il_4.5.json
        │   └── j*.json
        └── Rfam motif database/
            ├── GNRA/
            │   └── SEED
            ├── T-loop/
            │   └── SEED
            └── .../
```

---

## How the Plugin Works

### Initialization Flow

When PyMOL loads the plugin, it calls `__init_plugin__()` in `plugin.py`. Here is what happens:

1. **Logger Setup** - `initialize_logger()` creates a logger that prints to the PyMOL console with timestamps and color-coded messages.

2. **Database Registry** - `initialize_registry()` scans the `motif_database` folder and registers all available database providers:
   - Looks for `RNA 3D motif atlas/` and creates an `RNA3DAtlasProvider`
   - Looks for `Rfam motif database/` and creates an `RfamProvider`
   - Each provider is initialized and indexed

3. **Command Registration** - `initialize_gui()` registers all the PyMOL commands (`rna_load`, `rna_toggle`, etc.)

4. **Welcome Message** - Prints available databases and usage instructions

### Loading a Structure

When the user runs `rna_load 1S72`, the following happens:

1. **gui.py** - `load_structure_action()` receives the command
2. **loader.py** - `VisualizationManager.load_and_visualize()` orchestrates the process:
   - Calls `StructureLoader.load_structure()` to fetch/load the PDB
   - Calls `setup_clean_visualization()` to set up gray RNA cartoon
   - Calls `UnifiedMotifLoader.load_motifs()` to get motif data
3. **database/registry.py** - Gets the active provider
4. **database/*_provider.py** - Queries the provider for motifs in that PDB
5. **loader.py** - For each motif type:
   - Hides those residues on the main structure
   - Creates a separate PyMOL object with colored cartoon
6. **Console Output** - Prints the motif summary table

### Data Flow Diagram

```
User Command
    │
    ▼
gui.py (command parsing)
    │
    ▼
loader.py (VisualizationManager)
    │
    ├──► StructureLoader (fetch PDB from RCSB)
    │
    └──► UnifiedMotifLoader
            │
            ▼
        database/registry.py (get active provider)
            │
            ▼
        database/*_provider.py (query motifs)
            │
            ▼
        utils/selectors.py (create PyMOL objects)
            │
            ▼
        PyMOL display
```

---

## Core Components

### Base Provider (database/base_provider.py)

This module defines the data structures and abstract interface that all database providers must implement.

**Key Classes:**

- `ResidueSpec` - Represents a single nucleotide position (chain, residue number, nucleotide type)
- `MotifInstance` - One occurrence of a motif in a PDB structure
- `MotifType` - A family/class of motifs with multiple instances
- `BaseProvider` - Abstract base class that providers must inherit

**Important Methods in BaseProvider:**

```python
def initialize(self) -> bool:
    """Load and index the database. Called once at startup."""

def get_motifs_for_pdb(self, pdb_id: str) -> Dict[str, List[MotifInstance]]:
    """Return all motifs found in a specific PDB structure."""

def get_available_pdb_ids(self) -> List[str]:
    """List all PDB IDs in the database."""

def get_available_motif_types(self) -> List[str]:
    """List all motif types (HL, IL, GNRA, etc.)."""
```

### Registry (database/registry.py)

The registry manages multiple database providers and handles switching between them.

```python
registry = get_registry()
registry.register_provider(my_provider, 'my_db')
registry.set_active_provider('my_db')
motifs = registry.get_active_provider().get_motifs_for_pdb('1S72')
```

### Converters (database/converters.py)

Converters transform raw file data into the standard `MotifType` and `MotifInstance` objects.

- `AtlasJSONConverter` - Parses RNA 3D Atlas JSON format
- `StockholmConverter` - Parses Rfam SEED files (Stockholm format)

To add a new format, create a new converter class that inherits from `BaseConverter`.

---

## Example Walkthrough: RNA 3D Atlas

Here is how the Atlas provider processes data from beginning to end.

### Database Structure

```
RNA 3D motif atlas/
├── hl_4.5.json     # Hairpin loops
├── il_4.5.json     # Internal loops
├── j3_4.5.json     # 3-way junctions
└── ...
```

Each JSON file contains an array of motif entries:

```json
[
  {
    "motif_id": "HL_00001.1",
    "alignment": {
      "HL_1S72_001": {
        "1": "1S72|1|0|G|100",
        "2": "1S72|1|0|A|101"
      }
    }
  }
]
```

### Loading Process

1. **RNA3DAtlasProvider.__init__()** - Stores the database path

2. **RNA3DAtlasProvider.initialize()** - Called by registry:
   - Scans directory for JSON files matching `*_*.json`
   - For each file, calls `_load_motif_file()`
   - Uses `AtlasJSONConverter` to parse JSON into `MotifType` objects
   - Builds a PDB index mapping PDB IDs to motif instances

3. **RNA3DAtlasProvider.get_motifs_for_pdb('1S72')** - When queried:
   - Looks up '1S72' in the PDB index
   - Returns all motif instances grouped by type

4. **UnifiedMotifLoader._load_motif_type()** - Creates visualization:
   - Converts `MotifInstance` to legacy format `{chain, residues, motif_id}`
   - Calls `MotifSelector.create_motif_class_object()` to create PyMOL object
   - Hides those residues on main structure
   - Colors the object

---

## Example Walkthrough: Rfam Database

### Database Structure

```
Rfam motif database/
├── GNRA/
│   ├── SEED        # Stockholm format alignment
│   ├── CM          # Covariance model (optional)
│   └── SEED.png    # Structure diagram (optional)
├── T-loop/
│   └── SEED
└── ...
```

The SEED file format:

```
# STOCKHOLM 1.0

#=GF ID   GNRA
#=GF DE   GNRA tetraloop

3OWI_A/41-61    CGGGAAGAACCC
#=GR 3OWI_A/41-61 SS  (((...)))

1S72_0/500-510  GGGAGAACCC
//
```

### Loading Process

1. **RfamProvider.__init__()** - Stores the database path

2. **RfamProvider.initialize()** - Called by registry:
   - Scans for subdirectories containing SEED files
   - For each subdirectory, calls `_load_motif_directory()`
   - Uses `StockholmConverter` to parse SEED into `MotifType` objects
   - Builds PDB index

3. **StockholmConverter._parse_sequence_id()** - Parses entries like `1S72_0/500-510`:
   - Extracts PDB ID: `1S72`
   - Extracts chain: `0`
   - Extracts range: `500-510`
   - Creates `ResidueSpec` objects for each position

4. **get_motifs_for_pdb()** and visualization work the same as Atlas

---

## Adding a New Database Format

To add support for a new motif database format:

### Step 1 - Create a Converter

Add a new class in `database/converters.py`:

```python
class MyFormatConverter(BaseConverter):
    def convert_file(self, file_path: Path) -> List[MotifType]:
        # Read and parse your file format
        # Return list of MotifType objects
        pass
    
    def convert_data(self, data: Any, source_info: Dict) -> List[MotifType]:
        # Convert raw data to MotifType objects
        pass
```

### Step 2 - Create a Provider

Create a new file `database/my_provider.py`:

```python
from .base_provider import BaseProvider, DatabaseInfo, DatabaseSourceType

class MyDatabaseProvider(BaseProvider):
    def __init__(self, database_path: str):
        super().__init__(database_path)
        self._converter = MyFormatConverter()
    
    @property
    def info(self) -> DatabaseInfo:
        return DatabaseInfo(
            id='my_db',
            name='My Database',
            description='My custom motif database',
            version='1.0.0',
            source_type=DatabaseSourceType.LOCAL_DIRECTORY,
            motif_types=list(self._motif_types.keys()),
            pdb_count=len(self._pdb_index)
        )
    
    def initialize(self) -> bool:
        # Scan directory, load files, build index
        # Return True if successful
        pass
```

### Step 3 - Register the Provider

Update `database/registry.py` in `initialize_registry()`:

```python
from .my_provider import MyDatabaseProvider

# In initialize_registry():
my_path = db_path / 'My Database'
if my_path.exists():
    my_provider = MyDatabaseProvider(str(my_path))
    registry.register_provider(my_provider, 'my_db')
```

### Step 4 - Add Colors

Update `colors.py` with colors for your motif types:

```python
MOTIF_COLORS = {
    # ...
    'MY_MOTIF_TYPE': (0.5, 0.8, 0.3),
}
```

---

## Key Design Decisions

### Why Separate Providers?

Different databases use different file formats and data models. The provider abstraction allows each database to be loaded and queried in its native format while presenting a unified interface to the rest of the plugin.

### Why Hide Residues on Main Structure?

PyMOL has z-fighting issues when multiple objects occupy the same 3D coordinates. By hiding the motif residues on the main structure and showing them only on the motif objects, we get clean solid colors without visual artifacts.

### Why Use cmd.create() Instead of Selections?

PyMOL selections create visual markers (pink squares) and do not behave like objects. Using `cmd.create()` makes proper objects that appear in the right panel and can be independently shown/hidden.

---

## Testing

Run the validation script to test Atlas parsing without PyMOL:

```bash
python3 test_atlas_validation.py
```

This tests that the Atlas JSON files can be loaded and parsed correctly.

---

## Future Plans

- Add more database formats (API-based sources, custom annotation files)
- Users can drop their own database folders and have them auto-discovered
- Web-based motif lookup for structures not in local databases
- Integration with structure prediction tools
- GUI dialog for motif selection and filtering

---

## Questions?

If you have questions about the codebase or want to contribute, open an issue on the repository.
