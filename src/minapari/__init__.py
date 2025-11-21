"""Minapari - Minimal napari for image viewing."""

import os

try:
    from minapari._version import version as __version__
except ImportError:
    __version__ = '0.1.0'

# Allows us to use pydata/sparse arrays as layer data
os.environ.setdefault('SPARSE_AUTO_DENSIFY', '1')

del os

# Direct imports for common usage
from minapari.viewer import Viewer
from minapari.layers import Image, Layer

__all__ = [
    '__version__',
    'Viewer',
    'Image',
    'Layer',
]
