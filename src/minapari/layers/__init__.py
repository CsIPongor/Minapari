"""Layers are the viewable objects that can be added to a viewer.

Custom layers must inherit from Layer and pass along the
`visual node <https://vispy.org/api/vispy.scene.visuals.html>`_
to the super constructor.
"""

from minapari.layers.base import Layer
from minapari.layers.image import Image

__all__ = [
    'Image',
    'Layer',
]
