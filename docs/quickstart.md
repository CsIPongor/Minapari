# Quick Start

Get up and running with Minapari in 5 minutes.

## Your First Viewer

```python
import numpy as np
from minapari import Viewer

# Create a viewer
viewer = Viewer()

# Add a random image
data = np.random.random((256, 256))
viewer.add_image(data, name='my_image')

# Show the viewer (blocks until closed)
viewer.show(block=True)
```

## Loading Real Images

```python
import numpy as np
from PIL import Image  # or use imageio, tifffile, etc.
from minapari import Viewer

# Load image with PIL
img = np.array(Image.open('my_image.png'))

viewer = Viewer()
viewer.add_image(img, name='loaded_image')
viewer.show(block=True)
```

## Multi-Channel Images

```python
import numpy as np
from minapari import Viewer

# Create RGB image
rgb = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

viewer = Viewer()
viewer.add_image(rgb, name='rgb_image', rgb=True)
viewer.show(block=True)
```

## Separate Channels with Different Colormaps

```python
import numpy as np
from minapari import Viewer

# Create multi-channel data (C, Y, X)
channels = np.random.random((3, 256, 256))

viewer = Viewer()
viewer.add_image(
    channels,
    channel_axis=0,  # First axis is channels
    name=['red', 'green', 'blue'],
    colormap=['red', 'green', 'blue'],
    blending='additive',
)
viewer.show(block=True)
```

## 3D Volume

```python
import numpy as np
from minapari import Viewer

# Create 3D volume (Z, Y, X)
volume = np.random.random((64, 128, 128))

viewer = Viewer(ndisplay=3)  # Start in 3D mode
viewer.add_image(volume, name='volume', rendering='mip')
viewer.show(block=True)
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `2` | Switch to 2D view |
| `3` | Switch to 3D view |
| `Home` | Reset view |
| `R` | Reset view |
| `T` | Toggle grid |

## Mouse Controls

| Action | Effect |
|--------|--------|
| Scroll | Zoom in/out |
| Click + Drag | Pan |
| Right-click + Drag | Rotate (3D) |

## Next Steps

- [Basic Usage](basic_usage.md) - More detailed usage guide
- [Docking Guide](docking.md) - Embed in your application
- [API Reference](api_reference.md) - Full API documentation
