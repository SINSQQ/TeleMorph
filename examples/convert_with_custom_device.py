"""
Force a specific device fingerprint when converting.

Useful when you want every converted session to look identical on
Telegram's server side (e.g. multi-account setups that share hardware).
"""

from __future__ import annotations

import asyncio

from telemorph import (
    Device,
    KurigramSession,
    PyrogramSession,
    TdataSession,
    TelethonSession,
)


async def main() -> None:
    # Hand-craft a device profile.
    pixel = Device(
        device_model="Pixel 8 Pro",
        system_version="14",
        app_version="10.7.5",
        sdk=34,
        manufacturer="Google",
        app_build="48123",
        lang_pack="android",
        api_id=4,
        api_hash="014b35b6184100b085b0d0572f9b5103",
    )

    # Build a session that uses this device.
    session = TelethonSession.from_file("session.session", device=pixel)
    print("Source device :", session.device.device_model)

    # Convert through every supported format — the device sticks.
    pyro = session.to_pyrogram()
    print("Pyrogram  dev :", pyro.device.device_model)

    kuri = session.to_kurigram()
    print("Kurigram  dev :", kuri.device.device_model)

    tdat = session.to_tdata(folder="custom_tdata")
    print("Tdata     dev :", tdat.device.device_model)

    # Save them all.
    pyro.save("session.pyrogram")
    kuri.save("session.kurigram")
    tdat.save("custom_tdata")

    print("✅ Saved all variants.")


if __name__ == "__main__":
    asyncio.run(main())