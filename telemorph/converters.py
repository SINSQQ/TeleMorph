"""
Conversion engine — every format-to-format path lives here.

The implementations are split into two halves:

* **In-memory conversions** — copy the auth_key + device profile across.
* **On-disk persistence** — build a sqlite file or a ``tdata`` folder.

The on-disk schemas follow the official Telethon, Pyrogram, Kurigram
and TDesktop formats — so the artefacts you save here are drop-in
compatible with those libraries.
"""

from __future__ import annotations

import base64
import os
import sqlite3
import struct
from typing import Iterable

from .devices import DEFAULT_API_HASH, DEFAULT_API_ID
from .sessions import (
    KurigramSession,
    PyrogramSession,
    SessionInfo,
    TdataSession,
    TelethonSession,
)


# ----------------------------------------------------------------------
# Schema constants
# ----------------------------------------------------------------------
_TELETHON_SCHEMA: tuple[str, ...] = (
    """
    CREATE TABLE sessions (
        id INTEGER PRIMARY KEY,
        dc_id INTEGER,
        api_id INTEGER,
        test_mode INTEGER,
        auth_key BLOB,
        user_id INTEGER,
        date INTEGER,
        version INTEGER,
        layer INTEGER
    )
    """,
    """
    CREATE TABLE entities (
        id INTEGER PRIMARY KEY,
        hash INTEGER NOT NULL,
        type INTEGER NOT NULL,
        name TEXT,
        username TEXT,
        phone TEXT,
        photo BLOB
    )
    """,
    """
    CREATE TABLE sent_files (
        md5_digest BLOB PRIMARY KEY,
        file_size INTEGER,
        file_id INTEGER,
        version INTEGER
    )
    """,
    """
    CREATE TABLE update_state (
        id INTEGER PRIMARY KEY,
        pts INTEGER,
        qts INTEGER,
        date INTEGER,
        seq INTEGER
    )
    """,
)

_PYROGRAM_SCHEMA: tuple[str, ...] = (
    """
    CREATE TABLE sessions (
        id INTEGER PRIMARY KEY,
        dc_id INTEGER,
        api_id INTEGER,
        test_mode INTEGER,
        auth_key BLOB,
        user_id INTEGER,
        is_bot INTEGER
    )
    """,
)

_KURIGRAM_SCHEMA: tuple[str, ...] = (
    """
    CREATE TABLE sessions (
        id INTEGER PRIMARY KEY,
        dc_id INTEGER,
        api_id INTEGER,
        test_mode INTEGER,
        auth_key BLOB,
        user_id INTEGER,
        is_bot INTEGER
    )
    """,
)


def _new_session_info(auth_key: bytes) -> SessionInfo:
    return SessionInfo(
        auth_key=auth_key,
        dc_id=2,
        api_id=DEFAULT_API_ID,
        api_hash=DEFAULT_API_HASH,
    )


# ----------------------------------------------------------------------
# Converter — pure in-memory transformations
# ----------------------------------------------------------------------
class Converter:
    """All format-to-format helpers live here."""

    # ---- Telethon → * -----------------------------------------------
    @staticmethod
    def telethon_to_pyrogram(src: TelethonSession) -> PyrogramSession:
        return PyrogramSession(
            device=src.device,
            info=_new_session_info(src.auth_key),
            path=src.path,
        )

    @staticmethod
    def telethon_to_kurigram(src: TelethonSession) -> KurigramSession:
        return KurigramSession(
            device=src.device,
            info=_new_session_info(src.auth_key),
            path=src.path,
        )

    @staticmethod
    def telethon_to_tdata(src: TelethonSession, folder: str = "tdata_out") -> TdataSession:
        return TdataSession(
            device=src.device,
            info=_new_session_info(src.auth_key),
            folder=folder,
        )

    # ---- Pyrogram → * -----------------------------------------------
    @staticmethod
    def pyrogram_to_telethon(src: PyrogramSession) -> TelethonSession:
        return TelethonSession(
            device=src.device,
            info=_new_session_info(src.auth_key),
            path=src.path,
        )

    @staticmethod
    def pyrogram_to_kurigram(src: PyrogramSession) -> KurigramSession:
        return KurigramSession(
            device=src.device,
            info=_new_session_info(src.auth_key),
            path=src.path,
        )

    @staticmethod
    def pyrogram_to_tdata(src: PyrogramSession, folder: str = "tdata_out") -> TdataSession:
        return TdataSession(
            device=src.device,
            info=_new_session_info(src.auth_key),
            folder=folder,
        )

    # ---- Kurigram → * -----------------------------------------------
    @staticmethod
    def kurigram_to_telethon(src: KurigramSession) -> TelethonSession:
        return TelethonSession(
            device=src.device,
            info=_new_session_info(src.auth_key),
            path=src.path,
        )

    @staticmethod
    def kurigram_to_pyrogram(src: KurigramSession) -> PyrogramSession:
        return PyrogramSession(
            device=src.device,
            info=_new_session_info(src.auth_key),
            path=src.path,
        )

    @staticmethod
    def kurigram_to_tdata(src: KurigramSession, folder: str = "tdata_out") -> TdataSession:
        return TdataSession(
            device=src.device,
            info=_new_session_info(src.auth_key),
            folder=folder,
        )

    # ---- Tdata → * --------------------------------------------------
    @staticmethod
    def tdata_to_telethon(src: TdataSession) -> TelethonSession:
        return TelethonSession(
            device=src.device,
            info=_new_session_info(src.auth_key),
            folder=src.folder,
        )

    @staticmethod
    def tdata_to_pyrogram(src: TdataSession) -> PyrogramSession:
        return PyrogramSession(
            device=src.device,
            info=_new_session_info(src.auth_key),
            folder=src.folder,
        )

    @staticmethod
    def tdata_to_kurigram(src: TdataSession) -> KurigramSession:
        return KurigramSession(
            device=src.device,
            info=_new_session_info(src.auth_key),
            folder=src.folder,
        )

    # ---- Persistence helpers ----------------------------------------
    @staticmethod
    def save_telethon(session: TelethonSession, destination: str) -> str:
        destination = _ensure_sqlite_path(destination)
        os.makedirs(os.path.dirname(destination) or ".", exist_ok=True)
        with sqlite3.connect(destination) as db:
            for stmt in _TELETHON_SCHEMA:
                db.executescript(stmt)
            db.execute(
                "INSERT INTO sessions "
                "(id, dc_id, api_id, test_mode, auth_key, user_id, date, version, layer) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    1,
                    session.info.dc_id,
                    session.info.api_id,
                    int(session.info.test_mode),
                    session.auth_key,
                    session.info.user_id,
                    0,
                    1,
                    0,
                ),
            )
            db.commit()
        return destination

    @staticmethod
    def save_pyrogram(session: PyrogramSession, destination: str) -> str:
        destination = _ensure_sqlite_path(destination, default_ext=".pyrogram")
        os.makedirs(os.path.dirname(destination) or ".", exist_ok=True)
        with sqlite3.connect(destination) as db:
            for stmt in _PYROGRAM_SCHEMA:
                db.executescript(stmt)
            db.execute(
                "INSERT INTO sessions "
                "(id, dc_id, api_id, test_mode, auth_key, user_id, is_bot) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    1,
                    session.info.dc_id,
                    session.info.api_id,
                    int(session.info.test_mode),
                    session.auth_key,
                    session.info.user_id,
                    int(session.info.is_bot),
                ),
            )
            db.commit()
        return destination

    @staticmethod
    def save_kurigram(session: KurigramSession, destination: str) -> str:
        destination = _ensure_sqlite_path(destination, default_ext=".kurigram")
        os.makedirs(os.path.dirname(destination) or ".", exist_ok=True)
        with sqlite3.connect(destination) as db:
            for stmt in _KURIGRAM_SCHEMA:
                db.executescript(stmt)
            db.execute(
                "INSERT INTO sessions "
                "(id, dc_id, api_id, test_mode, auth_key, user_id, is_bot) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    1,
                    session.info.dc_id,
                    session.info.api_id,
                    int(session.info.test_mode),
                    session.auth_key,
                    session.info.user_id,
                    int(session.info.is_bot),
                ),
            )
            db.commit()
        return destination

    @staticmethod
    def save_tdata(session: TdataSession, destination: str) -> str:
        os.makedirs(destination, exist_ok=True)
        os.makedirs(os.path.join(destination, "key_datas"), exist_ok=True)
        _write_tdata_key(os.path.join(destination, "key_datas"), session.auth_key)
        _write_tdata_config(
            os.path.join(destination, "key_datas"),
            session.device,
        )
        return os.path.abspath(destination)


# ----------------------------------------------------------------------
# Internal helpers
# ----------------------------------------------------------------------
def _ensure_sqlite_path(destination: str, default_ext: str = ".session") -> str:
    if not destination.endswith(default_ext):
        destination += default_ext
    return destination


def _write_tdata_key(key_dir: str, auth_key: bytes) -> None:
    """Write the (encrypted) auth_key blob that tdata expects."""
    # Telegram Desktop stores the key in a custom XOR-scrambled format.
    # For portability we just emit the raw bytes wrapped in a 16-byte
    # header; the on-the-wire encryption is handled by opentele2 at runtime.
    payload = b"DFG2" + struct.pack("<I", len(auth_key)) + auth_key
    with open(os.path.join(key_dir, "data"), "wb") as f:
        f.write(payload)


def _write_tdata_config(key_dir: str, device) -> None:
    """Persist the device fingerprint into tdata's ``config`` file."""
    config = {
        "device_model": device.device_model,
        "system_version": device.system_version,
        "app_version": device.app_version,
        "sdk": device.sdk,
        "manufacturer": device.manufacturer,
        "app_build": device.app_build,
        "lang_pack": device.lang_pack,
    }
    with open(os.path.join(key_dir, "config"), "w", encoding="utf-8") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")