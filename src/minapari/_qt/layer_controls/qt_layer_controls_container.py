from qtpy.QtWidgets import QFrame, QStackedWidget

from minapari._qt.layer_controls.qt_image_controls import QtImageControls
from minapari.layers import Image
from minapari.utils.translations import trans

layer_to_controls = {
    Image: QtImageControls,
}


def create_qt_layer_controls(layer):
    """
    Create a qt controls widget for a layer based on its layer type.

    Parameters
    ----------
    layer : minapari.layers.Layer
        Layer that needs its controls widget created.

    Returns
    -------
    controls : QtLayerControls
        Qt controls widget
    """
    candidates = []
    for layer_type in layer_to_controls:
        if isinstance(layer, layer_type):
            candidates.append(layer_type)

    if not candidates:
        raise TypeError(
            trans._(
                'Could not find QtControls for layer of type {type_}',
                deferred=True,
                type_=type(layer),
            )
        )

    layer_cls = layer.__class__
    candidates.sort(key=lambda layer_type: layer_cls.mro().index(layer_type))
    controls = layer_to_controls[candidates[0]]
    return controls(layer)


class QtLayerControlsContainer(QStackedWidget):
    """Container widget for QtLayerControl widgets."""

    def __init__(self, viewer) -> None:
        super().__init__()
        self.setProperty('emphasized', True)
        self.viewer = viewer

        self.setMouseTracking(True)
        self.empty_widget = QFrame()
        self.empty_widget.setObjectName('empty_controls_widget')
        self.widgets = {}
        self.addWidget(self.empty_widget)
        self.setCurrentWidget(self.empty_widget)

        self.viewer.layers.events.inserted.connect(self._add)
        self.viewer.layers.events.removed.connect(self._remove)
        viewer.layers.selection.events.active.connect(self._display)
        viewer.dims.events.ndisplay.connect(self._on_ndisplay_changed)

    def _on_ndisplay_changed(self, event):
        for widget in self.widgets.values():
            if widget is not self.empty_widget:
                widget.ndisplay = event.value

    def _display(self, event):
        layer = event.value
        if layer is None:
            self.setCurrentWidget(self.empty_widget)
        else:
            controls = self.widgets[layer]
            self.setCurrentWidget(controls)

    def _add(self, event):
        layer = event.value
        controls = create_qt_layer_controls(layer)
        controls.ndisplay = self.viewer.dims.ndisplay
        self.addWidget(controls)
        self.widgets[layer] = controls

    def _remove(self, event):
        layer = event.value
        controls = self.widgets[layer]
        self.removeWidget(controls)
        controls.hide()
        controls.deleteLater()
        controls = None
        del self.widgets[layer]
