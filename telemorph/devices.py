"""
Device fingerprint generator for TeleMorph.

The profiles below are real device fingerprints shipped with the
official Telegram clients. Picking a random one makes converted
sessions look authentic to Telegram's anti-fraud heuristics.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional

DEFAULT_API_ID: int = 4
DEFAULT_API_HASH: str = "014b35b6184100b085b0d0572f9b5103"


@dataclass
class Device:
    """Immutable snapshot of a Telegram client fingerprint."""

    device_model: str = ""
    system_version: str = ""
    app_version: str = ""
    sdk: int = 0
    manufacturer: str = ""
    app_build: str = ""
    lang_pack: str = "android"
    api_id: int = DEFAULT_API_ID
    api_hash: str = DEFAULT_API_HASH
    extra: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serialisable snapshot of the profile."""
        return {
            "device_model": self.device_model,
            "system_version": self.system_version,
            "app_version": self.app_version,
            "sdk": self.sdk,
            "manufacturer": self.manufacturer,
            "app_build": self.app_build,
            "lang_pack": self.lang_pack,
            "api_id": self.api_id,
            "api_hash": self.api_hash,
            **self.extra,
        }


# ----------------------------------------------------------------------
# Built-in catalogue of fingerprints used by `get_random_device()`.
# ----------------------------------------------------------------------
DEVICE_PROFILES: list[Device] = [
    # Samsung
    Device(
        device_model="SM-G998B", system_version="13", app_version="10.6.1",
        sdk=33, manufacturer="Samsung", app_build="45777", lang_pack="android",
    ),
    Device(
        device_model="SM-S908B", system_version="14", app_version="10.7.5",
        sdk=34, manufacturer="Samsung", app_build="48123", lang_pack="android",
    ),
    # Google Pixel
    Device(
        device_model="Pixel 7", system_version="14", app_version="10.7.5",
        sdk=34, manufacturer="Google", app_build="48123", lang_pack="android",
    ),
    Device(
        device_model="Pixel 8 Pro", system_version="14", app_version="10.7.5",
        sdk=34, manufacturer="Google", app_build="48123", lang_pack="android",
    ),
    # Xiaomi
    Device(
        device_model="Mi 11", system_version="13", app_version="10.5.2",
        sdk=33, manufacturer="Xiaomi", app_build="45123", lang_pack="android",
    ),
    Device(
        device_model="Redmi Note 12", system_version="13", app_version="10.6.0",
        sdk=33, manufacturer="Xiaomi", app_build="45555", lang_pack="android",
    ),
    # OnePlus
    Device(
        device_model="OnePlus 11", system_version="14", app_version="10.7.2",
        sdk=34, manufacturer="OnePlus", app_build="47654", lang_pack="android",
    ),
    # Huawei
    Device(
        device_model="HUAWEI Mate 60 Pro", system_version="12", app_version="10.5.0",
        sdk=32, manufacturer="HUAWEI", app_build="44789", lang_pack="android",
    ),
    # iOS
    Device(
        device_model="iPhone 15 Pro", system_version="17.5.1", app_version="10.7",
        sdk=0, manufacturer="Apple", app_build="42000", lang_pack="ios",
    ),
    Device(
        device_model="iPhone 14", system_version="17.4", app_version="10.6.5",
        sdk=0, manufacturer="Apple", app_build="41700", lang_pack="ios",
    ),
    Device(
        device_model="iPhone 13", system_version="17.2", app_version="10.6.0",
        sdk=0, manufacturer="Apple", app_build="41200", lang_pack="ios",
    ),
    # Desktop
    Device(
        device_model="Desktop", system_version="4.16.8", app_version="4.16.8",
        sdk=0, manufacturer="Telegram", app_build="47373", lang_pack="tdesktop",
    ),
    Device(
        device_model="MacBook Pro", system_version="11.5.2", app_version="10.6.3",
        sdk=0, manufacturer="Apple", app_build="45600", lang_pack="macos",
    ),
]


_PLATFORM_MAP: dict[str, str] = {
    "android": "android",
    "ios": "ios",
    "desktop": "tdesktop",
    "macos": "macos",
    "web": "web",
}


def get_devices_by_platform(platform: str) -> list[Device]:
    """Return every built-in device whose ``lang_pack`` matches *platform*."""
    target = _PLATFORM_MAP.get(platform)
    if target is None:
        raise ValueError(
            f"Unknown platform {platform!r}. "
            f"Expected one of: {sorted(_PLATFORM_MAP)}"
        )
    return [d for d in DEVICE_PROFILES if d.lang_pack == target]


def get_random_device(
    platform: Optional[str] = None,
    *,
    api_id: Optional[int] = None,
    api_hash: Optional[str] = None,
) -> Device:
    """Return a random ``Device``, optionally filtered by *platform*.

    Parameters
    ----------
    platform:
        ``"android"``, ``"ios"``, ``"desktop"``, ``"macos"`` or ``"web"``.
        If omitted, picks from the full catalogue.
    api_id, api_hash:
        Override the Telegram API credentials on the returned device.
    """
    if platform is None:
        pool = DEVICE_PROFILES
    else:
        pool = get_devices_by_platform(platform)
        if not pool:
            raise ValueError(f"No device profiles registered for platform={platform!r}")

    device = random.choice(pool)
    if api_id is not None:
        device.api_id = api_id
    if api_hash is not None:
        device.api_hash = api_hash
    return device