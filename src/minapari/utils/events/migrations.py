import warnings
from typing import Any

from minapari.utils.events.event import WarningEmitter
from minapari.utils.translations import trans


def deprecated_class_name(
    new_class: type,
    old_name: str,
    version: str,
    since_version: str,
):
    """Create a deprecated alias for a class with a deprecation warning.

    Parameters
    ----------
    new_class : type
        The new class to use
    old_name : str
        The old deprecated name
    version : str
        Version when the old name will be removed
    since_version : str
        Version when deprecation started

    Returns
    -------
    type
        The new class (for backwards compatibility)
    """
    warnings.warn(
        f"{old_name} is deprecated since {since_version} and will be removed "
        f"in {version}. Please use {new_class.__name__} instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return new_class


class _DeprecatingDict(dict):
    """Dictionary that supports deprecated key names with warnings."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._deprecated_mappings: dict[str, tuple[str, str, str]] = {}

    def set_deprecated_from_rename(
        self,
        old_name: str,
        new_name: str,
        version: str,
        since_version: str | None = None,
    ) -> None:
        """Register a deprecated key name.

        Parameters
        ----------
        old_name : str
            The old deprecated key name
        new_name : str
            The new key name to use
        version : str
            Version when the old name will be removed
        since_version : str, optional
            Version when deprecation started
        """
        self._deprecated_mappings[old_name] = (new_name, version, since_version or "")

    def __getitem__(self, key: str) -> Any:
        if key in self._deprecated_mappings:
            new_key, version, since_version = self._deprecated_mappings[key]
            msg = f"{key} is deprecated"
            if since_version:
                msg += f" since {since_version}"
            msg += f" and will be removed in {version}. Please use {new_key} instead."
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return super().__getitem__(new_key)
        return super().__getitem__(key)

    def __setitem__(self, key: str, value: Any) -> None:
        if key in self._deprecated_mappings:
            new_key, version, since_version = self._deprecated_mappings[key]
            msg = f"{key} is deprecated"
            if since_version:
                msg += f" since {since_version}"
            msg += f" and will be removed in {version}. Please use {new_key} instead."
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            super().__setitem__(new_key, value)
        else:
            super().__setitem__(key, value)


def deprecation_warning_event(
    prefix: str,
    previous_name: str,
    new_name: str,
    version: str,
    since_version: str,
) -> WarningEmitter:
    """
    Helper function for event emitter deprecation warning.

    This event still needs to be added to the events group.

    Parameters
    ----------
    prefix:
        Prefix indicating class and event (e.g. layer.event)
    previous_name : str
        Name of deprecated event (e.g. edge_width)
    new_name : str
        Name of new event (e.g. border_width)
    version : str
        Version where deprecated event will be removed.
    since_version : str
        Version when new event name was added.

    Returns
    -------
    WarningEmitter
        Event emitter that prints a deprecation warning.
    """
    previous_path = f'{prefix}.{previous_name}'
    new_path = f'{prefix}.{new_name}'
    return WarningEmitter(
        trans._(
            '{previous_path} is deprecated since {since_version} and will be removed in {version}. Please use {new_path}',
            deferred=True,
            previous_path=previous_path,
            since_version=since_version,
            version=version,
            new_path=new_path,
        ),
        type_name=previous_name,
    )
