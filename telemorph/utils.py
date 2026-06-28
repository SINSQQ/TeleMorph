"""
Small helpers shared across TeleMorph.

* Format & API type catalogues.
* File-extension heuristics.
* Human-readable byte sizes.
"""

from __future__ import annotations

import os
from typing import Literal

SUPPORTED_FORMATS: tuple[str, ...] = (
    "telethon",
    "pyrogram",
    "kurigram",
    "tdata",
)

SUPPORTED_API_TYPES: tuple[str, ...] = (
    "android",
    "ios",
    "desktop",
    "macos",
    "web",
)

_Format = Literal["telethon", "pyrogram", "kurigram", "tdata"]
_ApiType = Literal["android", "ios", "desktop", "macos", "web"]


def list_formats() -> list[str]:
    """Return the list of conversion formats TeleMorph supports."""
    return list(SUPPORTED_FORMATS)


def list_api_types() -> list[str]:
    """Return the list of API types TeleMorph supports."""
    return list(SUPPORTED_API_TYPES)


def detect_format_by_extension(path: str) -> _Format:
    """Heuristic — pick a format from a file path's extension."""
    lower = path.lower()
    if lower.endswith(".pyrogram") or lower.endswith(".pyrosession"):
        return "pyrogram"
    if lower.endswith(".kurigram"):
        return "kurigram"
    if "tdata" in os.path.basename(lower):
        return "tdata"
    return "telethon"


def ensure_extension(path: str, extension: str) -> str:
    """Append *extension* to *path* if it isn't already there."""
    if not path.endswith(extension):
        return path + extension
    return path


def safe_session_name(path: str) -> str:
    """Return *path* without its directory and extension."""
    base = os.path.basename(path)
    for ext in (".session", ".pyrogram", ".pyrosession", ".kurigram"):
        if base.endswith(ext):
            return base[: -len(ext)]
    return os.path.splitext(base)[0]


def format_bytes(num: int) -> str:
    """Render *num* bytes as a short, human-readable string."""
    size = float(num)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"