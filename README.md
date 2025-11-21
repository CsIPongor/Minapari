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

### Standalone Viewer

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

### Dockable Widget (Embedded in Qt Application)

```python
from qtpy.QtWidgets import QMainWindow, QApplication
from qtpy.QtCore import Qt
from minapari.dockable import MinapariDockWidget, setup_shared_context
import numpy as np

app = QApplication([])

# IMPORTANT: Setup shared OpenGL context BEFORE creating viewers
# This prevents context loss when undocking
setup_shared_context()

# Create main window
main_window = QMainWindow()
main_window.setWindowTitle("My Application")
main_window.resize(1200, 800)

# Create dockable minapari viewer
dock = MinapariDockWidget(main_window, title="Image Viewer")
main_window.addDockWidget(Qt.RightDockWidgetArea, dock)

# Add images
dock.viewer.add_image(np.random.random((512, 512)), name='random')

main_window.show()
app.exec_()
```

The `setup_shared_context()` call creates a shared OpenGL context that survives
dock widget undocking/redocking without losing the rendering context.

## Performance

Compared to full napari:
- ~50% faster startup
- ~50% less memory usage
- ~37% smaller codebase

## License

BSD-3-Clause (same as napari)
