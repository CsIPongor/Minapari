"""Example: Multiple Synchronized Viewers.

Shows how to create multiple viewers that can display
different views of the same or related data.
"""

import sys
import numpy as np
from qtpy.QtWidgets import QMainWindow, QApplication
from qtpy.QtCore import Qt
from minapari.dockable import MinapariDockWidget, setup_shared_context


class MultiViewerWindow(QMainWindow):
    """Window with multiple Minapari viewers."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multiple Viewers")
        self.resize(1600, 900)

        # Create sample data
        self.data = self._create_sample_data()

        # Create viewers for different channels
        self.viewers = []
        colors = ['red', 'green', 'blue']
        titles = ['Red Channel', 'Green Channel', 'Blue Channel']

        for i, (color, title) in enumerate(zip(colors, titles)):
            dock = MinapariDockWidget(self, title=title)
            dock.viewer.add_image(
                self.data[:, :, i],
                name=color,
                colormap=color
            )
            self.viewers.append(dock)

        # Arrange docks
        self.addDockWidget(Qt.LeftDockWidgetArea, self.viewers[0])
        self.addDockWidget(Qt.RightDockWidgetArea, self.viewers[1])
        self.addDockWidget(Qt.RightDockWidgetArea, self.viewers[2])

        # Tab the right viewers together
        self.tabifyDockWidget(self.viewers[1], self.viewers[2])
        self.viewers[1].raise_()  # Show green tab first

        # Create a composite viewer
        self.composite_dock = MinapariDockWidget(self, title="Composite")
        self.composite_dock.viewer.add_image(
            self.data[:, :, 0], name='red', colormap='red', blending='additive'
        )
        self.composite_dock.viewer.add_image(
            self.data[:, :, 1], name='green', colormap='green', blending='additive'
        )
        self.composite_dock.viewer.add_image(
            self.data[:, :, 2], name='blue', colormap='blue', blending='additive'
        )
        self.addDockWidget(Qt.BottomDockWidgetArea, self.composite_dock)

        # Synchronize zoom across viewers
        self._setup_synchronization()

    def _create_sample_data(self):
        """Create synthetic RGB microscopy-like data."""
        y, x = np.ogrid[0:512, 0:512]

        # Red channel: circular structures
        r = np.sqrt((x - 256)**2 + (y - 256)**2)
        red = np.exp(-(r - 100)**2 / 500) + np.exp(-(r - 200)**2 / 500)

        # Green channel: blob pattern
        green = np.zeros((512, 512))
        for _ in range(50):
            cx, cy = np.random.randint(50, 462, 2)
            radius = np.random.randint(10, 30)
            mask = (x - cx)**2 + (y - cy)**2 < radius**2
            green[mask] = np.random.random() * 0.5 + 0.5

        # Blue channel: background gradient
        blue = (x + y) / 1024 * 0.3

        # Stack channels
        data = np.stack([red, green, blue], axis=-1)
        return data.astype(np.float32)

    def _setup_synchronization(self):
        """Synchronize zoom across all viewers."""
        def sync_zoom(event):
            zoom = event.value
            for dock in self.viewers + [self.composite_dock]:
                if dock.viewer.camera.zoom != zoom:
                    dock.viewer.camera.zoom = zoom

        # Connect zoom events
        for dock in self.viewers + [self.composite_dock]:
            dock.viewer.camera.events.zoom.connect(sync_zoom)


def main():
    app = QApplication(sys.argv)
    setup_shared_context()

    window = MultiViewerWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
