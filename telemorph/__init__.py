"""
TeleMorph — unified Telegram session conversion library.

Public API
----------
    >>> from telemorph import TeleMorph, get_random_device

    >>> tm = TeleMorph()
    >>> await tm.convert("session.session", "tdata", destination="my_tdata")
"""

from __future__ import annotations

from .core import TeleMorph
from .devices import (
    DEFAULT_API_HASH,
    DEFAULT_API_ID,
    DEVICE_PROFILES,
    Device,
    get_devices_by_platform,
    get_random_device,
)
from .sessions import (
    KurigramSession,
    PyrogramSession,
    Session,
    SessionInfo,
    TdataSession,
    TelethonSession,
)
from .utils import (
    SUPPORTED_API_TYPES,
    SUPPORTED_FORMATS,
    detect_format_by_extension,
    ensure_extension,
    format_bytes,
    list_api_types,
    list_formats,
    safe_session_name,
)

__version__ = "1.0.0"
__all__ = [
    "DEFAULT_API_HASH",
    "DEFAULT_API_ID",
    "DEVICE_PROFILES",
    "Device",
    "KurigramSession",
    "PyrogramSession",
    "Session",
    "SessionInfo",
    "SUPPORTED_API_TYPES",
    "SUPPORTED_FORMATS",
    "TdataSession",
    "TeleMorph",
    "TelethonSession",
    "detect_format_by_extension",
    "ensure_extension",
    "format_bytes",
    "get_devices_by_platform",
    "get_random_device",
    "list_api_types",
    "list_formats",
    "safe_session_name",
]