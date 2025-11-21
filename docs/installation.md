# Installation

## Requirements

- Python 3.10 or higher
- One of: PyQt5, PyQt6, PySide2, or PySide6

## Install from Source

```bash
# Clone the repository
git clone https://github.com/your-org/minapari.git
cd minapari

# Install with your preferred Qt backend
pip install -e ".[pyqt5]"    # PyQt5
pip install -e ".[pyqt6]"    # PyQt6
pip install -e ".[pyside2]"  # PySide2
pip install -e ".[pyside6]"  # PySide6
```

## Dependencies

### Core Dependencies (always installed)

| Package | Purpose |
|---------|---------|
| numpy | Array operations |
| scipy | Scientific computing |
| vispy | GPU-accelerated rendering |
| qtpy | Qt abstraction layer |
| superqt | Enhanced Qt widgets |
| pydantic | Data validation |
| psygnal | Event system |
| dask | Large array support |

### Optional Dependencies

```bash
# For development/testing
pip install -e ".[testing]"
```

## Verifying Installation

```python
import minapari
print(minapari.__version__)

# Quick test
import numpy as np
from minapari import Viewer

viewer = Viewer(show=False)
viewer.add_image(np.zeros((10, 10)))
print("Installation successful!")
viewer.close()
```

## Troubleshooting

### ImportError: No Qt bindings found

Install a Qt backend:
```bash
pip install PyQt5  # or PyQt6, PySide2, PySide6
```

### OpenGL errors on Linux

Install OpenGL libraries:
```bash
# Ubuntu/Debian
sudo apt-get install libgl1-mesa-glx libegl1-mesa

# Fedora
sudo dnf install mesa-libGL mesa-libEGL
```

### Display issues on headless servers

Use a virtual display:
```bash
# Install xvfb
sudo apt-get install xvfb

# Run with virtual display
xvfb-run python your_script.py
```

Or use the offscreen backend:
```python
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
```
