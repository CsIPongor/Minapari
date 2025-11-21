# API Reference

## Core Classes

### `minapari.Viewer`

The main viewer class for displaying images.

```python
class Viewer(ViewerModel):
    """Minapari ndarray viewer."""

    def __init__(
        self,
        *,
        title: str = 'minapari',
        ndisplay: int = 2,
        order: tuple = (),
        axis_labels: list = (),
        show: bool = True,
        **kwargs
    )
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | str | 'minapari' | Window title |
| `ndisplay` | int | 2 | Number of displayed dimensions (2 or 3) |
| `order` | tuple | () | Order of dimensions for display |
| `axis_labels` | list | () | Labels for each axis |
| `show` | bool | True | Whether to show viewer immediately |

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `window` | Window | The Qt window wrapper |
| `layers` | LayerList | List of all layers |
| `dims` | Dims | Dimension state (slicing, display) |
| `camera` | Camera | Camera state (zoom, center, angles) |
| `cursor` | Cursor | Cursor state |
| `theme` | str | Current theme name |

**Methods:**

#### `add_image()`

```python
def add_image(
    self,
    data=None,
    *,
    name: str = None,
    colormap: str = 'gray',
    contrast_limits: tuple = None,
    gamma: float = 1.0,
    opacity: float = 1.0,
    blending: str = 'translucent',
    visible: bool = True,
    scale: tuple = None,
    translate: tuple = None,
    rotate: float = None,
    shear: tuple = None,
    affine = None,
    rendering: str = 'mip',
    iso_threshold: float = 0.5,
    attenuation: float = 0.05,
    rgb: bool = None,
    channel_axis: int = None,
    multiscale: bool = None,
    **kwargs
) -> Image
```

Add an image layer to the viewer.

**Returns:** `Image` layer object

#### `screenshot()`

```python
def screenshot(
    self,
    path: str = None,
    *,
    size: tuple = None,
    scale: float = None,
    canvas_only: bool = True,
    flash: bool = False
) -> np.ndarray
```

Take a screenshot of the viewer.

**Returns:** numpy array of shape (H, W, 4)

#### `show()`

```python
def show(self, *, block: bool = False)
```

Show the viewer window.

#### `close()`

```python
def close(self)
```

Close the viewer and release resources.

#### `reset_view()`

```python
def reset_view(self)
```

Reset camera to fit all layer data.

---

### `minapari.layers.Image`

Image layer for displaying array data.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `data` | array | The image data |
| `name` | str | Layer name |
| `visible` | bool | Layer visibility |
| `opacity` | float | Layer opacity (0-1) |
| `blending` | str | Blending mode |
| `colormap` | Colormap | Current colormap |
| `contrast_limits` | tuple | (min, max) display range |
| `gamma` | float | Gamma correction value |
| `rendering` | str | 3D rendering mode |
| `iso_threshold` | float | Isosurface threshold |
| `interpolation2d` | str | 2D interpolation mode |
| `interpolation3d` | str | 3D interpolation mode |
| `rgb` | bool | Whether data is RGB |
| `multiscale` | bool | Whether data is multiscale |
| `ndim` | int | Number of dimensions |
| `shape` | tuple | Data shape |
| `dtype` | dtype | Data type |
| `scale` | tuple | Scale per dimension |
| `translate` | tuple | Translation per dimension |

**Colormaps:**

```python
# Set by name
layer.colormap = 'viridis'

# Available colormaps
from minapari.utils.colormaps import AVAILABLE_COLORMAPS
print(list(AVAILABLE_COLORMAPS.keys()))
```

**Blending modes:**

- `'translucent'` - Standard alpha blending
- `'additive'` - Add pixel values
- `'minimum'` - Show minimum value
- `'opaque'` - No transparency

**Rendering modes (3D):**

- `'mip'` - Maximum intensity projection
- `'minip'` - Minimum intensity projection
- `'translucent'` - Translucent volume
- `'iso'` - Isosurface
- `'attenuated_mip'` - Attenuated MIP

---

### `minapari.components.LayerList`

Container for managing layers.

**Methods:**

```python
# Add layer
layers.append(layer)

# Remove by name or object
layers.remove('layer_name')
layers.remove(layer)

# Clear all
layers.clear()

# Get by index or name
layer = layers[0]
layer = layers['name']

# Move layer
layers.move(from_index, to_index)

# Check containment
'name' in layers  # True/False
```

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `selection` | Selection | Selected layers |

---

### `minapari.components.Dims`

Dimension state management.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `ndim` | int | Total number of dimensions |
| `ndisplay` | int | Number of displayed dimensions |
| `displayed` | tuple | Indices of displayed dimensions |
| `point` | tuple | Current slice position |
| `range` | list | Range for each dimension |
| `order` | tuple | Dimension order |
| `axis_labels` | list | Labels for each axis |

**Example:**

```python
# Switch to 3D display
viewer.dims.ndisplay = 3

# Set slice position
viewer.dims.point = (10, 0, 0)  # Slice first dim at 10

# Get displayed dimensions
print(viewer.dims.displayed)  # e.g., (1, 2)
```

---

### `minapari.components.Camera`

Camera state for viewing.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `center` | tuple | Camera center point |
| `zoom` | float | Zoom level |
| `angles` | tuple | Camera angles (3D): (roll, pitch, yaw) |
| `mouse_pan` | bool | Enable mouse panning |
| `mouse_zoom` | bool | Enable mouse zooming |

**Example:**

```python
# Set zoom
viewer.camera.zoom = 2.0

# Center on point
viewer.camera.center = (256, 256)

# 3D rotation
viewer.camera.angles = (0, 45, 30)
```

---

## Docking Module

### `minapari.dockable`

Utilities for embedding Minapari in Qt applications.

#### `setup_shared_context()`

```python
def setup_shared_context() -> GLContext
```

Setup shared OpenGL context for all viewers. Call once at application startup.

**Returns:** The shared OpenGL context

#### `get_shared_context()`

```python
def get_shared_context() -> GLContext
```

Get the shared context, creating it if necessary.

#### `MinapariDockWidget`

```python
class MinapariDockWidget(QDockWidget):
    def __init__(
        self,
        parent: QWidget = None,
        title: str = "Minapari",
        auto_setup_context: bool = True
    )
```

A QDockWidget containing a Minapari viewer.

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `viewer` | Viewer | The embedded Minapari viewer |

**Methods:**

```python
# Convenience method
dock.add_image(data, **kwargs)
```

#### `MinapariWidget`

```python
class MinapariWidget(QWidget):
    def __init__(
        self,
        parent: QWidget = None,
        auto_setup_context: bool = True
    )
```

A simple QWidget containing a Minapari viewer.

---

## Canvas Classes

### `minapari._vispy.canvas.VispyCanvas`

Low-level canvas class (usually not used directly).

**Class Methods:**

```python
@classmethod
def set_shared_context(cls, context)
```

Set a shared OpenGL context for all canvas instances.

**Constructor Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `viewer` | ViewerModel | The viewer model |
| `key_map_handler` | KeymapHandler | Keyboard handler |
| `shared` | Canvas/GLContext | Shared context |

---

## Type Aliases

```python
from minapari.types import (
    ArrayLike,      # np.ndarray, dask.array, zarr.Array
    ImageData,      # NewType for image data
    LayerData,      # Tuple of (data,) or (data, meta) or (data, meta, type)
    PathLike,       # str or Path
)
```

---

## Events

Layers and components emit events when properties change:

```python
# Connect to layer events
layer.events.data.connect(callback)
layer.events.visible.connect(callback)
layer.events.colormap.connect(callback)

# Connect to viewer events
viewer.layers.events.inserted.connect(on_layer_added)
viewer.layers.events.removed.connect(on_layer_removed)
viewer.dims.events.ndisplay.connect(on_ndisplay_change)
viewer.camera.events.zoom.connect(on_zoom_change)

# Callback signature
def callback(event):
    print(f"New value: {event.value}")
```
