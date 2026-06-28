"""Shared pytest fixtures."""

from __future__ import annotations

import os

import pytest

from telemorph.devices import get_random_device


@pytest.fixture()
def device():
    """Return a deterministic Android device for tests."""
    return get_random_device(platform="android")


@pytest.fixture()
def auth_key() -> bytes:
    """256 bytes of deterministic fake auth_key."""
    return bytes(range(256))


@pytest.fixture()
def tmp_session_path(tmp_path):
    """Return a writable .session file path inside a fresh tmp dir."""
    return str(tmp_path / "session.session")


@pytest.fixture()
def tmp_pyrogram_path(tmp_path):
    return str(tmp_path / "session.pyrogram")


@pytest.fixture()
def tmp_kurigram_path(tmp_path):
    return str(tmp_path / "session.kurigram")


@pytest.fixture()
def tmp_tdata_dir(tmp_path):
    folder = tmp_path / "tdata"
    folder.mkdir()
    return str(folder)


@pytest.fixture()
def tmp_tdata_output(tmp_path):
    return str(tmp_path / "tdata_out")