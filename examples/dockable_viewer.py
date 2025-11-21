"""Example: Dockable Viewer in Qt Application.

Shows how to embed Minapari as a dock widget that can be
freely docked, undocked, and rearranged.
"""

import sys
import numpy as np
from qtpy.QtWidgets import (
    QMainWindow, QApplication, QTextEdit, QMenuBar, QMenu, QAction
)
from qtpy.QtCore import Qt
from minapari.dockable import MinapariDockWidget, setup_shared_context


class MainWindow(QMainWindow):
    """Main application window with dockable Minapari viewer."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application with Dockable Minapari")
        self.resize(1400, 900)

        # Setup menus
        self._setup_menus()

        # Central widget (your main application content)
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(
            "This is the main application area.\n\n"
            "The Minapari viewer is in a dock widget on the right.\n\n"
            "Try:\n"
            "- Undocking the viewer (drag the title bar)\n"
            "- Docking it to different edges\n"
            "- Closing and reopening it via View menu\n"
        )
        self.setCentralWidget(self.text_edit)

        # Create Minapari dock widget
        self.viewer_dock = MinapariDockWidget(self, title="Image Viewer")
        self.addDockWidget(Qt.RightDockWidgetArea, self.viewer_dock)

        # Add sample data
        self._add_sample_data()

    def _setup_menus(self):
        """Setup application menus."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        new_image_action = QAction("New Random Image", self)
        new_image_action.triggered.connect(self._add_random_image)
        file_menu.addAction(new_image_action)

        file_menu.addSeparator()

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # View menu
        view_menu = menubar.addMenu("View")

        self.toggle_viewer_action = QAction("Show Viewer", self)
        self.toggle_viewer_action.setCheckable(True)
        self.toggle_viewer_action.setChecked(True)
        self.toggle_viewer_action.triggered.connect(self._toggle_viewer)
        view_menu.addAction(self.toggle_viewer_action)

        reset_view_action = QAction("Reset Viewer", self)
        reset_view_action.triggered.connect(self._reset_viewer)
        view_menu.addAction(reset_view_action)

    def _add_sample_data(self):
        """Add sample images to the viewer."""
        viewer = self.viewer_dock.viewer

        # Add a gradient image
        y, x = np.ogrid[0:256, 0:256]
        gradient = (x + y) / 512
        viewer.add_image(gradient, name='gradient', colormap='viridis')

        # Add a pattern
        pattern = np.sin(x / 10) * np.cos(y / 10)
        viewer.add_image(
            pattern,
            name='pattern',
            colormap='plasma',
            opacity=0.5,
            blending='additive'
        )

    def _add_random_image(self):
        """Add a new random image to the viewer."""
        data = np.random.random((256, 256))
        n = len(self.viewer_dock.viewer.layers)
        self.viewer_dock.viewer.add_image(
            data,
            name=f'random_{n}',
            colormap='gray'
        )

    def _toggle_viewer(self, checked):
        """Toggle viewer visibility."""
        self.viewer_dock.setVisible(checked)

    def _reset_viewer(self):
        """Reset viewer to default state."""
        self.viewer_dock.viewer.reset_view()


def main():
    app = QApplication(sys.argv)

    # CRITICAL: Setup shared context BEFORE creating any viewers
    # This ensures the OpenGL context survives undocking
    setup_shared_context()

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
