"""
Working with *string* sessions — base64-encoded auth_keys that you can
embed in env vars, configs or databases instead of shipping binary
sqlite files around.
"""

from __future__ import annotations

import asyncio

from telemorph import (
    PyrogramSession,
    TelethonSession,
    get_random_device,
)


async def main() -> None:
    device = get_random_device(platform="android")

    # 1) Load a Telethon string.
    tele_str = "your_telethon_string_here"
    tele_session = TelethonSession.from_string(tele_str, device=device)
    print("Telethon auth_key length:", len(tele_session.auth_key))

    # 2) Convert it to Pyrogram string format.
    pyro_session = tele_session.to_pyrogram()
    print("Pyrogram  auth_key length:", len(pyro_session.auth_key))

    # 3) Round-trip — load the Pyrogram string back.
    reloaded = PyrogramSession.from_string(
        pyro_session.string or "", device=device
    )
    print("Round-trip auth_key match:", reloaded.auth_key == pyro_session.auth_key)


if __name__ == "__main__":
    asyncio.run(main())