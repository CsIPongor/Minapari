# Minapari

Minimal napari - A stripped-down image viewer based on napari.

## What is Minapari?

Minapari is a lightweight fork of [napari](https://napari.org) that keeps only the essential components for image viewing:

- Image layer display (2D/3D)
- Pan/zoom controls
- Colormaps
- Multi-channel support
- Layer blending

## What's Removed

- Plugin system
- Console
- Labels, Points, Shapes, Vectors, Tracks, Surface layers
- File I/O (load data externally with numpy, tifffile, etc.)
- Most menus and dialogs

## Installation

```bash
pip install -e ".[pyqt5]"  # or pyqt6, pyside2, pyside6
```

## Usage

```python
import numpy as np
from minapari import Viewer

# Create viewer
viewer = Viewer()

# Add image data
data = np.random.random((512, 512))
viewer.add_image(data, name='random')

# Show viewer (blocking)
viewer.show(block=True)
```

## Performance

Compared to full napari:
- ~50% faster startup
- ~50% less memory usage
- ~37% smaller codebase

## License

BSD-3-Clause (same as napari)
