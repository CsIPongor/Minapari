from collections.abc import Callable, Iterable, Mapping, Sequence
from functools import wraps
from pathlib import Path
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    NewType,
    Union,
)

import numpy as np
from typing_extensions import TypedDict

if TYPE_CHECKING:
    import dask.array  # noqa: ICN001
    import zarr
    from magicgui.widgets import FunctionGui
    from qtpy.QtWidgets import QWidget


__all__ = [
    'ArrayBase',
    'ArrayLike',
    'ExcInfo',
    'FullLayerData',
    'ImageData',
    'LayerData',
    'LayerDataTuple',
    'LayerTypeName',
    'PathLike',
    'PathOrPaths',
]

# Layer type name - simplified for Minapari (Image only)
LayerTypeName = Literal['image']

# Array types
ArrayLike = Union[np.ndarray, 'dask.array.Array', 'zarr.Array']

# Layer data tuples
FullLayerData = tuple[Any, Mapping, LayerTypeName]
LayerData = Union[tuple[Any], tuple[Any, Mapping], FullLayerData]

PathLike = Union[str, Path]
PathOrPaths = Union[PathLike, Sequence[PathLike]]
ReaderFunction = Callable[[PathOrPaths], list[LayerData]]
WriterFunction = Callable[[str, list[FullLayerData]], list[str]]

ExcInfo = Union[
    tuple[type[BaseException], BaseException, TracebackType],
    tuple[None, None, None],
]

# Types for GUI HookSpecs
WidgetCallable = Callable[..., Union['FunctionGui', 'QWidget']]
AugmentedWidget = Union[WidgetCallable, tuple[WidgetCallable, dict]]

# Sample Data
SampleData = Union[PathLike, Callable[..., Iterable[LayerData]]]


class SampleDict(TypedDict):
    display_name: str
    data: SampleData


ArrayBase: type[np.ndarray] = np.ndarray

# Data types - Image only for Minapari
ImageData = NewType('ImageData', np.ndarray)

LayerDataTuple = NewType('LayerDataTuple', tuple)


def image_reader_to_layerdata_reader(
    func: Callable[[PathOrPaths], ArrayLike],
) -> ReaderFunction:
    """Convert a PathLike -> ArrayLike function to a PathLike -> LayerData."""

    @wraps(func)
    def reader_function(*args, **kwargs) -> list[LayerData]:
        result = func(*args, **kwargs)
        return [(result,)]

    return reader_function
