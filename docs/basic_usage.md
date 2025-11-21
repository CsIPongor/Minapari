# Basic Usage Guide

This guide covers the essential features of Minapari for image visualization.

## Creating a Viewer

### Basic Viewer

```python
from minapari import Viewer

# Default viewer
viewer = Viewer()

# With custom title
viewer = Viewer(title='My Viewer')

# Start in 3D mode
viewer = Viewer(ndisplay=3)

# Don't show immediately (for embedding)
viewer = Viewer(show=False)
```

### Viewer Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | str | 'minapari' | Window title |
| `ndisplay` | int | 2 | Display dimensions (2 or 3) |
| `order` | tuple | () | Dimension display order |
| `axis_labels` | list | () | Labels for each axis |
| `show` | bool | True | Show viewer on creation |

## Adding Images

### Simple Image

```python
import numpy as np
from minapari import Viewer

viewer = Viewer()

# Add 2D image
data_2d = np.random.random((512, 512))
layer = viewer.add_image(data_2d, name='2D Image')

# Add 3D volume
data_3d = np.random.random((64, 128, 128))
layer = viewer.add_image(data_3d, name='3D Volume')
```

### Image Parameters

```python
viewer.add_image(
    data,
    name='my_image',           # Layer name
    colormap='viridis',        # Colormap name
    contrast_limits=(0, 1),    # Min/max display range
    gamma=1.0,                 # Gamma correction
    opacity=1.0,               # Layer opacity (0-1)
    blending='translucent',    # Blending mode
    visible=True,              # Layer visibility
    scale=(1, 1),              # Pixel size per dimension
    translate=(0, 0),          # Offset per dimension
    rendering='mip',           # 3D rendering mode
    iso_threshold=0.5,         # Isosurface threshold
    rgb=False,                 # Treat as RGB
    channel_axis=None,         # Axis for channels
)
```

### Colormaps

Available colormaps:

```python
# Perceptually uniform
'viridis', 'plasma', 'inferno', 'magma', 'cividis'

# Sequential
'gray', 'gray_r', 'hot', 'cool', 'bone'

# Diverging
'coolwarm', 'RdBu', 'seismic'

# Single color (for multi-channel)
'red', 'green', 'blue', 'cyan', 'magenta', 'yellow'

# Example
viewer.add_image(data, colormap='plasma')
```

### Blending Modes

```python
# Translucent (default) - standard alpha blending
viewer.add_image(data, blending='translucent')

# Additive - add pixel values (good for multi-channel)
viewer.add_image(data, blending='additive')

# Minimum - show minimum value
viewer.add_image(data, blending='minimum')

# Opaque - no transparency
viewer.add_image(data, blending='opaque')
```

### 3D Rendering Modes

```python
# Maximum Intensity Projection (default)
viewer.add_image(volume, rendering='mip')

# Minimum Intensity Projection
viewer.add_image(volume, rendering='minip')

# Translucent
viewer.add_image(volume, rendering='translucent')

# Isosurface
viewer.add_image(volume, rendering='iso', iso_threshold=0.5)

# Attenuated MIP
viewer.add_image(volume, rendering='attenuated_mip')
```

## Multi-Channel Images

### RGB Images

```python
# Shape: (Y, X, 3) or (Y, X, 4) for RGBA
rgb_image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
viewer.add_image(rgb_image, rgb=True)
```

### Separate Channels

```python
# Shape: (C, Y, X) where C is number of channels
multichannel = np.random.random((4, 256, 256))

viewer.add_image(
    multichannel,
    channel_axis=0,
    name=['DAPI', 'GFP', 'RFP', 'Brightfield'],
    colormap=['blue', 'green', 'red', 'gray'],
    blending='additive',
)
```

### Time Series

```python
# Shape: (T, Y, X)
timeseries = np.random.random((100, 256, 256))
viewer.add_image(timeseries, name='time_series')

# Use dimension slider to navigate time
```

### 4D Data (Time + Z)

```python
# Shape: (T, Z, Y, X)
data_4d = np.random.random((50, 32, 256, 256))
viewer.add_image(data_4d, name='4D_data')

# Two sliders appear: one for T, one for Z
```

## Working with Layers

### Accessing Layers

```python
# By index
layer = viewer.layers[0]

# By name
layer = viewer.layers['my_image']

# Active layer
layer = viewer.layers.selection.active

# Iterate all layers
for layer in viewer.layers:
    print(layer.name)
```

### Modifying Layers

```python
layer = viewer.layers['my_image']

# Change properties
layer.colormap = 'plasma'
layer.opacity = 0.5
layer.contrast_limits = (0.2, 0.8)
layer.visible = False

# Update data
layer.data = new_data

# Rename
layer.name = 'renamed_image'
```

### Layer Operations

```python
# Remove layer
viewer.layers.remove('my_image')

# Remove all layers
viewer.layers.clear()

# Move layer order
viewer.layers.move(0, 2)  # Move layer 0 to position 2

# Select layers
viewer.layers.selection.add(layer)
viewer.layers.selection.active = layer
```

## Camera Control

### Programmatic Camera Control

```python
# Zoom
viewer.camera.zoom = 2.0  # 2x zoom

# Center on point
viewer.camera.center = (256, 256)  # Center on (y, x)

# Reset view to fit all data
viewer.reset_view()

# 3D camera angles (in 3D mode)
viewer.camera.angles = (0, 0, 90)  # (roll, pitch, yaw)
```

### Switching 2D/3D

```python
# Switch to 3D
viewer.dims.ndisplay = 3

# Switch to 2D
viewer.dims.ndisplay = 2
```

## Dimension Slicing

```python
# Get current slice position
current_point = viewer.dims.point

# Set slice position
viewer.dims.point = (10, 0, 0)  # Set first dimension to slice 10

# Set displayed dimensions
viewer.dims.displayed = (1, 2)  # Display Y and X (for 3D data)
```

## Screenshots

```python
# Take screenshot
screenshot = viewer.screenshot()

# Save to file
viewer.screenshot(path='screenshot.png')

# With specific size
viewer.screenshot(path='hires.png', scale=2.0)
```

## Event Loop

### Blocking Mode

```python
# Show and block until window is closed
viewer.show(block=True)
```

### Non-Blocking Mode

```python
from minapari import Viewer
from qtpy.QtWidgets import QApplication

app = QApplication([])
viewer = Viewer()
viewer.add_image(data)
viewer.show()  # Non-blocking
app.exec_()  # Start event loop
```

### Update Data Live

```python
import time
from qtpy.QtWidgets import QApplication
from qtpy.QtCore import QTimer

app = QApplication([])
viewer = Viewer()
layer = viewer.add_image(np.random.random((256, 256)))

def update():
    layer.data = np.random.random((256, 256))

# Update every 100ms
timer = QTimer()
timer.timeout.connect(update)
timer.start(100)

viewer.show()
app.exec_()
```

## Complete Example

```python
import numpy as np
from minapari import Viewer

# Create viewer
viewer = Viewer(title='Complete Example')

# Add background image
background = np.random.random((512, 512)) * 0.3
viewer.add_image(background, name='background', colormap='gray')

# Add overlay with different colormap
overlay = np.zeros((512, 512))
overlay[200:300, 200:300] = 1.0
viewer.add_image(
    overlay,
    name='overlay',
    colormap='red',
    blending='additive',
    opacity=0.7,
)

# Adjust view
viewer.camera.zoom = 1.5
viewer.camera.center = (256, 256)

# Show viewer
viewer.show(block=True)
```
