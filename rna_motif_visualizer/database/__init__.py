"""
RNA Motif Visualizer - Database Package
Provides scalable database provider abstraction for multiple motif databases.

This package implements a plugin architecture for motif databases:
- BaseProvider: Abstract base class for all database providers
- DatabaseRegistry: Central registry for managing database providers
- Format converters for different data formats

Supported databases:
- RNA 3D Motif Atlas (JSON format)
- Rfam Motif Database (Stockholm format)
- Future: Custom databases, API-based sources

Author: Structural Biology Lab
Version: 2.0.0
"""

from .base_provider import (
    BaseProvider,
    MotifInstance,
    MotifType,
    ResidueSpec,
    DatabaseInfo,
)
from .registry import DatabaseRegistry, get_registry, initialize_registry
from .atlas_provider import RNA3DAtlasProvider
from .rfam_provider import RfamProvider

__all__ = [
    # Base classes
    'BaseProvider',
    'MotifInstance',
    'MotifType',
    'ResidueSpec',
    'DatabaseInfo',
    # Registry
    'DatabaseRegistry',
    'get_registry',
    'initialize_registry',
    # Providers
    'RNA3DAtlasProvider',
    'RfamProvider',
]
