"""Stub implementation of action manager for minapari.

This is a minimal implementation to allow imports to work.
Full functionality would require integration with app-model.
"""

from typing import Any, Callable


class ActionManager:
    """Minimal stub for action manager functionality."""

    def __init__(self):
        self._actions: dict[str, Any] = {}
        self._shortcuts: dict[str, list[str]] = {}
        self._buttons: dict[str, Any] = {}

    def register_action(
        self,
        name: str,
        callback: Callable | None = None,
        description: str = "",
        **kwargs: Any,
    ) -> None:
        """Register an action.

        Parameters
        ----------
        name : str
            Action name
        callback : Callable, optional
            Callback function
        description : str
            Action description
        **kwargs
            Additional arguments
        """
        # Create a simple action object
        class Action:
            def __init__(self, desc: str):
                self.description = desc

        self._actions[name] = Action(description)

    def bind_shortcut(self, action_name: str, shortcut: str) -> None:
        """Bind a keyboard shortcut to an action.

        Parameters
        ----------
        action_name : str
            Name of the action
        shortcut : str
            Keyboard shortcut
        """
        if action_name not in self._shortcuts:
            self._shortcuts[action_name] = []
        self._shortcuts[action_name].append(shortcut)

    def unbind_shortcut(self, action_name: str) -> None:
        """Unbind all shortcuts for an action.

        Parameters
        ----------
        action_name : str
            Name of the action
        """
        if action_name in self._shortcuts:
            self._shortcuts[action_name] = []

    def bind_button(
        self,
        action_name: str,
        button: Any,
        **kwargs: Any,
    ) -> None:
        """Bind a button to an action.

        Parameters
        ----------
        action_name : str
            Name of the action
        button : Any
            Button widget
        **kwargs
            Additional arguments
        """
        self._buttons[action_name] = button

    def trigger(self, action_name: str) -> None:
        """Trigger an action.

        Parameters
        ----------
        action_name : str
            Name of the action to trigger
        """
        # In a full implementation, this would call the registered callback
        pass

    def _get_repeatable_shortcuts(self, keymap_chain: Any) -> list[str]:
        """Get list of repeatable shortcuts.

        Parameters
        ----------
        keymap_chain : Any
            Keymap chain

        Returns
        -------
        list[str]
            List of repeatable shortcuts
        """
        # Return empty list for stub implementation
        return []


# Global action manager instance
action_manager = ActionManager()
