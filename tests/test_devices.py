"""Tests for ``telemorph.devices``."""

from __future__ import annotations

import pytest

from telemorph.devices import (
    DEFAULT_API_HASH,
    DEFAULT_API_ID,
    DEVICE_PROFILES,
    Device,
    get_devices_by_platform,
    get_random_device,
)


def test_default_credentials() -> None:
    assert DEFAULT_API_ID == 4
    assert len(DEFAULT_API_HASH) == 32


def test_device_to_dict() -> None:
    device = Device(device_model="Pixel", system_version="14", app_version="10.7")
    data = device.to_dict()
    assert data["device_model"] == "Pixel"
    assert data["system_version"] == "14"


def test_get_random_device_android() -> None:
    device = get_random_device(platform="android")
    assert device.lang_pack == "android"


def test_get_random_device_ios() -> None:
    device = get_random_device(platform="ios")
    assert device.lang_pack == "ios"


def test_get_random_device_desktop() -> None:
    device = get_random_device(platform="desktop")
    assert device.lang_pack == "tdesktop"


def test_get_random_device_invalid_platform() -> None:
    with pytest.raises(ValueError):
        get_random_device(platform="flipphone")


def test_get_devices_by_platform() -> None:
    devices = get_devices_by_platform("android")
    assert devices
    assert all(d.lang_pack == "android" for d in devices)


def test_device_profiles_have_unique_models() -> None:
    models = [d.device_model for d in DEVICE_PROFILES]
    assert len(models) == len(set(models))