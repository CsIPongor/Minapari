import typing
from weakref import WeakSet

import numpy as np

from minapari.components.viewer_model import ViewerModel
from minapari.utils.events.event_utils import disconnect_events

if typing.TYPE_CHECKING:
    from minapari._qt.qt_main_window import Window


class Viewer(ViewerModel):
    """Minapari ndarray viewer.

    Parameters
    ----------
    title : string, optional
        The title of the viewer window. By default 'minapari'.
    ndisplay : {2, 3}, optional
        Number of displayed dimensions. By default 2.
    order : tuple of int, optional
        Order in which dimensions are displayed.
    axis_labels : list of str, optional
        Dimension names.
    show : bool, optional
        Whether to show the viewer after instantiation. By default True.
    """

    _window: 'Window' = None  # type: ignore
    _instances: typing.ClassVar[WeakSet['Viewer']] = WeakSet()

    def __init__(
        self,
        *,
        title='minapari',
        ndisplay=2,
        order=(),
        axis_labels=(),
        show=True,
        **kwargs,
    ) -> None:
        super().__init__(
            title=title,
            ndisplay=ndisplay,
            order=order,
            axis_labels=axis_labels,
            **kwargs,
        )
        from minapari.window import Window

        self._window = Window(self, show=show)
        self._instances.add(self)

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    @property
    def window(self) -> 'Window':
        return self._window

    def screenshot(
        self,
        path: str | None = None,
        *,
        size: tuple[str, str] | None = None,
        scale: float | None = None,
        canvas_only: bool = True,
        flash: bool = False,
    ):
        """Take currently displayed screen and convert to an image array.

        Parameters
        ----------
        path : str, optional
            Filename for saving screenshot image.
        size : tuple of two ints, optional
            Size (resolution height x width) of the screenshot.
        scale : float, optional
            Scale factor used to increase resolution of canvas.
        canvas_only : bool
            If True, screenshot shows only the image display canvas.
        flash : bool
            Flag to indicate whether flash animation should be shown.

        Returns
        -------
        image : array
            Numpy array of type ubyte and shape (h, w, 4).
        """
        return self.window.screenshot(
            path=path,
            size=size,
            scale=scale,
            flash=flash,
            canvas_only=canvas_only,
        )

    def show(self, *, block=False):
        """Resize, show, and raise the viewer window."""
        self.window.show(block=block)

    def close(self):
        """Close the viewer window."""
        self._layer_slicer.shutdown()
        disconnect_events(self.dims.events, self)
        self.layers.clear()
        self.window.close()
        self._instances.discard(self)

    @classmethod
    def close_all(cls) -> int:
        """Close all existing viewer instances."""
        viewers = list(cls._instances)
        ret = len(viewers)
        for viewer in viewers:
            viewer.close()
        return ret


def current_viewer() -> Viewer | None:
    """Return the currently active minapari viewer."""
    try:
        from minapari._qt.qt_main_window import _QtMainWindow
    except ImportError:
        return None
    else:
        return _QtMainWindow.current_viewer()
