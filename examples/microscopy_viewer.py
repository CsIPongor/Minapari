"""Example: Complete Microscopy Viewer Application.

A full-featured microscopy image viewer demonstrating many Minapari features.
"""

import sys
import numpy as np
from qtpy.QtWidgets import (
    QMainWindow, QApplication, QDockWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QSlider, QComboBox, QGroupBox, QFileDialog,
    QStatusBar, QToolBar, QAction, QSpinBox, QDoubleSpinBox
)
from qtpy.QtCore import Qt
from qtpy.QtGui import QIcon
from minapari.dockable import MinapariDockWidget, setup_shared_context


class MicroscopyViewer(QMainWindow):
    """A complete microscopy image viewer application."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Microscopy Viewer")
        self.resize(1400, 900)

        # Setup UI components
        self._setup_toolbar()
        self._setup_viewer()
        self._setup_channel_panel()
        self._setup_display_panel()
        self._setup_statusbar()

        # Load demo data
        self._load_demo_data()

    def _setup_toolbar(self):
        """Create main toolbar."""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Open action
        open_action = QAction("Open", self)
        open_action.triggered.connect(self._open_file)
        toolbar.addAction(open_action)

        toolbar.addSeparator()

        # View actions
        reset_action = QAction("Reset View", self)
        reset_action.triggered.connect(self._reset_view)
        toolbar.addAction(reset_action)

        self.toggle_3d_action = QAction("3D", self)
        self.toggle_3d_action.setCheckable(True)
        self.toggle_3d_action.toggled.connect(self._toggle_3d)
        toolbar.addAction(self.toggle_3d_action)

        toolbar.addSeparator()

        # Screenshot action
        screenshot_action = QAction("Screenshot", self)
        screenshot_action.triggered.connect(self._take_screenshot)
        toolbar.addAction(screenshot_action)

    def _setup_viewer(self):
        """Setup the main viewer."""
        self.viewer_dock = MinapariDockWidget(self, title="Viewer")
        self.addDockWidget(Qt.TopDockWidgetArea, self.viewer_dock)

        # Make it take most of the space
        self.viewer_dock.setMinimumWidth(600)
        self.viewer_dock.setMinimumHeight(400)

    def _setup_channel_panel(self):
        """Setup channel controls panel."""
        dock = QDockWidget("Channels", self)
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.channel_widgets = []

        # Will be populated when data is loaded
        self.channel_container = QVBoxLayout()
        layout.addLayout(self.channel_container)

        # All channels button
        btn_layout = QHBoxLayout()
        show_all_btn = QPushButton("Show All")
        show_all_btn.clicked.connect(self._show_all_channels)
        btn_layout.addWidget(show_all_btn)

        hide_all_btn = QPushButton("Hide All")
        hide_all_btn.clicked.connect(self._hide_all_channels)
        btn_layout.addWidget(hide_all_btn)

        layout.addLayout(btn_layout)
        layout.addStretch()

        dock.setWidget(widget)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.channels_dock = dock

    def _setup_display_panel(self):
        """Setup display settings panel."""
        dock = QDockWidget("Display", self)
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Contrast group
        contrast_group = QGroupBox("Contrast")
        contrast_layout = QVBoxLayout(contrast_group)

        # Auto contrast button
        auto_btn = QPushButton("Auto Contrast")
        auto_btn.clicked.connect(self._auto_contrast)
        contrast_layout.addWidget(auto_btn)

        # Min contrast
        min_layout = QHBoxLayout()
        min_layout.addWidget(QLabel("Min:"))
        self.min_spin = QDoubleSpinBox()
        self.min_spin.setRange(0, 1)
        self.min_spin.setSingleStep(0.01)
        self.min_spin.setValue(0)
        self.min_spin.valueChanged.connect(self._on_contrast_change)
        min_layout.addWidget(self.min_spin)
        contrast_layout.addLayout(min_layout)

        # Max contrast
        max_layout = QHBoxLayout()
        max_layout.addWidget(QLabel("Max:"))
        self.max_spin = QDoubleSpinBox()
        self.max_spin.setRange(0, 1)
        self.max_spin.setSingleStep(0.01)
        self.max_spin.setValue(1)
        self.max_spin.valueChanged.connect(self._on_contrast_change)
        max_layout.addWidget(self.max_spin)
        contrast_layout.addLayout(max_layout)

        layout.addWidget(contrast_group)

        # Rendering group (for 3D)
        render_group = QGroupBox("3D Rendering")
        render_layout = QVBoxLayout(render_group)

        render_layout.addWidget(QLabel("Mode:"))
        self.render_combo = QComboBox()
        self.render_combo.addItems(['mip', 'minip', 'translucent', 'iso', 'attenuated_mip'])
        self.render_combo.currentTextChanged.connect(self._on_render_change)
        render_layout.addWidget(self.render_combo)

        layout.addWidget(render_group)

        layout.addStretch()
        dock.setWidget(widget)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.display_dock = dock

        # Tab the panels
        self.tabifyDockWidget(self.channels_dock, dock)
        self.channels_dock.raise_()

    def _setup_statusbar(self):
        """Setup status bar."""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.coord_label = QLabel("Position: --")
        self.statusbar.addWidget(self.coord_label)

        self.value_label = QLabel("Value: --")
        self.statusbar.addWidget(self.value_label)

        self.zoom_label = QLabel("Zoom: 1.0x")
        self.statusbar.addPermanentWidget(self.zoom_label)

        # Connect to cursor events
        self.viewer_dock.viewer.cursor.events.position.connect(self._update_position)
        self.viewer_dock.viewer.camera.events.zoom.connect(self._update_zoom)

    def _load_demo_data(self):
        """Load demonstration data."""
        # Create synthetic multi-channel microscopy data
        size = 256
        z_size = 32

        # Create coordinate grids
        z, y, x = np.ogrid[0:z_size, 0:size, 0:size]
        z = z / z_size * 2 * np.pi
        y = y / size * 4 * np.pi - 2 * np.pi
        x = x / size * 4 * np.pi - 2 * np.pi

        # Channel 1: DAPI (nuclei) - blue
        nuclei = np.zeros((z_size, size, size))
        for i in range(10):
            cx = np.random.randint(50, size-50)
            cy = np.random.randint(50, size-50)
            cz = np.random.randint(5, z_size-5)
            radius = np.random.randint(15, 30)
            dist = ((x * size / (4*np.pi) - cx)**2 +
                    (y * size / (4*np.pi) - cy)**2 +
                    (z * z_size / (2*np.pi) - cz)**2 * 4)
            nuclei += np.exp(-dist / (radius**2))
        nuclei = np.clip(nuclei, 0, 1)

        # Channel 2: GFP (membrane) - green
        membrane = np.sin(x * 2) * np.cos(y * 2) * np.cos(z * 2) * 0.5 + 0.5

        # Channel 3: RFP (puncta) - red
        puncta = np.zeros((z_size, size, size))
        for _ in range(100):
            px = np.random.randint(0, size)
            py = np.random.randint(0, size)
            pz = np.random.randint(0, z_size)
            puncta[max(0, pz-1):pz+2, max(0, py-2):py+3, max(0, px-2):px+3] = np.random.random()

        # Add channels to viewer
        channels = [
            (nuclei, 'DAPI', 'blue'),
            (membrane, 'GFP', 'green'),
            (puncta, 'RFP', 'red'),
        ]

        viewer = self.viewer_dock.viewer

        for data, name, color in channels:
            viewer.add_image(
                data.astype(np.float32),
                name=name,
                colormap=color,
                blending='additive'
            )

        # Create channel control widgets
        self._create_channel_controls()

        self.statusbar.showMessage("Demo data loaded", 3000)

    def _create_channel_controls(self):
        """Create controls for each channel."""
        # Clear existing
        for w in self.channel_widgets:
            w.deleteLater()
        self.channel_widgets.clear()

        viewer = self.viewer_dock.viewer

        for layer in viewer.layers:
            group = QGroupBox(layer.name)
            layout = QVBoxLayout(group)

            # Visibility checkbox
            visible_cb = QPushButton("Visible")
            visible_cb.setCheckable(True)
            visible_cb.setChecked(layer.visible)
            visible_cb.toggled.connect(lambda checked, l=layer: setattr(l, 'visible', checked))
            layout.addWidget(visible_cb)

            # Opacity slider
            opacity_layout = QHBoxLayout()
            opacity_layout.addWidget(QLabel("Opacity:"))
            opacity_slider = QSlider(Qt.Horizontal)
            opacity_slider.setRange(0, 100)
            opacity_slider.setValue(int(layer.opacity * 100))
            opacity_slider.valueChanged.connect(
                lambda v, l=layer: setattr(l, 'opacity', v / 100)
            )
            opacity_layout.addWidget(opacity_slider)
            layout.addLayout(opacity_layout)

            # Colormap selector
            cmap_layout = QHBoxLayout()
            cmap_layout.addWidget(QLabel("Color:"))
            cmap_combo = QComboBox()
            cmap_combo.addItems(['gray', 'red', 'green', 'blue', 'cyan', 'magenta', 'yellow'])
            cmap_combo.setCurrentText(layer.colormap.name)
            cmap_combo.currentTextChanged.connect(
                lambda c, l=layer: setattr(l, 'colormap', c)
            )
            cmap_layout.addWidget(cmap_combo)
            layout.addLayout(cmap_layout)

            self.channel_container.addWidget(group)
            self.channel_widgets.append(group)

    def _open_file(self):
        """Open file dialog (placeholder)."""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "",
            "Image Files (*.tif *.tiff *.png *.jpg);;All Files (*)"
        )
        if filename:
            self.statusbar.showMessage(f"Would load: {filename}", 3000)
            # In real app: data = tifffile.imread(filename)
            # viewer.add_image(data)

    def _reset_view(self):
        """Reset the viewer."""
        self.viewer_dock.viewer.reset_view()

    def _toggle_3d(self, checked):
        """Toggle 2D/3D view."""
        self.viewer_dock.viewer.dims.ndisplay = 3 if checked else 2

    def _take_screenshot(self):
        """Take a screenshot."""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Screenshot", "screenshot.png",
            "PNG Files (*.png);;All Files (*)"
        )
        if filename:
            self.viewer_dock.viewer.screenshot(filename)
            self.statusbar.showMessage(f"Screenshot saved to {filename}", 3000)

    def _show_all_channels(self):
        """Show all channels."""
        for layer in self.viewer_dock.viewer.layers:
            layer.visible = True

    def _hide_all_channels(self):
        """Hide all channels."""
        for layer in self.viewer_dock.viewer.layers:
            layer.visible = False

    def _auto_contrast(self):
        """Auto-adjust contrast for active layer."""
        layer = self.viewer_dock.viewer.layers.selection.active
        if layer:
            data = np.asarray(layer.data)
            layer.contrast_limits = (np.percentile(data, 1), np.percentile(data, 99))

    def _on_contrast_change(self):
        """Handle contrast slider change."""
        layer = self.viewer_dock.viewer.layers.selection.active
        if layer:
            layer.contrast_limits = (self.min_spin.value(), self.max_spin.value())

    def _on_render_change(self, mode):
        """Handle rendering mode change."""
        for layer in self.viewer_dock.viewer.layers:
            layer.rendering = mode

    def _update_position(self, event):
        """Update position display."""
        pos = event.value
        if pos:
            pos_str = ", ".join(f"{p:.1f}" for p in pos)
            self.coord_label.setText(f"Position: ({pos_str})")

    def _update_zoom(self, event):
        """Update zoom display."""
        self.zoom_label.setText(f"Zoom: {event.value:.2f}x")


def main():
    app = QApplication(sys.argv)
    setup_shared_context()

    window = MicroscopyViewer()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
