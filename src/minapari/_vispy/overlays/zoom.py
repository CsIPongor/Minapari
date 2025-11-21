"""Vispy zoom box overlay."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from minapari._vispy.overlays.base import ViewerOverlayMixin, VispyCanvasOverlay
from minapari._vispy.visuals.interaction_box import InteractionBox
from minapari.settings import get_settings

if TYPE_CHECKING:
    from minapari.components.overlays import ZoomOverlay
    from minapari.components.viewer_model import ViewerModel
    from minapari.utils.events import Event


class VispyZoomOverlay(ViewerOverlayMixin, VispyCanvasOverlay):
    """Zoom box overlay.."""

    def __init__(
        self,
        viewer: ViewerModel,
        overlay: ZoomOverlay,
        parent: Optional[Any] = None,
    ):
        super().__init__(
            node=InteractionBox(),
            viewer=viewer,
            overlay=overlay,
            parent=parent,
        )

        self.overlay.events.position.connect(self._on_position_change)

        self._on_visible_change()

    def _on_position_change(self, _evt: Optional[Event] = None) -> None:
        """Change position."""
        settings = get_settings()
        self.node._highlight_width = (
            settings.appearance.highlight.highlight_thickness
        )
        self.node._edge_color = settings.appearance.highlight.highlight_color

        top_left, bot_right = self.overlay.position
        self.node.set_data(
            # invert axes for vispy
            top_left[::-1],
            bot_right[::-1],
            handles=False,
            selected=None,
        )

    def reset(self) -> None:
        """Reset the overlay."""
        super().reset()
