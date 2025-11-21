# Dockable Widgets Guide

This guide explains how to embed Minapari viewers in Qt applications as dockable widgets that can be freely docked, undocked, and rearranged.

## The Problem

When a Qt dock widget is undocked (floated), Qt reparents the widget to a new top-level window. This can destroy the OpenGL context, causing the viewer to lose its rendering state.

## The Solution

Minapari provides a **shared OpenGL context** mechanism that survives widget reparenting. All viewers share a single context that lives for the application's lifetime.

## Quick Start

```python
from qtpy.QtWidgets import QMainWindow, QApplication
from qtpy.QtCore import Qt
from minapari.dockable import MinapariDockWidget, setup_shared_context
import numpy as np

app = QApplication([])

# CRITICAL: Setup shared context BEFORE creating any viewers
setup_shared_context()

# Create main window
main_window = QMainWindow()
main_window.resize(1200, 800)

# Create dockable viewer
dock = MinapariDockWidget(main_window, title="Image Viewer")
main_window.addDockWidget(Qt.RightDockWidgetArea, dock)

# Add image data
dock.viewer.add_image(np.random.random((512, 512)))

main_window.show()
app.exec_()
```

## API Reference

### `setup_shared_context()`

Creates a shared OpenGL context for all Minapari viewers.

```python
from minapari.dockable import setup_shared_context

# Call ONCE at application startup, BEFORE creating viewers
context = setup_shared_context()
```

**Important:** Must be called before creating any `Viewer` or `MinapariDockWidget`.

### `MinapariDockWidget`

A `QDockWidget` containing a Minapari viewer.

```python
from minapari.dockable import MinapariDockWidget

dock = MinapariDockWidget(
    parent=main_window,      # Parent widget
    title="Viewer",          # Dock widget title
    auto_setup_context=True  # Auto-setup context if needed
)

# Access the viewer
dock.viewer.add_image(data)

# Convenience method
dock.add_image(data, colormap='viridis')
```

### `MinapariWidget`

A simple `QWidget` containing a Minapari viewer (for custom layouts).

```python
from minapari.dockable import MinapariWidget

widget = MinapariWidget(parent=some_container)
widget.viewer.add_image(data)
```

## Complete Examples

### Single Dockable Viewer

```python
import sys
import numpy as np
from qtpy.QtWidgets import QMainWindow, QApplication, QTextEdit
from qtpy.QtCore import Qt
from minapari.dockable import MinapariDockWidget, setup_shared_context


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application with Minapari")
        self.resize(1400, 900)

        # Central widget (your main content)
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText("Main application content here...")
        self.setCentralWidget(self.text_edit)

        # Create minapari dock
        self.viewer_dock = MinapariDockWidget(self, title="Image Viewer")
        self.addDockWidget(Qt.RightDockWidgetArea, self.viewer_dock)

        # Add sample data
        self.viewer_dock.viewer.add_image(
            np.random.random((256, 256)),
            name='sample',
            colormap='viridis'
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setup_shared_context()  # IMPORTANT: Before creating windows

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
```

### Multiple Dockable Viewers

```python
import sys
import numpy as np
from qtpy.QtWidgets import QMainWindow, QApplication
from qtpy.QtCore import Qt
from minapari.dockable import MinapariDockWidget, setup_shared_context


class MultiViewerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multiple Viewers")
        self.resize(1600, 900)

        # Create multiple viewer docks
        self.viewer1 = MinapariDockWidget(self, title="Channel 1 (Red)")
        self.viewer2 = MinapariDockWidget(self, title="Channel 2 (Green)")
        self.viewer3 = MinapariDockWidget(self, title="Channel 3 (Blue)")

        # Arrange docks
        self.addDockWidget(Qt.LeftDockWidgetArea, self.viewer1)
        self.addDockWidget(Qt.RightDockWidgetArea, self.viewer2)
        self.addDockWidget(Qt.RightDockWidgetArea, self.viewer3)

        # Stack viewer2 and viewer3
        self.tabifyDockWidget(self.viewer2, self.viewer3)

        # Add different data to each
        data = np.random.random((256, 256, 3))
        self.viewer1.viewer.add_image(data[:, :, 0], colormap='red')
        self.viewer2.viewer.add_image(data[:, :, 1], colormap='green')
        self.viewer3.viewer.add_image(data[:, :, 2], colormap='blue')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setup_shared_context()

    window = MultiViewerWindow()
    window.show()

    sys.exit(app.exec_())
```

### Viewer with Controls Panel

```python
import sys
import numpy as np
from qtpy.QtWidgets import (
    QMainWindow, QApplication, QDockWidget, QWidget,
    QVBoxLayout, QSlider, QLabel, QPushButton
)
from qtpy.QtCore import Qt
from minapari.dockable import MinapariDockWidget, setup_shared_context


class ViewerWithControls(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Viewer with Controls")
        self.resize(1200, 800)

        # Minapari viewer as central widget area
        self.viewer_dock = MinapariDockWidget(self, title="Viewer")
        self.addDockWidget(Qt.TopDockWidgetArea, self.viewer_dock)

        # Add sample data
        self.data = np.random.random((100, 256, 256))
        self.layer = self.viewer_dock.viewer.add_image(
            self.data, name='volume', colormap='viridis'
        )

        # Create controls dock
        self.controls_dock = QDockWidget("Controls", self)
        controls_widget = QWidget()
        layout = QVBoxLayout(controls_widget)

        # Colormap selector (simplified)
        layout.addWidget(QLabel("Gamma:"))
        self.gamma_slider = QSlider(Qt.Horizontal)
        self.gamma_slider.setRange(10, 300)  # 0.1 to 3.0
        self.gamma_slider.setValue(100)  # 1.0
        self.gamma_slider.valueChanged.connect(self._on_gamma_change)
        layout.addWidget(self.gamma_slider)

        # Opacity slider
        layout.addWidget(QLabel("Opacity:"))
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self._on_opacity_change)
        layout.addWidget(self.opacity_slider)

        # Reset button
        reset_btn = QPushButton("Reset View")
        reset_btn.clicked.connect(self._reset_view)
        layout.addWidget(reset_btn)

        # Toggle 2D/3D button
        toggle_btn = QPushButton("Toggle 2D/3D")
        toggle_btn.clicked.connect(self._toggle_ndisplay)
        layout.addWidget(toggle_btn)

        layout.addStretch()
        self.controls_dock.setWidget(controls_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.controls_dock)

    def _on_gamma_change(self, value):
        self.layer.gamma = value / 100.0

    def _on_opacity_change(self, value):
        self.layer.opacity = value / 100.0

    def _reset_view(self):
        self.viewer_dock.viewer.reset_view()

    def _toggle_ndisplay(self):
        viewer = self.viewer_dock.viewer
        viewer.dims.ndisplay = 3 if viewer.dims.ndisplay == 2 else 2


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setup_shared_context()

    window = ViewerWithControls()
    window.show()

    sys.exit(app.exec_())
```

### Live Data Updates

```python
import sys
import numpy as np
from qtpy.QtWidgets import QMainWindow, QApplication
from qtpy.QtCore import Qt, QTimer
from minapari.dockable import MinapariDockWidget, setup_shared_context


class LiveUpdateWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Updates")
        self.resize(800, 600)

        self.viewer_dock = MinapariDockWidget(self, title="Live Data")
        self.addDockWidget(Qt.TopDockWidgetArea, self.viewer_dock)

        # Initial data
        self.frame = 0
        self.layer = self.viewer_dock.viewer.add_image(
            self._generate_frame(),
            name='live',
            colormap='plasma'
        )

        # Timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)
        self.timer.start(50)  # 20 FPS

    def _generate_frame(self):
        """Generate a moving pattern."""
        x = np.linspace(-3, 3, 256)
        y = np.linspace(-3, 3, 256)
        X, Y = np.meshgrid(x, y)
        phase = self.frame * 0.1
        return np.sin(X + phase) * np.cos(Y + phase)

    def _update_frame(self):
        self.frame += 1
        self.layer.data = self._generate_frame()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setup_shared_context()

    window = LiveUpdateWindow()
    window.show()

    sys.exit(app.exec_())
```

## Manual Context Setup

If you need more control, you can setup the shared context manually:

```python
from vispy import app
from minapari._vispy.canvas import VispyCanvas

# Create your own context holder
context_canvas = app.Canvas(show=False, size=(1, 1))

# Register it with VispyCanvas
VispyCanvas.set_shared_context(context_canvas.context)

# Now create viewers normally
from minapari import Viewer
viewer = Viewer()
```

## Troubleshooting

### OpenGL context lost on undock

**Cause:** `setup_shared_context()` was not called before creating viewers.

**Solution:** Call `setup_shared_context()` immediately after creating `QApplication`, before any viewer creation.

### Multiple applications / processes

Each process needs its own shared context. The context cannot be shared across processes.

### Context errors on application exit

Make sure to close all viewers before the application exits:

```python
def cleanup():
    for dock in [self.viewer1, self.viewer2]:
        dock.viewer.close()

app.aboutToQuit.connect(cleanup)
```

### Performance with many viewers

Each viewer shares the context but has its own scene graph. For best performance:
- Limit the number of simultaneous viewers
- Use lower resolution data when possible
- Disable viewers that are not visible

## Best Practices

1. **Always call `setup_shared_context()` first** - Before creating any viewer
2. **One shared context per application** - Don't create multiple
3. **Close viewers on exit** - Prevent resource leaks
4. **Use `show=False`** - When creating embedded viewers
5. **Parent widgets properly** - Helps Qt manage the widget lifecycle
