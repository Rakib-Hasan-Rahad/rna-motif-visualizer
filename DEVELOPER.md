# Developer Documentation

Comprehensive technical guide for developers who want to understand, extend, or contribute to the RNA Motif Visualizer plugin.

---

## 📚 Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Project Structure](#2-project-structure)
3. [Core Components](#3-core-components)
4. [Multi-Source Provider System](#4-multi-source-provider-system)
5. [Data Flow](#5-data-flow)
6. [API Providers](#6-api-providers)
7. [Caching System](#7-caching-system)
8. [Adding New Features](#8-adding-new-features)
9. [Testing](#9-testing)
10. [Contributing](#10-contributing)

---

## 1. Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PyMOL Application                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────────┐ │
│  │  plugin.py  │───►│   gui.py    │───►│      loader.py          │ │
│  │  (entry)    │    │ (commands)  │    │  (VisualizationManager) │ │
│  └─────────────┘    └─────────────┘    └───────────┬─────────────┘ │
│                                                     │               │
│                                    ┌────────────────┴────────────┐  │
│                                    │     UnifiedMotifLoader      │  │
│                                    └────────────┬────────────────┘  │
│                                                 │                   │
│  ┌──────────────────────────────────────────────┴───────────────┐  │
│  │                     Source Selector                           │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐  │  │
│  │  │  LOCAL  │  │  BGSU   │  │  RFAM   │  │  CACHE MANAGER  │  │  │
│  │  │Provider │  │  API    │  │  API    │  │                 │  │  │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────────┬────────┘  │  │
│  └───────┼────────────┼───────────┼─────────────────┼───────────┘  │
│          │            │           │                 │               │
└──────────┼────────────┼───────────┼─────────────────┼───────────────┘
           │            │           │                 │
           ▼            ▼           ▼                 ▼
    ┌──────────┐  ┌───────────┐ ┌───────────┐  ┌──────────────┐
    │  Local   │  │   BGSU    │ │   Rfam    │  │    Cache     │
    │ Database │  │    API    │ │    API    │  │   Storage    │
    └──────────┘  └───────────┘ └───────────┘  └──────────────┘
```

### Design Philosophy

1. **Provider Pattern** - All data sources implement a common interface
2. **Smart Fallback** - Automatically tries multiple sources when one fails
3. **Aggressive Caching** - API responses cached for 30 days
4. **Contextual Help** - Guide users with suggestions after each command
5. **Clean Separation** - PyMOL interactions isolated from data logic

---

## 2. Project Structure

```
rna-motif-visualizer/
├── README.md                    # User documentation
├── TUTORIAL.md                  # Step-by-step tutorial
├── DEVELOPER.md                 # This file
├── LICENSE                      # MIT License
├── test_atlas_validation.py     # Testing script
├── images/                      # Documentation images
│   ├── 1.png, 2.png, 3.png
│   └── README.md
│
└── rna_motif_visualizer/        # Main plugin package
    │
    ├── __init__.py              # Package marker
    ├── plugin.py                # PyMOL entry point
    ├── gui.py                   # Command registration
    ├── loader.py                # Core visualization logic
    ├── colors.py                # Color definitions
    │
    ├── atlas_loader.py          # Legacy (compatibility)
    ├── pdb_motif_mapper.py      # Legacy (compatibility)
    │
    ├── database/                # Data provider layer
    │   ├── __init__.py          # Package exports
    │   ├── base_provider.py     # Abstract base classes
    │   ├── registry.py          # Provider registry
    │   ├── atlas_provider.py    # Local Atlas provider
    │   ├── rfam_provider.py     # Local Rfam provider
    │   ├── bgsu_api_provider.py # BGSU API provider
    │   ├── rfam_api_provider.py # Rfam API provider
    │   ├── cache_manager.py     # Response caching
    │   ├── config.py            # Configuration
    │   ├── source_selector.py   # Source orchestration
    │   └── converters.py        # Format converters
    │
    ├── motif_database/          # Bundled data files
    │   ├── hl_4.5.json          # Hairpin loops
    │   ├── il_4.5.json          # Internal loops
    │   ├── j3_4.5.json - j7_4.5.json
    │   └── motif_registry.json
    │
    └── utils/                   # Utility modules
        ├── __init__.py
        ├── logger.py            # PyMOL console logging
        ├── parser.py            # PDB ID parsing
        └── selectors.py         # PyMOL selections
```

---

## 3. Core Components

### 3.1 plugin.py - Entry Point

```python
def __init_plugin__(app=None):
    """PyMOL calls this when loading the plugin."""
    # 1. Initialize logger
    # 2. Initialize database registry
    # 3. Register PyMOL commands
    # 4. Print welcome message
```

### 3.2 gui.py - Command Layer

Registers all PyMOL commands and handles argument parsing:

```python
# Core commands
cmd.extend('rna_load', load_structure_action)
cmd.extend('rna_show', show_motif_action)
cmd.extend('rna_instance', show_instance_action)
cmd.extend('rna_all', show_all_action)
cmd.extend('rna_summary', summary_action)

# Source control
cmd.extend('rna_source', set_source_action)
cmd.extend('rna_source_info', source_info_action)
cmd.extend('rna_refresh', refresh_action)

# Utilities
cmd.extend('rna_switch', switch_db_action)
cmd.extend('rna_toggle', toggle_action)
cmd.extend('rna_status', status_action)
cmd.extend('rna_databases', databases_action)
cmd.extend('rna_bg_color', bg_color_action)
```

### 3.3 loader.py - Visualization Engine

The heart of the plugin. Contains three main classes:

#### VisualizationManager

```python
class VisualizationManager:
    """Orchestrates the entire visualization workflow."""
    
    def load_and_visualize(self, pdb_id: str):
        """Main entry point for loading structures."""
        # 1. Load PDB structure
        # 2. Setup gray RNA cartoon
        # 3. Load motifs from sources
        # 4. Create colored objects
        # 5. Print summary with suggestions
```

#### UnifiedMotifLoader

```python
class UnifiedMotifLoader:
    """Loads motifs from multiple sources."""
    
    def load_motifs(self, pdb_id: str) -> Dict[str, List]:
        """Query active sources for motifs."""
        # Uses source_selector to get motifs
        # Merges results from multiple providers
```

#### StructureLoader

```python
class StructureLoader:
    """Handles PDB structure fetching."""
    
    def load_structure(self, pdb_id: str) -> bool:
        """Download and load PDB from RCSB."""
```

### 3.4 colors.py - Color Definitions

```python
MOTIF_COLORS = {
    'HL': (1.0, 0.4, 0.4),      # Red - Hairpin Loops
    'IL': (1.0, 0.6, 0.2),      # Orange - Internal Loops
    'J3': (1.0, 0.8, 0.2),      # Yellow - 3-way Junctions
    'J4': (0.2, 0.8, 0.2),      # Green - 4-way Junctions
    'J5': (0.2, 0.6, 0.8),      # Cyan - 5-way Junctions
    'J6': (0.4, 0.4, 0.8),      # Purple - 6-way Junctions
    'J7': (0.8, 0.4, 0.8),      # Magenta - 7-way Junctions
    'GNRA': (0.2, 0.6, 0.2),    # Forest Green - GNRA Tetraloops
    'UNCG': (0.3, 0.5, 0.7),    # Slate Blue - UNCG Tetraloops
    'K-turn': (0.1, 0.4, 0.6),  # Marine Blue - Kink-turns
    'T-loop': (0.9, 0.5, 0.6),  # Pink - T-loops
    'C-loop': (0.6, 0.4, 0.2),  # Brown - C-loops
    'U-turn': (0.7, 0.3, 0.5),  # Mauve - U-turns
}
```

---

## 4. Multi-Source Provider System

### 4.1 Source Modes

```python
class SourceMode(Enum):
    AUTO = "auto"       # Smart selection with fallback
    LOCAL = "local"     # Bundled database only
    BGSU = "bgsu"       # BGSU API only
    RFAM = "rfam"       # Rfam API only
    ALL = "all"         # Combine all sources
```

### 4.2 Source Selector (source_selector.py)

```python
class SourceSelector:
    """Orchestrates queries across multiple data sources."""
    
    def __init__(self):
        self.config = Config()
        self.cache_manager = CacheManager()
        self.local_provider = LocalProvider()
        self.bgsu_provider = BGSUAPIProvider()
        self.rfam_provider = RfamAPIProvider()
    
    def get_motifs(self, pdb_id: str) -> Dict[str, List]:
        """Get motifs based on current source mode."""
        mode = self.config.get_source_mode()
        
        if mode == SourceMode.AUTO:
            return self._auto_fetch(pdb_id)
        elif mode == SourceMode.BGSU:
            return self.bgsu_provider.get_motifs(pdb_id)
        elif mode == SourceMode.RFAM:
            return self.rfam_provider.get_motifs(pdb_id)
        elif mode == SourceMode.ALL:
            return self._merge_all_sources(pdb_id)
        else:
            return self.local_provider.get_motifs(pdb_id)
    
    def _auto_fetch(self, pdb_id: str) -> Dict:
        """Try local first, then BGSU, then Rfam."""
        result = self.local_provider.get_motifs(pdb_id)
        if not result:
            result = self.bgsu_provider.get_motifs(pdb_id)
        if not result:
            result = self.rfam_provider.get_motifs(pdb_id)
        return result
```

### 4.3 Base Provider Interface (base_provider.py)

```python
class BaseProvider(ABC):
    """Abstract base class for all data providers."""
    
    @abstractmethod
    def initialize(self) -> bool:
        """Load and index the database."""
        pass
    
    @abstractmethod
    def get_motifs_for_pdb(self, pdb_id: str) -> Dict[str, List]:
        """Return all motifs for a PDB structure."""
        pass
    
    @property
    @abstractmethod
    def info(self) -> DatabaseInfo:
        """Return metadata about this provider."""
        pass

@dataclass
class MotifInstance:
    """Represents one occurrence of a motif."""
    motif_id: str
    chain: str
    residues: List[ResidueSpec]
    sequence: Optional[str] = None

@dataclass
class ResidueSpec:
    """Represents a single nucleotide."""
    chain: str
    position: int
    nucleotide: str
```

---

## 5. Data Flow

### Complete Request Flow

```
1. User types: rna_load 1S72
         │
         ▼
2. gui.py: load_structure_action("1S72")
         │
         ▼
3. loader.py: VisualizationManager.load_and_visualize("1S72")
         │
         ├─► StructureLoader.load_structure("1S72")
         │         │
         │         ▼
         │   RCSB PDB → Download → cmd.load()
         │
         ├─► setup_clean_visualization()
         │         │
         │         ▼
         │   cmd.show("cartoon"), cmd.color("gray")
         │
         └─► UnifiedMotifLoader.load_motifs("1S72")
                   │
                   ▼
4. source_selector.py: SourceSelector.get_motifs("1S72")
         │
         ├─► Check cache_manager
         │         │
         │         ├─ Cache HIT → Return cached data
         │         │
         │         └─ Cache MISS → Continue
         │
         ├─► Query BGSU API (if mode allows)
         │         │
         │         ▼
         │   https://rna.bgsu.edu/rna3dhub/motifs/...
         │
         ├─► Query Rfam API (if mode allows)
         │         │
         │         ▼
         │   https://rfam.org/family/.../pdb_matches
         │
         └─► Store in cache
                   │
                   ▼
5. Return to loader.py with motif data
         │
         ▼
6. For each motif type:
         │
         ├─► selectors.py: create_motif_class_object()
         │         │
         │         ▼
         │   cmd.create("GNRA", selection)
         │   cmd.color([0.2, 0.6, 0.2], "GNRA")
         │   cmd.hide("cartoon", "1S72 and " + selection)
         │
         └─► Continue for HL, IL, J3, etc.
                   │
                   ▼
7. _print_motif_summary_table()
         │
         ▼
8. Console displays summary + contextual suggestions
```

---

## 6. API Providers

### 6.1 BGSU API Provider (bgsu_api_provider.py)

```python
class BGSUAPIProvider:
    """Fetches motifs from BGSU RNA 3D Hub API."""
    
    BASE_URL = "https://rna.bgsu.edu/rna3dhub/motifs"
    
    def get_motifs_for_pdb(self, pdb_id: str) -> Dict[str, List]:
        """Query BGSU API for hairpins, internal loops, junctions."""
        
        # Endpoint: /motifs/release/{version}/nrlist/{pdb_id}
        # Returns: JSON with HL, IL, J3-J7 instances
        
        url = f"{self.BASE_URL}/release/4.5/nrlist/{pdb_id}"
        response = self._fetch_with_ssl_fix(url)
        return self._parse_response(response)
    
    def _fetch_with_ssl_fix(self, url: str) -> dict:
        """Handle SSL certificate issues on macOS."""
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        # ... fetch with context
```

**Motif Types Available**: HL, IL, J3, J4, J5, J6, J7

### 6.2 Rfam API Provider (rfam_api_provider.py)

```python
class RfamAPIProvider:
    """Fetches named motifs from Rfam API."""
    
    BASE_URL = "https://rfam.org"
    
    # Mapping of motif names to Rfam family IDs
    MOTIF_FAMILIES = {
        'GNRA': 'RF00028',
        'UNCG': 'RF00029',
        'K-turn': 'RF00167',
        'T-loop': 'RF00370',
        'C-loop': 'RF00371',
        'U-turn': 'RF01051',
        'sarcin-ricin': 'RF00022',
    }
    
    def get_motifs_for_pdb(self, pdb_id: str) -> Dict[str, List]:
        """Query Rfam API for named motifs."""
        
        results = {}
        for motif_name, rfam_id in self.MOTIF_FAMILIES.items():
            # Endpoint: /family/{rfam_id}/pdb_matches/{pdb_id}
            url = f"{self.BASE_URL}/family/{rfam_id}/pdb_matches/{pdb_id}"
            matches = self._fetch_matches(url)
            if matches:
                results[motif_name] = matches
        
        return results
```

**Motif Types Available**: GNRA, UNCG, K-turn, T-loop, C-loop, U-turn, sarcin-ricin, and more

---

## 7. Caching System

### 7.1 Cache Manager (cache_manager.py)

```python
class CacheManager:
    """Manages persistent caching of API responses."""
    
    CACHE_DIR = "~/.rna_motif_visualizer_cache"
    EXPIRY_DAYS = 30
    
    def __init__(self):
        self.cache_path = Path(self.CACHE_DIR).expanduser()
        self.cache_path.mkdir(exist_ok=True)
    
    def get(self, key: str) -> Optional[dict]:
        """Retrieve cached data if not expired."""
        cache_file = self._get_cache_file(key)
        if cache_file.exists():
            data = json.load(cache_file.open())
            if not self._is_expired(data['timestamp']):
                return data['payload']
        return None
    
    def set(self, key: str, data: dict):
        """Store data in cache with timestamp."""
        cache_file = self._get_cache_file(key)
        payload = {
            'timestamp': time.time(),
            'payload': data
        }
        json.dump(payload, cache_file.open('w'))
    
    def _get_cache_file(self, key: str) -> Path:
        """Generate cache filename from key."""
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_path / f"{hash_key}.json"
    
    def _is_expired(self, timestamp: float) -> bool:
        """Check if cache entry has expired."""
        age_days = (time.time() - timestamp) / 86400
        return age_days > self.EXPIRY_DAYS
    
    def clear(self):
        """Clear all cached data."""
        for f in self.cache_path.glob("*.json"):
            f.unlink()
```

### 7.2 Cache Structure

```
~/.rna_motif_visualizer_cache/
├── a1b2c3d4e5f6...json    # BGSU response for 1S72
├── f6e5d4c3b2a1...json    # Rfam GNRA for 1S72
└── ...
```

Each cache file:
```json
{
  "timestamp": 1704067200.0,
  "payload": {
    "HL": [...],
    "IL": [...]
  }
}
```

---

## 8. Adding New Features

### 8.1 Adding a New API Provider

1. **Create provider file** `database/my_api_provider.py`:

```python
from .base_provider import BaseProvider

class MyAPIProvider(BaseProvider):
    BASE_URL = "https://api.example.com"
    
    def get_motifs_for_pdb(self, pdb_id: str) -> Dict[str, List]:
        # Implementation
        pass
```

2. **Register in source_selector.py**:

```python
from .my_api_provider import MyAPIProvider

class SourceSelector:
    def __init__(self):
        # ...
        self.my_provider = MyAPIProvider()
```

3. **Add source mode** (optional):

```python
class SourceMode(Enum):
    # ...
    MY_SOURCE = "mysource"
```

### 8.2 Adding a New Motif Type

1. **Add color** in `colors.py`:

```python
MOTIF_COLORS = {
    # ...
    'NEW_MOTIF': (0.5, 0.5, 0.8),
}
```

2. **Update API provider** to recognize the new type

3. **Update converters** if needed

### 8.3 Adding a New Command

1. **Add handler** in `loader.py`:

```python
def my_new_feature(self, arg1, arg2):
    """Implement feature logic."""
    # Implementation
    
    # Add contextual suggestions
    print("\n  Next steps:")
    print("    rna_summary                View summary")
```

2. **Register command** in `gui.py`:

```python
def my_feature_action(arg1="", arg2=""):
    """PyMOL command wrapper."""
    manager = get_visualization_manager()
    manager.my_new_feature(arg1, arg2)

cmd.extend('rna_myfeature', my_feature_action)
```

### 8.4 Adding Contextual Help

In any function that outputs to console:

```python
def some_function(self):
    # ... do work ...
    
    # Print contextual suggestions
    print("\n  Next steps:")
    print(f"    rna_show {motif_type:<20} View {motif_type} instances")
    print(f"    rna_summary                View summary table")
```

---

## 9. Testing

### 9.1 Unit Tests

Run validation without PyMOL:

```bash
python3 test_atlas_validation.py
```

This tests:
- JSON parsing for Atlas format
- PDB ID extraction
- Residue specification parsing

### 9.2 API Tests

Test API connectivity:

```python
# In Python interpreter
from rna_motif_visualizer.database.bgsu_api_provider import BGSUAPIProvider
from rna_motif_visualizer.database.rfam_api_provider import RfamAPIProvider

bgsu = BGSUAPIProvider()
print(bgsu.get_motifs_for_pdb('1S72'))

rfam = RfamAPIProvider()
print(rfam.get_motifs_for_pdb('1S72'))
```

### 9.3 Integration Tests

Test in PyMOL:

```python
# Test all source modes
rna_source local
rna_load 1S72
rna_summary

rna_source bgsu
rna_load 1S72
rna_summary

rna_source all
rna_load 1S72
rna_summary
```

### 9.4 Cache Tests

```python
# Test cache functionality
from rna_motif_visualizer.database.cache_manager import CacheManager

cache = CacheManager()
cache.set('test_key', {'data': 'test'})
print(cache.get('test_key'))
cache.clear()
```

---

## 10. Contributing

### 10.1 Development Setup

```bash
git clone https://github.com/Rakib-Hasan-Rahad/rna-motif-visualizer.git
cd rna-motif-visualizer

# Link to PyMOL plugins folder (macOS)
ln -s $(pwd)/rna_motif_visualizer ~/Library/Application\ Support/PyMOL/plugins/

# Or add via Plugin Manager
```

### 10.2 Code Style

- Python 3.6+ compatible
- Type hints encouraged
- Docstrings for public methods
- Contextual help for user-facing functions

### 10.3 Pull Request Checklist

- [ ] Tests pass (`python3 test_atlas_validation.py`)
- [ ] New features have contextual help
- [ ] Colors added for new motif types
- [ ] Documentation updated
- [ ] No breaking changes to existing commands

### 10.4 Issue Reporting

Please include:
- PyMOL version
- Operating system
- Plugin version (`rna_status`)
- Error messages from console
- Steps to reproduce

---

## 📖 Quick Reference

### Key Files to Understand

| File | Purpose |
|------|---------|
| `loader.py` | Core visualization logic |
| `source_selector.py` | Multi-source orchestration |
| `bgsu_api_provider.py` | BGSU API integration |
| `rfam_api_provider.py` | Rfam API integration |
| `cache_manager.py` | Caching layer |

### Important Classes

| Class | Location | Purpose |
|-------|----------|---------|
| `VisualizationManager` | loader.py | Main orchestrator |
| `SourceSelector` | source_selector.py | Source routing |
| `CacheManager` | cache_manager.py | Caching |
| `BGSUAPIProvider` | bgsu_api_provider.py | BGSU API |
| `RfamAPIProvider` | rfam_api_provider.py | Rfam API |

---

<p align="center">
  <b>Happy Developing! 🛠️</b>
</p>
