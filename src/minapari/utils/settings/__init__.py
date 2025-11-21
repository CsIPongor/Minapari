import warnings

from minapari.settings import *  # noqa: F403
from minapari.utils.translations import trans

warnings.warn(
    trans._(
        "'minapari.utils.settings' has moved to 'minapari.settings' in 0.4.11. This will raise an ImportError in a future version",
        deferred=True,
    ),
    FutureWarning,
    stacklevel=2,
)
