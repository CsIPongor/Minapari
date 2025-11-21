"""This module contains actions (functions) that operate on layers."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np

from minapari.layers import Image, Layer
from minapari.layers._source import layer_source
from minapari.layers.utils import stack_utils
from minapari.layers.utils._link_layers import get_linked_layers
from minapari.utils.translations import trans

if TYPE_CHECKING:
    from minapari.components import LayerList


def _duplicate_layer(ll: LayerList, *, name: str = '') -> None:
    from copy import deepcopy

    for lay in list(ll.selection):
        data, state, type_str = lay.as_layer_data_tuple()
        state['name'] = trans._('{name} copy', name=lay.name)
        with layer_source(parent=lay):
            new = Layer.create(deepcopy(data), state, type_str)
        ll.insert(ll.index(lay) + 1, new)


def _split_stack(ll: LayerList, axis: int = 0) -> None:
    layer = ll.selection.active
    if not isinstance(layer, Image):
        return
    if layer.rgb:
        with_alpha = layer.data.shape[-1] == 4
        images = stack_utils.split_rgb(layer, with_alpha=with_alpha)
    else:
        images = stack_utils.stack_to_images(layer, axis)
    ll.remove(layer)
    ll.extend(images)
    ll.selection = set(images)  # type: ignore


def _split_rgb(ll: LayerList) -> None:
    return _split_stack(ll)


def _merge_stack(ll: LayerList, rgb: bool = False) -> None:
    imgs = cast(list[Image], [layer for layer in ll if layer in ll.selection])
    merged = (
        stack_utils.merge_rgb(imgs)
        if rgb
        else stack_utils.images_to_stack(imgs)
    )
    for layer in imgs:
        ll.remove(layer)
    ll.append(merged)


def _toggle_visibility(ll: LayerList) -> None:
    current_visibility_state = []
    for layer in ll.selection:
        current_visibility_state.append(layer.visible)

    for visibility, layer in zip(
        current_visibility_state, ll.selection, strict=False
    ):
        if layer.visible == visibility:
            layer.visible = not visibility


def _show_selected(ll: LayerList) -> None:
    for lay in ll.selection:
        lay.visible = True


def _hide_selected(ll: LayerList) -> None:
    for lay in ll.selection:
        lay.visible = False


def _show_unselected(ll: LayerList) -> None:
    for lay in ll:
        if lay not in ll.selection:
            lay.visible = True


def _hide_unselected(ll: LayerList) -> None:
    for lay in ll:
        if lay not in ll.selection:
            lay.visible = False


def _link_selected_layers(ll: LayerList) -> None:
    ll.link_layers(ll.selection)


def _unlink_selected_layers(ll: LayerList) -> None:
    ll.unlink_layers(ll.selection)


def _select_linked_layers(ll: LayerList) -> None:
    linked_layers_in_list = [
        x for x in get_linked_layers(*ll.selection) if x in ll
    ]
    ll.selection.update(linked_layers_in_list)


def _project(ll: LayerList, axis: int = 0, mode: str = 'max') -> None:
    layer = ll.selection.active
    if not layer:
        return
    if not isinstance(layer, Image):
        raise NotImplementedError(
            trans._(
                'Projections are only implemented for images', deferred=True
            )
        )

    data = (getattr(np, mode)(layer.data, axis=axis, keepdims=False),)
    meta = {
        key: layer._get_base_state()[key]
        for key in layer._get_base_state()
        if key
        not in (
            'scale',
            'translate',
            'rotate',
            'shear',
            'affine',
            'axis_labels',
            'units',
        )
    }
    meta.update(
        {
            'name': f'{layer} {mode}-proj',
            'colormap': layer.colormap.name,
            'rendering': layer.rendering,
        }
    )
    new = Layer.create(data, meta, layer._type_string)
    new._transforms = layer._transforms.set_slice(
        [ax for ax in range(layer.ndim) if ax != axis]
    )
    ll.append(new)


def _toggle_bounding_box(ll: LayerList) -> None:
    for layer in ll.selection:
        layer.bounding_box.visible = not layer.bounding_box.visible


def _toggle_colorbar(ll: LayerList) -> None:
    for layer in ll.selection:
        if not hasattr(layer, 'colorbar'):
            raise NotImplementedError(
                trans._(
                    'Colorbar is only implemented for Images',
                    deferred=True,
                )
            )
        layer.colorbar.visible = not layer.colorbar.visible
