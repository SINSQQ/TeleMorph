"""Tests for ``telemorph.utils``."""

from __future__ import annotations

from telemorph.utils import (
    SUPPORTED_API_TYPES,
    SUPPORTED_FORMATS,
    detect_format_by_extension,
    ensure_extension,
    format_bytes,
    list_api_types,
    list_formats,
    safe_session_name,
)


def test_list_formats_matches_constant() -> None:
    assert list_formats() == list(SUPPORTED_FORMATS)


def test_list_api_types_matches_constant() -> None:
    assert list_api_types() == list(SUPPORTED_API_TYPES)


def test_detect_format() -> None:
    assert detect_format_by_extension("foo.session") == "telethon"
    assert detect_format_by_extension("foo.pyrogram") == "pyrogram"
    assert detect_format_by_extension("foo.pyrosession") == "pyrogram"
    assert detect_format_by_extension("foo.kurigram") == "kurigram"
    assert detect_format_by_extension("tdata") == "tdata"
    assert detect_format_by_extension("tdata_session") == "tdata"
    assert detect_format_by_extension("unknown.unknown") == "telethon"


def test_ensure_extension_adds() -> None:
    assert ensure_extension("foo", ".session") == "foo.session"


def test_ensure_extension_keeps() -> None:
    assert ensure_extension("foo.session", ".session") == "foo.session"


def test_format_bytes_human_readable() -> None:
    assert "B" in format_bytes(512)
    assert "KB" in format_bytes(2048)
    assert "MB" in format_bytes(5 * 1024 * 1024)


def test_safe_session_name() -> None:
    assert safe_session_name("/tmp/session.session") == "session"
    assert safe_session_name("pyro.pyrogram") == "pyro"
    assert safe_session_name("kurigram_session.kurigram") == "kurigram_session"