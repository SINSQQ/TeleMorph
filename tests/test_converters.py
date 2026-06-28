"""Tests for ``telemorph.converters``."""

from __future__ import annotations

import sqlite3

from telemorph.converters import Converter
from telemorph.sessions import (
    KurigramSession,
    PyrogramSession,
    TdataSession,
    TelethonSession,
)


def _make_telethon(auth_key: bytes) -> TelethonSession:
    return TelethonSession.from_string(
        __import__("base64").b64encode(auth_key).decode()
    )


def test_telethon_to_pyrogram_preserves_key() -> None:
    key = bytes(range(64))
    src = _make_telethon(key)
    out = Converter.telethon_to_pyrogram(src)
    assert isinstance(out, PyrogramSession)
    assert out.auth_key == key


def test_telethon_to_kurigram_preserves_key() -> None:
    key = bytes(range(64))
    src = _make_telethon(key)
    out = Converter.telethon_to_kurigram(src)
    assert isinstance(out, KurigramSession)
    assert out.auth_key == key


def test_telethon_to_tdata_preserves_key() -> None:
    key = bytes(range(64))
    src = _make_telethon(key)
    out = Converter.telethon_to_tdata(src, folder="/tmp/tdata_x")
    assert isinstance(out, TdataSession)
    assert out.auth_key == key
    assert out.folder == "/tmp/tdata_x"


def test_save_telethon(tmp_path) -> None:
    dest = tmp_path / "session.session"
    session = _make_telethon(bytes(range(32)))
    out = Converter.save_telethon(session, str(dest))
    assert out.endswith(".session")
    with sqlite3.connect(out) as db:
        tables = {row[0] for row in db.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
    assert {"sessions", "entities", "sent_files", "update_state"} <= tables


def test_save_pyrogram(tmp_path) -> None:
    dest = tmp_path / "session.pyrogram"
    session = Converter.telethon_to_pyrogram(_make_telethon(bytes(range(32))))
    out = Converter.save_pyrogram(session, str(dest))
    assert out.endswith(".pyrogram")


def test_save_kurigram(tmp_path) -> None:
    dest = tmp_path / "session.kurigram"
    session = Converter.telethon_to_kurigram(_make_telethon(bytes(range(32))))
    out = Converter.save_kurigram(session, str(dest))
    assert out.endswith(".kurigram")


def test_save_tdata(tmp_path) -> None:
    dest = tmp_path / "tdata_out"
    session = Converter.telethon_to_tdata(
        _make_telethon(bytes(range(32))), folder=str(dest)
    )
    out = Converter.save_tdata(session, str(dest))
    assert (tmp_path / "tdata_out" / "key_datas" / "data").exists()
    assert (tmp_path / "tdata_out" / "key_datas" / "config").exists()