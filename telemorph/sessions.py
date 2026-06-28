"""
Session classes for TeleMorph.

Each class is a thin wrapper around a specific session format:

* :class:`TelethonSession`  — Telethon sqlite session.
* :class:`PyrogramSession`  — Pyrogram sqlite session.
* :class:`KurigramSession`  — Kurigram sqlite session.
* :class:`TdataSession`     — Telegram Desktop ``tdata`` folder.

Every subclass exposes the four converters ``to_telethon``,
``to_pyrogram``, ``to_kurigram`` and ``to_tdata``.
"""

from __future__ import annotations

import base64
import os
from dataclasses import dataclass, field
from typing import Optional

from .devices import DEFAULT_API_HASH, DEFAULT_API_ID, Device, get_random_device
from .utils import detect_format_by_extension


@dataclass
class SessionInfo:
    """Plain-data carrier for the bits TeleMorph needs to round-trip."""

    auth_key: bytes = b""
    user_id: int = 0
    dc_id: int = 2
    is_bot: bool = False
    test_mode: bool = False
    api_id: int = DEFAULT_API_ID
    api_hash: str = DEFAULT_API_HASH


# ----------------------------------------------------------------------
# Abstract base
# ----------------------------------------------------------------------
@dataclass
class Session:
    """Base class shared by every concrete session format."""

    device: Device
    fmt: str = "base"
    info: SessionInfo = field(default_factory=SessionInfo)
    path: Optional[str] = None
    folder: Optional[str] = None
    string: Optional[str] = None

    # ---- factories ----------------------------------------------------
    @classmethod
    def from_file(cls, path: str, *, device: Optional[Device] = None) -> "Session":
        return cls(
            device=device or get_random_device(),
            path=path,
        )

    @classmethod
    def from_string(cls, value: str, *, device: Optional[Device] = None) -> "Session":
        return cls(
            device=device or get_random_device(),
            string=value,
            info=SessionInfo(auth_key=base64.b64decode(value + "=" * (-len(value) % 4))),
        )

    @staticmethod
    def detect(path: str, *, device: Optional[Device] = None) -> "Session":
        fmt = detect_format_by_extension(path)
        return {
            "telethon": TelethonSession,
            "pyrogram": PyrogramSession,
            "kurigram": KurigramSession,
            "tdata": TdataSession,
        }[fmt].from_file(path, device=device)

    # ---- the canonical auth_key accessor -----------------------------
    @property
    def auth_key(self) -> bytes:
        if self.info.auth_key:
            return self.info.auth_key
        if self.string:
            return base64.b64decode(self.string + "=" * (-len(self.string) % 4))
        return b""

    @auth_key.setter
    def auth_key(self, value: bytes) -> None:
        self.info.auth_key = value

    # ---- conversion dispatch -----------------------------------------
    def to(self, target: str) -> "Session":
        if target == self.fmt:
            return self
        method = getattr(self, f"to_{target}", None)
        if method is None:
            raise ValueError(
                f"Cannot convert from {self.fmt!r} to {target!r}"
            )
        return method()

    def save(self, destination: str) -> str:
        from .converters import Converter

        saver = getattr(Converter, f"save_{self.fmt}", None)
        if saver is None:
            raise NotImplementedError(f"No saver for format {self.fmt!r}")
        saver(self, destination)
        return os.path.abspath(destination)


# ----------------------------------------------------------------------
# Telethon
# ----------------------------------------------------------------------
@dataclass
class TelethonSession(Session):
    fmt: str = "telethon"

    @classmethod
    def from_string(cls, value: str, *, device: Optional[Device] = None) -> "TelethonSession":
        return cls(
            device=device or get_random_device(),
            string=value,
            info=SessionInfo(
                auth_key=base64.b64decode(value + "=" * (-len(value) % 4))
            ),
        )

    def to_pyrogram(self) -> "PyrogramSession":
        from .converters import Converter
        return Converter.telethon_to_pyrogram(self)

    def to_kurigram(self) -> "KurigramSession":
        from .converters import Converter
        return Converter.telethon_to_kurigram(self)

    def to_tdata(self, folder: Optional[str] = None) -> "TdataSession":
        from .converters import Converter
        return Converter.telethon_to_tdata(self, folder=folder or "tdata_out")

    def to_telethon(self) -> "TelethonSession":
        return self


# ----------------------------------------------------------------------
# Pyrogram
# ----------------------------------------------------------------------
@dataclass
class PyrogramSession(Session):
    fmt: str = "pyrogram"

    @classmethod
    def from_string(cls, value: str, *, device: Optional[Device] = None) -> "PyrogramSession":
        return cls(
            device=device or get_random_device(),
            string=value,
            info=SessionInfo(
                auth_key=base64.b64decode(value + "=" * (-len(value) % 4))
            ),
        )

    def to_telethon(self) -> "TelethonSession":
        from .converters import Converter
        return Converter.pyrogram_to_telethon(self)

    def to_kurigram(self) -> "KurigramSession":
        from .converters import Converter
        return Converter.pyrogram_to_kurigram(self)

    def to_tdata(self, folder: Optional[str] = None) -> "TdataSession":
        from .converters import Converter
        return Converter.pyrogram_to_tdata(self, folder=folder or "tdata_out")

    def to_pyrogram(self) -> "PyrogramSession":
        return self


# ----------------------------------------------------------------------
# Kurigram
# ----------------------------------------------------------------------
@dataclass
class KurigramSession(Session):
    fmt: str = "kurigram"

    @classmethod
    def from_string(cls, value: str, *, device: Optional[Device] = None) -> "KurigramSession":
        return cls(
            device=device or get_random_device(),
            string=value,
            info=SessionInfo(
                auth_key=base64.b64decode(value + "=" * (-len(value) % 4))
            ),
        )

    def to_telethon(self) -> "TelethonSession":
        from .converters import Converter
        return Converter.kurigram_to_telethon(self)

    def to_pyrogram(self) -> "PyrogramSession":
        from .converters import Converter
        return Converter.kurigram_to_pyrogram(self)

    def to_tdata(self, folder: Optional[str] = None) -> "TdataSession":
        from .converters import Converter
        return Converter.kurigram_to_tdata(self, folder=folder or "tdata_out")

    def to_kurigram(self) -> "KurigramSession":
        return self


# ----------------------------------------------------------------------
# Tdata
# ----------------------------------------------------------------------
@dataclass
class TdataSession(Session):
    fmt: str = "tdata"
    folder: Optional[str] = None

    @classmethod
    def from_folder(cls, folder: str, *, device: Optional[Device] = None) -> "TdataSession":
        return cls(
            device=device or get_random_device(),
            folder=folder,
        )

    def to_telethon(self) -> "TelethonSession":
        from .converters import Converter
        return Converter.tdata_to_telethon(self)

    def to_pyrogram(self) -> "PyrogramSession":
        from .converters import Converter
        return Converter.tdata_to_pyrogram(self)

    def to_kurigram(self) -> "KurigramSession":
        from .converters import Converter
        return Converter.tdata_to_kurigram(self)

    def to_tdata(self, folder: Optional[str] = None) -> "TdataSession":
        if folder and folder != self.folder:
            new = TdataSession(device=self.device, folder=folder)
            new.info = self.info
            return new
        return self