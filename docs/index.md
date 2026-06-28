# TeleMorph

> Unified Telegram session conversion library — wraps **TGConvertor** and **opentele2** into a single, easy-to-use API.

## What is TeleMorph?

TeleMorph lets you convert Telegram session files between **Telethon**, **Pyrogram**, **Kurigram** and **Telegram Desktop tdata** — with realistic device fingerprinting baked in.

## Features

- Convert between 4 formats: telethon, pyrogram, kurigram, tdata.
- 14+ realistic device profiles out of the box.
- Async and sync APIs.
- CLI: ``telemorph``.
- Zero hard dependencies — install extras only when you need them.

## Quickstart

```python
import asyncio
from telemorph import TeleMorph


async def main():
    tm = TeleMorph()
    out = await tm.convert("session.session", "tdata", destination="my_tdata")
    print(out)


asyncio.run(main())
```

## Contents

- [Getting started](getting-started.md)
- [API reference](api-reference.md)
- [CLI reference](cli.md)