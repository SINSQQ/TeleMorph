# Getting started

## Installation

```bash
pip install telemorph
```

Or pick the extras you need:

```bash
pip install "telemorph[telethon]"
pip install "telemorph[pyrogram]"
pip install "telemorph[kurigram]"
pip install "telemorph[opentele]"
pip install "telemorph[all]"
```

## Your first conversion

```python
import asyncio
from telemorph import TeleMorph


async def main():
    tm = TeleMorph(api_id=4, api_hash="...")
    out = await tm.convert("session.session", "tdata", destination="my_tdata")
    print(out)


asyncio.run(main())
```

## Picking a device

```python
from telemorph import get_random_device

# Always use an Android-style fingerprint
device = get_random_device(platform="android")
print(device.device_model, device.system_version)
```

## CLI

```bash
telemorph list-formats
telemorph list-api-types
telemorph info session.session
telemorph convert session.session -t pyrogram -o session.pyrogram
telemorph batch-convert ./sessions -t tdata -o ./out --randomize-device
```