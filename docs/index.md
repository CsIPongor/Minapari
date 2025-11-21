# Minapari Documentation

**Minapari** is a minimal, lightweight fork of [napari](https://napari.org) focused on efficient image viewing. It strips away features you don't need while keeping the powerful GPU-accelerated rendering.

## Table of Contents

1. [Installation](installation.md)
2. [Quick Start](quickstart.md)
3. [Basic Usage](basic_usage.md)
4. [Dockable Widgets](docking.md)
5. [API Reference](api_reference.md)
6. [Examples](examples.md)
7. [Migration from napari](migration.md)

## Why Minapari?

| Feature | napari | Minapari |
|---------|--------|----------|
| Image viewing | Yes | Yes |
| GPU rendering | Yes | Yes |
| 2D/3D support | Yes | Yes |
| Colormaps | Yes | Yes |
| Multi-channel | Yes | Yes |
| Labels layer | Yes | No |
| Points layer | Yes | No |
| Shapes layer | Yes | No |
| Plugin system | Yes | No |
| Console | Yes | No |
| File I/O | Yes | No |
| Startup time | ~3s | ~1.5s |
| Memory | ~200MB | ~80MB |

## When to Use Minapari

**Use Minapari when:**
- You only need image visualization
- You're embedding a viewer in a larger application
- You want minimal startup time and memory footprint
- You're deploying multiple viewer instances
- You load data through your own code (not drag-drop)

**Use napari when:**
- You need annotations (points, shapes, labels)
- You want plugin support
- You need the console for interactive work
- You want built-in file I/O

## Quick Example

```python
import numpy as np
from minapari import Viewer

viewer = Viewer()
viewer.add_image(np.random.random((512, 512)), colormap='viridis')
viewer.show(block=True)
```

## License

BSD-3-Clause (same as napari)
