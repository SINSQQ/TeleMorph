"""Tests for ``telemorph.sessions``."""

from __future__ import annotations

import pytest

from telemorph.sessions import (
    KurigramSession,
    PyrogramSession,
    Session,
    SessionInfo,
    TdataSession,
    TelethonSession,
)


def test_session_info_defaults() -> None:
    info = SessionInfo()
    assert info.dc_id == 2
    assert info.is_bot is False


def test_session_to_self_returns_self() -> None:
    s = TelethonSession.from_string("abcd", device=None)
    assert s.to("telethon") is s


def test_session_invalid_target_raises() -> None:
    s = TelethonSession.from_string("abcd", device=None)
    with pytest.raises(ValueError):
        s.to("nope")


def test_session_detect_telethon(tmp_path) -> None:
    p = tmp_path / "session.session"
    p.write_bytes(b"")
    session = Session.detect(str(p))
    assert isinstance(session, TelethonSession)


def test_session_detect_pyrogram(tmp_path) -> None:
    p = tmp_path / "session.pyrogram"
    p.write_bytes(b"")
    session = Session.detect(str(p))
    assert isinstance(session, PyrogramSession)


def test_session_detect_kurigram(tmp_path) -> None:
    p = tmp_path / "session.kurigram"
    p.write_bytes(b"")
    session = Session.detect(str(p))
    assert isinstance(session, KurigramSession)


def test_tdata_from_folder() -> None:
    session = TdataSession.from_folder("./tdata_folder")
    assert session.folder == "./tdata_folder"


def test_session_auth_key_roundtrip() -> None:
    s = TelethonSession.from_string("aGVsbG8=", device=None)
    assert s.auth_key == b"hello"
    s.auth_key = b"goodbye"
    assert s.auth_key == b"goodbye"