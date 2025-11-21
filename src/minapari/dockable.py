"""Helper classes for embedding Minapari as a dockable widget.

This module provides utilities to create Minapari viewers that can be
safely docked/undocked in a Qt application without losing the OpenGL context.

Example
-------
```python
from qtpy.QtWidgets import QMainWindow, QApplication
from minapari.dockable import MinapariDockWidget, setup_shared_context

app = QApplication([])

# Setup shared context BEFORE creating any viewers
setup_shared_context()

# Create main window with dockable minapari
main_window = QMainWindow()
dock = MinapariDockWidget(main_window)
main_window.addDockWidget(Qt.RightDockWidgetArea, dock)

# Add images
dock.viewer.add_image(my_data)

main_window.show()
app.exec_()
```
"""

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDockWidget, QWidget, QVBoxLayout


_context_canvas = None


def setup_shared_context():
    """Setup a shared OpenGL context for all Minapari viewers.

    Call this ONCE at application startup, BEFORE creating any viewers.
    This ensures all canvases share the same OpenGL context, preventing
    context loss when dock widgets are undocked.

    Returns
    -------
    context : vispy.gloo.GLContext
        The shared context that will be used by all viewers.
    """
    global _context_canvas

    from vispy import app
    from minapari._vispy.canvas import VispyCanvas

    # Create a hidden canvas that holds the shared context
    # This canvas lives for the lifetime of the application
    _context_canvas = app.Canvas(show=False, size=(1, 1))

    # Set this as the shared context for all VispyCanvas instances
    VispyCanvas.set_shared_context(_context_canvas.context)

    return _context_canvas.context


def get_shared_context():
    """Get the shared OpenGL context, creating it if necessary."""
    global _context_canvas
    if _context_canvas is None:
        return setup_shared_context()
    return _context_canvas.context


class MinapariDockWidget(QDockWidget):
    """A QDockWidget containing a Minapari viewer.

    This widget handles OpenGL context sharing automatically, so the viewer
    survives docking/undocking without losing the OpenGL context.

    Parameters
    ----------
    parent : QWidget, optional
        Parent widget.
    title : str, optional
        Title of the dock widget. Default is "Minapari".
    auto_setup_context : bool, optional
        If True (default), automatically setup shared context if not done.

    Attributes
    ----------
    viewer : minapari.Viewer
        The Minapari viewer instance.

    Example
    -------
    ```python
    dock = MinapariDockWidget(main_window)
    main_window.addDockWidget(Qt.RightDockWidgetArea, dock)
    dock.viewer.add_image(np.random.random((512, 512)))
    ```
    """

    def __init__(
        self,
        parent: QWidget = None,
        title: str = "Minapari",
        auto_setup_context: bool = True,
    ):
        super().__init__(title, parent)

        # Ensure shared context exists
        if auto_setup_context:
            get_shared_context()

        # Create viewer without showing it
        from minapari.viewer import Viewer
        self._viewer = Viewer(show=False, title=title)

        # Get the Qt viewer widget and set it as dock content
        qt_viewer = self._viewer.window._qt_viewer
        self.setWidget(qt_viewer)

        # Allow docking in all areas
        self.setAllowedAreas(
            Qt.LeftDockWidgetArea |
            Qt.RightDockWidgetArea |
            Qt.TopDockWidgetArea |
            Qt.BottomDockWidgetArea
        )

    @property
    def viewer(self):
        """The Minapari viewer instance."""
        return self._viewer

    def add_image(self, data, **kwargs):
        """Convenience method to add an image to the viewer."""
        return self._viewer.add_image(data, **kwargs)

    def closeEvent(self, event):
        """Clean up viewer on close."""
        self._viewer.close()
        super().closeEvent(event)


class MinapariWidget(QWidget):
    """A simple QWidget containing a Minapari viewer.

    Use this when you want to embed Minapari in a custom layout
    (not as a dock widget).

    Parameters
    ----------
    parent : QWidget, optional
        Parent widget.
    auto_setup_context : bool, optional
        If True (default), automatically setup shared context if not done.
    """

    def __init__(self, parent: QWidget = None, auto_setup_context: bool = True):
        super().__init__(parent)

        if auto_setup_context:
            get_shared_context()

        from minapari.viewer import Viewer
        self._viewer = Viewer(show=False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._viewer.window._qt_viewer)

    @property
    def viewer(self):
        return self._viewer

    def closeEvent(self, event):
        self._viewer.close()
        super().closeEvent(event)
