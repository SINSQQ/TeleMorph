"""
The ``TeleMorph`` façade — the only class most users need.

It wraps the lower-level Session / Converter objects and exposes a
fluent, both-async-and-sync API:

    tm = TeleMorph()
    await tm.convert("session.session", "tdata", destination="my_tdata")
    info = tm.info_sync("session.session")
"""

from __future__ import annotations

import asyncio
import os
from typing import Optional, Union

from .devices import Device, get_random_device
from .sessions import (
    KurigramSession,
    PyrogramSession,
    Session,
    TdataSession,
    TelethonSession,
)
from .utils import (
    SUPPORTED_FORMATS,
    detect_format_by_extension,
    ensure_extension,
    safe_session_name,
)


class TeleMorph:
    """High-level entry point for every TeleMorph operation."""

    def __init__(
        self,
        api_id: int = 4,
        api_hash: str = "014b35b6184100b085b0d0572f9b5103",
        *,
        platform: Optional[str] = None,
        randomize_device: bool = False,
    ) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.platform = platform
        self.randomize_device = randomize_device

    # ------------------------------------------------------------------
    # Device helpers
    # ------------------------------------------------------------------
    def device(self) -> Device:
        """Return a ``Device`` to use for the next conversion."""
        return get_random_device(
            platform=self.platform,
            api_id=self.api_id,
            api_hash=self.api_hash,
        )

    # ------------------------------------------------------------------
    # Loaders
    # ------------------------------------------------------------------
    @classmethod
    def from_file(
        cls,
        path: str,
        *,
        device: Optional[Device] = None,
    ) -> Session:
        """Auto-detect the format of *path* and return the right session."""
        fmt = detect_format_by_extension(path)
        instance = cls()
        if fmt == "telethon":
            return instance.from_telethon_file(path, device=device)
        if fmt == "pyrogram":
            return instance.from_pyrogram_file(path, device=device)
        if fmt == "kurigram":
            return instance.from_kurigram_file(path, device=device)
        if fmt == "tdata":
            return instance.from_tdata(path, device=device)
        raise ValueError(f"Unknown format for path: {path}")

    def from_telethon_file(self, path: str, *, device: Optional[Device] = None) -> TelethonSession:
        return TelethonSession.from_file(path, device=device or self.device())

    def from_pyrogram_file(self, path: str, *, device: Optional[Device] = None) -> PyrogramSession:
        return PyrogramSession.from_file(path, device=device or self.device())

    def from_kurigram_file(self, path: str, *, device: Optional[Device] = None) -> KurigramSession:
        return KurigramSession.from_file(path, device=device or self.device())

    def from_tdata(self, folder: str, *, device: Optional[Device] = None) -> TdataSession:
        return TdataSession.from_folder(folder, device=device or self.device())

    @staticmethod
    def from_telethon_string(value: str, *, device: Optional[Device] = None) -> TelethonSession:
        return TelethonSession.from_string(value, device=device)

    @staticmethod
    def from_pyrogram_string(value: str, *, device: Optional[Device] = None) -> PyrogramSession:
        return PyrogramSession.from_string(value, device=device)

    @staticmethod
    def from_kurigram_string(value: str, *, device: Optional[Device] = None) -> KurigramSession:
        return KurigramSession.from_string(value, device=device)

    # ------------------------------------------------------------------
    # Conversions
    # ------------------------------------------------------------------
    async def convert(
        self,
        source: Union[str, Session],
        target_format: str,
        *,
        destination: Optional[str] = None,
        device: Optional[Device] = None,
    ) -> str:
        """Asynchronously convert *source* into *target_format*."""
        return await asyncio.to_thread(
            self.convert_sync, source, target_format, destination=destination, device=device
        )

    def convert_sync(
        self,
        source: Union[str, Session],
        target_format: str,
        *,
        destination: Optional[str] = None,
        device: Optional[Device] = None,
    ) -> str:
        """Synchronously convert *source* into *target_format*."""
        if target_format not in SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported target format: {target_format!r}. "
                f"Choose one of: {list(SUPPORTED_FORMATS)}"
            )

        # 1) Load the source session.
        if isinstance(source, Session):
            session = source
        else:
            session = self.from_file(source, device=device)

        # 2) Pick a device for the output if requested.
        if self.randomize_device and device is None:
            session.device = self.device()

        # 3) Convert.
        converted = session.to(target_format)

        # 4) Choose a destination if none provided.
        if destination is None:
            base = (
                safe_session_name(session.path or session.folder or "session")
            )
            ext_map = {
                "telethon": ".session",
                "pyrogram": ".pyrogram",
                "kurigram": ".kurigram",
                "tdata": "",
            }
            if target_format == "tdata":
                destination = base + "_tdata"
            else:
                destination = ensure_extension(
                    base + "_converted", ext_map[target_format]
                )

        # 5) Persist.
        return converted.save(destination)

    async def convert_many(
        self,
        sources: list[Union[str, Session]],
        target_format: str,
        *,
        output_dir: Optional[str] = None,
    ) -> list[str]:
        """Async wrapper around :meth:`convert_many_sync`."""
        return await asyncio.to_thread(
            self.convert_many_sync, sources, target_format, output_dir=output_dir
        )

    def convert_many_sync(
        self,
        sources: list[Union[str, Session]],
        target_format: str,
        *,
        output_dir: Optional[str] = None,
    ) -> list[str]:
        """Convert a batch of sessions."""
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        results: list[str] = []
        for src in sources:
            if output_dir:
                base = safe_session_name(
                    src.path if isinstance(src, Session) else str(src)
                )
                ext_map = {
                    "telethon": ".session",
                    "pyrogram": ".pyrogram",
                    "kurigram": ".kurigram",
                    "tdata": "",
                }
                if target_format == "tdata":
                    dest = os.path.join(output_dir, base + "_tdata")
                else:
                    dest = os.path.join(
                        output_dir, base + ext_map[target_format]
                    )
            else:
                dest = None
            results.append(self.convert_sync(src, target_format, destination=dest))
        return results

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------
    async def info(self, source: Union[str, Session]) -> dict[str, object]:
        return await asyncio.to_thread(self.info_sync, source)

    def info_sync(self, source: Union[str, Session]) -> dict[str, object]:
        if isinstance(source, Session):
            session = source
        else:
            session = self.from_file(source)

        return {
            "format": session.fmt,
            "device_model": session.device.device_model,
            "system_version": session.device.system_version,
            "app_version": session.device.app_version,
            "api_id": session.device.api_id,
            "path": session.path,
            "folder": session.folder,
            "has_auth_key": bool(session.auth_key),
        }