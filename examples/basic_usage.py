"""
Basic usage of TeleMorph.

This example walks through the most common workflow:

1. Build a ``TeleMorph`` instance.
2. Convert a Telethon ``.session`` to a ``tdata`` folder.
3. Convert the same source to a Pyrogram ``.pyrogram`` file.
4. Inspect the result.
"""

from __future__ import annotations

import asyncio

from telemorph import (
    PyrogramSession,
    TdataSession,
    TeleMorph,
    TelethonSession,
    get_random_device,
)


async def main() -> None:
    # 1) Build a TeleMorph instance with custom credentials.
    tm = TeleMorph(
        api_id=4,
        api_hash="014b35b6184100b085b0d0572f9b5103",
        platform="android",
    )

    print("📱 Picked device:", tm.device().device_model)

    # 2) Convert a Telethon session to tdata.
    tdata_out = await tm.convert(
        "session.session",
        "tdata",
        destination="my_tdata",
    )
    print(f"✅ Tdata saved to    {tdata_out}")

    # 3) Convert the same source to Pyrogram.
    pyro_out = await tm.convert(
        "session.session",
        "pyrogram",
        destination="session.pyrogram",
    )
    print(f"✅ Pyrogram saved to {pyro_out}")

    # 4) Inspect the result.
    info = await tm.info("session.session")
    print("ℹ️  Session info:")
    for key, value in info.items():
        print(f"   - {key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())