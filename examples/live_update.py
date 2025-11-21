"""Example: Live Data Updates.

Shows how to update image data in real-time, simulating
a live camera feed or computation.
"""

import sys
import numpy as np
from qtpy.QtWidgets import (
    QMainWindow, QApplication, QDockWidget, QWidget,
    QVBoxLayout, QPushButton, QLabel, QSlider, QHBoxLayout
)
from qtpy.QtCore import Qt, QTimer
from minapari.dockable import MinapariDockWidget, setup_shared_context


class LiveUpdateWindow(QMainWindow):
    """Window with live-updating viewer."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Update Example")
        self.resize(1000, 700)

        # State
        self.frame = 0
        self.running = False
        self.fps = 30

        # Create viewer
        self.viewer_dock = MinapariDockWidget(self, title="Live Feed")
        self.addDockWidget(Qt.LeftDockWidgetArea, self.viewer_dock)

        # Add initial frame
        self.layer = self.viewer_dock.viewer.add_image(
            self._generate_frame(),
            name='live',
            colormap='plasma'
        )

        # Create controls
        self._setup_controls()

        # Timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)

    def _setup_controls(self):
        """Create control panel."""
        controls_dock = QDockWidget("Controls", self)
        controls = QWidget()
        layout = QVBoxLayout(controls)

        # Start/Stop button
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self._toggle_running)
        layout.addWidget(self.start_btn)

        # Single step button
        step_btn = QPushButton("Single Step")
        step_btn.clicked.connect(self._single_step)
        layout.addWidget(step_btn)

        # FPS slider
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("FPS:"))
        self.fps_slider = QSlider(Qt.Horizontal)
        self.fps_slider.setRange(1, 60)
        self.fps_slider.setValue(30)
        self.fps_slider.valueChanged.connect(self._on_fps_change)
        fps_layout.addWidget(self.fps_slider)
        self.fps_label = QLabel("30")
        fps_layout.addWidget(self.fps_label)
        layout.addLayout(fps_layout)

        # Frame counter
        self.frame_label = QLabel("Frame: 0")
        layout.addWidget(self.frame_label)

        # Pattern selector
        layout.addWidget(QLabel("Pattern:"))
        pattern_btns = QHBoxLayout()
        for pattern in ['wave', 'noise', 'spiral']:
            btn = QPushButton(pattern.title())
            btn.clicked.connect(lambda checked, p=pattern: self._set_pattern(p))
            pattern_btns.addWidget(btn)
        layout.addLayout(pattern_btns)

        layout.addStretch()
        controls_dock.setWidget(controls)
        self.addDockWidget(Qt.RightDockWidgetArea, controls_dock)

        # Current pattern
        self.pattern = 'wave'

    def _generate_frame(self):
        """Generate a frame based on current pattern."""
        size = 256
        x = np.linspace(-np.pi, np.pi, size)
        y = np.linspace(-np.pi, np.pi, size)
        X, Y = np.meshgrid(x, y)

        t = self.frame * 0.1

        if self.pattern == 'wave':
            data = np.sin(X + t) * np.cos(Y + t * 0.7)
        elif self.pattern == 'noise':
            base = np.random.random((size, size)) * 0.3
            wave = np.sin(X * 2 + t) * np.cos(Y * 2 + t)
            data = base + wave * 0.7
        elif self.pattern == 'spiral':
            R = np.sqrt(X**2 + Y**2)
            theta = np.arctan2(Y, X)
            data = np.sin(R * 3 - t * 2 + theta * 2)
        else:
            data = np.random.random((size, size))

        return data.astype(np.float32)

    def _update_frame(self):
        """Update the displayed frame."""
        self.frame += 1
        self.layer.data = self._generate_frame()
        self.frame_label.setText(f"Frame: {self.frame}")

    def _toggle_running(self):
        """Start or stop the live feed."""
        self.running = not self.running
        if self.running:
            self.start_btn.setText("Stop")
            interval = int(1000 / self.fps)
            self.timer.start(interval)
        else:
            self.start_btn.setText("Start")
            self.timer.stop()

    def _single_step(self):
        """Advance by a single frame."""
        self._update_frame()

    def _on_fps_change(self, value):
        """Handle FPS slider change."""
        self.fps = value
        self.fps_label.setText(str(value))
        if self.running:
            self.timer.setInterval(int(1000 / self.fps))

    def _set_pattern(self, pattern):
        """Set the pattern type."""
        self.pattern = pattern


class SimulatedMicroscope(QMainWindow):
    """Simulated microscope with multiple channels updating live."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulated Microscope")
        self.resize(1200, 800)

        self.frame = 0

        # Create viewer
        self.viewer_dock = MinapariDockWidget(self, title="Microscope")
        self.addDockWidget(Qt.TopDockWidgetArea, self.viewer_dock)

        # Add channels
        shape = (256, 256)
        self.layers = []
        colors = ['blue', 'green', 'red']
        names = ['DAPI', 'GFP', 'RFP']

        for color, name in zip(colors, names):
            layer = self.viewer_dock.viewer.add_image(
                np.zeros(shape, dtype=np.float32),
                name=name,
                colormap=color,
                blending='additive'
            )
            self.layers.append(layer)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._update)
        self.timer.start(100)  # 10 FPS

    def _update(self):
        """Update all channels."""
        self.frame += 1
        t = self.frame * 0.05
        size = 256
        x = np.linspace(-3, 3, size)
        y = np.linspace(-3, 3, size)
        X, Y = np.meshgrid(x, y)

        # DAPI: nuclei (slow moving spots)
        dapi = np.zeros((size, size))
        for i in range(5):
            cx = np.sin(t * 0.1 + i) * 2
            cy = np.cos(t * 0.1 + i * 1.5) * 2
            dapi += np.exp(-((X - cx)**2 + (Y - cy)**2) / 0.3)
        self.layers[0].data = dapi.astype(np.float32)

        # GFP: cytoplasm (diffuse, changing)
        gfp = np.sin(X + t) * np.cos(Y + t * 0.7) * 0.3 + 0.5
        gfp = np.clip(gfp, 0, 1)
        self.layers[1].data = gfp.astype(np.float32)

        # RFP: puncta (moving dots)
        rfp = np.zeros((size, size))
        np.random.seed(int(t * 10) % 1000)
        for _ in range(20):
            cx = np.random.uniform(-2.5, 2.5)
            cy = np.random.uniform(-2.5, 2.5)
            rfp += np.exp(-((X - cx)**2 + (Y - cy)**2) / 0.05) * np.random.uniform(0.5, 1)
        self.layers[2].data = rfp.astype(np.float32)


def main():
    app = QApplication(sys.argv)
    setup_shared_context()

    # Choose which demo to run
    window = LiveUpdateWindow()
    # window = SimulatedMicroscope()

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
