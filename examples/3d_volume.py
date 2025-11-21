"""Example: 3D Volume Visualization.

Demonstrates various 3D rendering modes and controls.
"""

import numpy as np
from minapari import Viewer


def create_synthetic_volume():
    """Create a synthetic 3D volume with interesting features."""
    # Create coordinate grids
    z, y, x = np.ogrid[-50:50:100j, -50:50:100j, -50:50:100j]

    # Sphere
    sphere = (x**2 + y**2 + z**2) < 30**2

    # Add some internal structure
    internal = np.sin(x/5) * np.sin(y/5) * np.sin(z/5)

    # Combine
    volume = sphere.astype(float) * (0.5 + 0.5 * internal)

    return volume.astype(np.float32)


def main():
    viewer = Viewer(title='3D Volume Example', ndisplay=3)

    # Create volume data
    volume = create_synthetic_volume()

    # Add with MIP rendering (default)
    layer = viewer.add_image(
        volume,
        name='volume',
        colormap='plasma',
        rendering='mip',
        opacity=1.0,
    )

    print("3D Volume Viewer")
    print("================")
    print("Rendering modes:")
    print("  - 'mip': Maximum Intensity Projection (default)")
    print("  - 'minip': Minimum Intensity Projection")
    print("  - 'translucent': Translucent volume")
    print("  - 'iso': Isosurface rendering")
    print("  - 'attenuated_mip': Attenuated MIP")
    print()
    print("Try changing rendering mode:")
    print("  layer.rendering = 'iso'")
    print("  layer.iso_threshold = 0.5")
    print()
    print("Mouse controls:")
    print("  - Right-click + drag: Rotate")
    print("  - Scroll: Zoom")
    print("  - Click + drag: Pan")

    viewer.show(block=True)


def rendering_comparison():
    """Show same volume with different rendering modes."""
    from qtpy.QtWidgets import QApplication

    app = QApplication([])

    volume = create_synthetic_volume()

    # Create multiple viewers to compare
    viewers = []
    modes = ['mip', 'minip', 'translucent', 'iso']

    for i, mode in enumerate(modes):
        v = Viewer(title=f'{mode.upper()} Rendering', ndisplay=3, show=False)
        kwargs = {'rendering': mode, 'colormap': 'viridis'}
        if mode == 'iso':
            kwargs['iso_threshold'] = 0.5
        v.add_image(volume, name='volume', **kwargs)
        v.show()
        viewers.append(v)

    app.exec_()


if __name__ == '__main__':
    main()
