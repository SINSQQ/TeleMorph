"""Tests for ``telemorph.core`` — the ``TeleMorph`` façade."""

from __future__ import annotations

import asyncio

import pytest

from telemorph import TeleMorph


@pytest.fixture()
def tm() -> TeleMorph:
    return TeleMorph(api_id=4, api_hash="x" * 32, platform="android")


def test_device_returns_android(tm) -> None:
    device = tm.device()
    assert device.lang_pack == "android"
    assert device.api_id == 4


def test_convert_unknown_format_raises(tm, tmp_session_path) -> None:
    tmp_session_path = __import__("pathlib").Path(tmp_session_path)
    tmp_session_path.write_bytes(b"")
    with pytest.raises(ValueError):
        tm.convert_sync(str(tmp_session_path), "nope")


def test_convert_sync_telethon_to_pyrogram(tm, tmp_session_path, tmp_pyrogram_path) -> None:
    from telemorph.converters import Converter
    from telemorph.sessions import TelethonSession

    key = bytes(range(64))
    session = TelethonSession.from_string(__import__("base64").b64encode(key).decode())
    Converter.save_telethon(session, tmp_session_path)

    out = tm.convert_sync(tmp_session_path, "pyrogram", destination=tmp_pyrogram_path)
    assert out.endswith(".pyrogram")
    assert out == tmp_pyrogram_path


def test_info_sync(tm, tmp_session_path) -> None:
    from telemorph.converters import Converter
    from telemorph.sessions import TelethonSession

    key = bytes(range(64))
    session = TelethonSession.from_string(__import__("base64").b64encode(key).decode())
    Converter.save_telethon(session, tmp_session_path)

    info = tm.info_sync(tmp_session_path)
    assert info["fmt"] == "telethon"
    assert info["has_auth_key"] is True


def test_convert_many_sync(tm, tmp_path) -> None:
    from telemorph.converters import Converter
    from telemorph.sessions import TelethonSession

    files = []
    for i in range(2):
        p = tmp_path / f"acc{i}.session"
        session = TelethonSession.from_string(
            __import__("base64").b64encode(bytes(range(64))).decode()
        )
        Converter.save_telethon(session, str(p))
        files.append(str(p))

    results = tm.convert_many_sync(files, "tdata", output_dir=str(tmp_path / "out"))
    assert len(results) == 2