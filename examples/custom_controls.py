"""Example: Custom Controls Panel.

Shows how to create a custom control panel alongside the viewer.
"""

import sys
import numpy as np
from qtpy.QtWidgets import (
    QMainWindow, QApplication, QDockWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton,
    QComboBox, QGroupBox, QCheckBox, QSpinBox
)
from qtpy.QtCore import Qt
from minapari.dockable import MinapariDockWidget, setup_shared_context


class ControlPanel(QWidget):
    """Custom control panel for the viewer."""

    def __init__(self, viewer_dock, parent=None):
        super().__init__(parent)
        self.viewer = viewer_dock.viewer
        self.layer = None

        layout = QVBoxLayout(self)

        # Display controls
        display_group = QGroupBox("Display")
        display_layout = QVBoxLayout(display_group)

        # Colormap selector
        cmap_layout = QHBoxLayout()
        cmap_layout.addWidget(QLabel("Colormap:"))
        self.cmap_combo = QComboBox()
        self.cmap_combo.addItems([
            'gray', 'viridis', 'plasma', 'inferno', 'magma',
            'hot', 'cool', 'red', 'green', 'blue'
        ])
        self.cmap_combo.currentTextChanged.connect(self._on_colormap_change)
        cmap_layout.addWidget(self.cmap_combo)
        display_layout.addLayout(cmap_layout)

        # Gamma slider
        gamma_layout = QHBoxLayout()
        gamma_layout.addWidget(QLabel("Gamma:"))
        self.gamma_slider = QSlider(Qt.Horizontal)
        self.gamma_slider.setRange(10, 300)
        self.gamma_slider.setValue(100)
        self.gamma_slider.valueChanged.connect(self._on_gamma_change)
        gamma_layout.addWidget(self.gamma_slider)
        self.gamma_label = QLabel("1.00")
        gamma_layout.addWidget(self.gamma_label)
        display_layout.addLayout(gamma_layout)

        # Opacity slider
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel("Opacity:"))
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self._on_opacity_change)
        opacity_layout.addWidget(self.opacity_slider)
        self.opacity_label = QLabel("100%")
        opacity_layout.addWidget(self.opacity_label)
        display_layout.addLayout(opacity_layout)

        layout.addWidget(display_group)

        # View controls
        view_group = QGroupBox("View")
        view_layout = QVBoxLayout(view_group)

        # 2D/3D toggle
        self.ndisplay_check = QCheckBox("3D View")
        self.ndisplay_check.toggled.connect(self._on_ndisplay_change)
        view_layout.addWidget(self.ndisplay_check)

        # Reset view button
        reset_btn = QPushButton("Reset View")
        reset_btn.clicked.connect(self._reset_view)
        view_layout.addWidget(reset_btn)

        # Zoom controls
        zoom_layout = QHBoxLayout()
        zoom_in_btn = QPushButton("+")
        zoom_in_btn.clicked.connect(lambda: self._zoom(1.2))
        zoom_out_btn = QPushButton("-")
        zoom_out_btn.clicked.connect(lambda: self._zoom(0.8))
        zoom_layout.addWidget(QLabel("Zoom:"))
        zoom_layout.addWidget(zoom_out_btn)
        zoom_layout.addWidget(zoom_in_btn)
        view_layout.addLayout(zoom_layout)

        layout.addWidget(view_group)

        # Layer controls
        layer_group = QGroupBox("Layer")
        layer_layout = QVBoxLayout(layer_group)

        # Visibility toggle
        self.visible_check = QCheckBox("Visible")
        self.visible_check.setChecked(True)
        self.visible_check.toggled.connect(self._on_visibility_change)
        layer_layout.addWidget(self.visible_check)

        # Blending mode
        blend_layout = QHBoxLayout()
        blend_layout.addWidget(QLabel("Blending:"))
        self.blend_combo = QComboBox()
        self.blend_combo.addItems(['translucent', 'additive', 'minimum', 'opaque'])
        self.blend_combo.currentTextChanged.connect(self._on_blending_change)
        blend_layout.addWidget(self.blend_combo)
        layer_layout.addLayout(blend_layout)

        layout.addWidget(layer_group)

        # Data controls
        data_group = QGroupBox("Data")
        data_layout = QVBoxLayout(data_group)

        # Generate new random data
        new_data_btn = QPushButton("New Random Data")
        new_data_btn.clicked.connect(self._generate_new_data)
        data_layout.addWidget(new_data_btn)

        layout.addWidget(data_group)

        layout.addStretch()

        # Connect to layer events
        self.viewer.layers.events.inserted.connect(self._on_layer_added)
        if len(self.viewer.layers) > 0:
            self._set_active_layer(self.viewer.layers[0])

    def _set_active_layer(self, layer):
        """Set the layer controlled by this panel."""
        self.layer = layer
        # Update controls to match layer state
        self.opacity_slider.setValue(int(layer.opacity * 100))
        self.gamma_slider.setValue(int(layer.gamma * 100))
        self.visible_check.setChecked(layer.visible)

    def _on_layer_added(self, event):
        """Handle new layer added."""
        if self.layer is None:
            self._set_active_layer(event.value)

    def _on_colormap_change(self, name):
        if self.layer:
            self.layer.colormap = name

    def _on_gamma_change(self, value):
        gamma = value / 100.0
        self.gamma_label.setText(f"{gamma:.2f}")
        if self.layer:
            self.layer.gamma = gamma

    def _on_opacity_change(self, value):
        self.opacity_label.setText(f"{value}%")
        if self.layer:
            self.layer.opacity = value / 100.0

    def _on_ndisplay_change(self, checked):
        self.viewer.dims.ndisplay = 3 if checked else 2

    def _on_visibility_change(self, checked):
        if self.layer:
            self.layer.visible = checked

    def _on_blending_change(self, mode):
        if self.layer:
            self.layer.blending = mode

    def _reset_view(self):
        self.viewer.reset_view()

    def _zoom(self, factor):
        self.viewer.camera.zoom *= factor

    def _generate_new_data(self):
        if self.layer:
            shape = self.layer.data.shape
            self.layer.data = np.random.random(shape).astype(np.float32)


class CustomControlsWindow(QMainWindow):
    """Main window with viewer and custom controls."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Controls Example")
        self.resize(1200, 800)

        # Create viewer dock
        self.viewer_dock = MinapariDockWidget(self, title="Viewer")
        self.addDockWidget(Qt.LeftDockWidgetArea, self.viewer_dock)

        # Add sample data
        data = np.random.random((64, 256, 256)).astype(np.float32)
        self.viewer_dock.viewer.add_image(data, name='volume', colormap='viridis')

        # Create controls dock
        self.controls_dock = QDockWidget("Controls", self)
        self.controls = ControlPanel(self.viewer_dock)
        self.controls_dock.setWidget(self.controls)
        self.addDockWidget(Qt.RightDockWidgetArea, self.controls_dock)


def main():
    app = QApplication(sys.argv)
    setup_shared_context()

    window = CustomControlsWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
