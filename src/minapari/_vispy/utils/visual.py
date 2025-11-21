from __future__ import annotations

from typing import Any

import numpy as np
from vispy.scene.widgets.viewbox import ViewBox

from minapari._vispy.layers.base import VispyBaseLayer
from minapari._vispy.layers.image import VispyImageLayer
from minapari._vispy.overlays.axes import VispyAxesOverlay
from minapari._vispy.overlays.base import VispyBaseOverlay
from minapari._vispy.overlays.bounding_box import VispyBoundingBoxOverlay
from minapari._vispy.overlays.brush_circle import VispyBrushCircleOverlay
from minapari._vispy.overlays.colorbar import VispyColorBarOverlay
from minapari._vispy.overlays.interaction_box import (
    VispySelectionBoxOverlay,
    VispyTransformBoxOverlay,
)
from minapari._vispy.overlays.labels_polygon import VispyLabelsPolygonOverlay
from minapari._vispy.overlays.scale_bar import VispyScaleBarOverlay
from minapari._vispy.overlays.text import VispyTextOverlay
from minapari._vispy.overlays.zoom import VispyZoomOverlay
from minapari.components.overlays import (
    AxesOverlay,
    BoundingBoxOverlay,
    BrushCircleOverlay,
    ColorBarOverlay,
    LabelsPolygonOverlay,
    Overlay,
    ScaleBarOverlay,
    SelectionBoxOverlay,
    TextOverlay,
    TransformBoxOverlay,
    ZoomOverlay,
)
from minapari.layers import Image, Layer
from minapari.utils.translations import trans

layer_to_visual: dict[type[Layer], type[VispyBaseLayer]] = {
    Image: VispyImageLayer,
}


overlay_to_visual: dict[type[Overlay], type[VispyBaseOverlay]] = {
    ScaleBarOverlay: VispyScaleBarOverlay,
    TextOverlay: VispyTextOverlay,
    AxesOverlay: VispyAxesOverlay,
    BoundingBoxOverlay: VispyBoundingBoxOverlay,
    TransformBoxOverlay: VispyTransformBoxOverlay,
    SelectionBoxOverlay: VispySelectionBoxOverlay,
    BrushCircleOverlay: VispyBrushCircleOverlay,
    LabelsPolygonOverlay: VispyLabelsPolygonOverlay,
    ZoomOverlay: VispyZoomOverlay,
    ColorBarOverlay: VispyColorBarOverlay,
}


def create_vispy_layer(
    layer: Layer, *args: Any, **kwargs: Any
) -> VispyBaseLayer:
    """Create vispy visual for a layer based on its layer type."""
    for cls in layer.__class__.mro():
        if cls in layer_to_visual:
            return layer_to_visual[cls](layer, *args, **kwargs)

    raise TypeError(
        trans._(
            'Could not find VispyLayer for layer of type {dtype}',
            deferred=True,
            dtype=type(layer),
        )
    )


def create_vispy_overlay(overlay: Overlay, **kwargs) -> VispyBaseOverlay:
    """Create vispy visual for Overlay based on its type."""
    for cls in overlay.__class__.mro():
        if cls in overlay_to_visual:
            return overlay_to_visual[cls](overlay=overlay, **kwargs)

    raise TypeError(
        trans._(
            'Could not find VispyOverlay for overlay of type {dtype}',
            deferred=True,
            dtype=type(overlay),
        )
    )


def get_view_direction_in_scene_coordinates(
    view: ViewBox,
    ndim: int,
    dims_displayed: tuple[int],
) -> np.ndarray | None:
    """Calculate the unit vector pointing in the direction of the view."""
    if len(dims_displayed) == 2:
        return None

    tform = view.scene.transform
    w, h = view.canvas.size

    screen_center = np.array([w / 2, h / 2, 0, 1])
    d1 = np.array([0, 0, 1, 0])
    point_in_front_of_screen_center = screen_center + d1
    p1 = tform.imap(point_in_front_of_screen_center)
    p0 = tform.imap(screen_center)
    d2 = p1 - p0

    d3 = d2[:3]
    d4 = d3 / np.linalg.norm(d3)

    d4 = d4[[2, 1, 0]]
    view_dir_world = np.zeros((ndim,))
    for i, d in enumerate(dims_displayed):
        view_dir_world[d] = d4[i]

    return view_dir_world
