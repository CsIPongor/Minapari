# Migration from napari

This guide helps you migrate from napari to Minapari.

## What's Different

### Removed Features

| napari | Minapari | Alternative |
|--------|----------|-------------|
| `viewer.add_labels()` | Not available | Use external labeling tools |
| `viewer.add_points()` | Not available | Use matplotlib overlay |
| `viewer.add_shapes()` | Not available | Use matplotlib overlay |
| `viewer.add_vectors()` | Not available | - |
| `viewer.add_tracks()` | Not available | - |
| `viewer.add_surface()` | Not available | - |
| Plugin system | Not available | Direct Python imports |
| Console | Not available | Use external debugger |
| File I/O | Not available | Use imageio, tifffile, etc. |
| `napari.run()` | Not available | `viewer.show(block=True)` |

### Import Changes

```python
# napari
import napari
viewer = napari.Viewer()
napari.run()

# Minapari
from minapari import Viewer
viewer = Viewer()
viewer.show(block=True)
```

### File Loading

```python
# napari (built-in)
viewer = napari.view_image('image.tif')

# Minapari (external)
import tifffile
data = tifffile.imread('image.tif')

from minapari import Viewer
viewer = Viewer()
viewer.add_image(data)
viewer.show(block=True)
```

## Code Migration Examples

### Basic Viewer

```python
# ---- napari ----
import napari
import numpy as np

viewer = napari.Viewer()
viewer.add_image(np.random.random((512, 512)))
napari.run()

# ---- Minapari ----
from minapari import Viewer
import numpy as np

viewer = Viewer()
viewer.add_image(np.random.random((512, 512)))
viewer.show(block=True)
```

### Multi-channel Image

```python
# ---- napari ----
import napari
import numpy as np

data = np.random.random((3, 256, 256))
viewer = napari.Viewer()
viewer.add_image(data, channel_axis=0, colormap=['red', 'green', 'blue'])
napari.run()

# ---- Minapari ----
from minapari import Viewer
import numpy as np

data = np.random.random((3, 256, 256))
viewer = Viewer()
viewer.add_image(data, channel_axis=0, colormap=['red', 'green', 'blue'])
viewer.show(block=True)
```

### Loading Files

```python
# ---- napari ----
import napari
viewer = napari.view_image('cells.tif')
napari.run()

# ---- Minapari ----
import tifffile  # pip install tifffile
from minapari import Viewer

data = tifffile.imread('cells.tif')
viewer = Viewer()
viewer.add_image(data, name='cells')
viewer.show(block=True)
```

### Non-blocking with Qt

```python
# ---- napari ----
import napari
from qtpy.QtWidgets import QApplication

viewer = napari.Viewer()
# ... do stuff ...
napari.run()

# ---- Minapari ----
from qtpy.QtWidgets import QApplication
from minapari import Viewer

app = QApplication([])
viewer = Viewer()
viewer.show()
# ... do stuff ...
app.exec_()
```

### Embedding in Qt Application

```python
# ---- napari ----
# napari doesn't have built-in docking support
# You'd need to extract the Qt viewer manually

# ---- Minapari ----
from qtpy.QtWidgets import QMainWindow, QApplication
from qtpy.QtCore import Qt
from minapari.dockable import MinapariDockWidget, setup_shared_context

app = QApplication([])
setup_shared_context()

window = QMainWindow()
dock = MinapariDockWidget(window)
window.addDockWidget(Qt.RightDockWidgetArea, dock)

dock.viewer.add_image(data)
window.show()
app.exec_()
```

## Compatibility Notes

### API Compatibility

Most `Viewer` and `Image` layer APIs are identical:

```python
# These work the same in both
viewer.add_image(data, colormap='viridis', opacity=0.5)
viewer.layers['name'].visible = False
viewer.camera.zoom = 2.0
viewer.dims.ndisplay = 3
viewer.reset_view()
viewer.screenshot('output.png')
```

### Event System

Event connections work the same:

```python
# Works in both
viewer.layers.events.inserted.connect(callback)
layer.events.data.connect(callback)
viewer.dims.events.ndisplay.connect(callback)
```

### Settings

Minapari uses a simplified settings system. Some napari settings may not apply.

## Performance Comparison

| Metric | napari | Minapari | Improvement |
|--------|--------|----------|-------------|
| Import time | ~2-3s | ~0.8-1.2s | 60% faster |
| Startup time | ~3-4s | ~1.5-2s | 50% faster |
| Memory usage | ~200MB | ~80-100MB | 50% less |
| Code size | ~165K lines | ~66K lines | 60% smaller |

## When to Stay with napari

Keep using napari if you need:

- Annotation tools (labels, points, shapes)
- Plugin ecosystem
- Interactive console
- Built-in file I/O with format detection
- Multiple layer types beyond images

## Getting Help

If you encounter issues migrating:

1. Check this migration guide
2. Review the [API Reference](api_reference.md)
3. Look at the [Examples](examples.md)
4. Open an issue on GitHub
