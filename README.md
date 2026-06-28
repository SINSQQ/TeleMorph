# 🦋 TeleMorph

> Unified Telegram session conversion library — wraps **TGConvertor** and **opentele2** into a single, easy-to-use API.

[![PyPI](https://img.shields.io/pypi/v/telemorph.svg)](https://pypi.org/project/telemorph/)
[![Python](https://img.shields.io/pypi/pyversions/telemorph.svg)](https://pypi.org/project/telemorph/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

TeleMorph lets you convert Telegram session files between **Telethon**, **Pyrogram**, **Kurigram** and **Telegram Desktop tdata** — with realistic device fingerprinting baked in. It's the spiritual successor of [TGConvertor](https://github.com/nazar220160/TGConvertor), powered by [opentele2](https://github.com/DedInc/opentele2) under the hood.

---

## ✨ Features

- 🔄 **Convert** between Telethon / Pyrogram / Kurigram / Tdata in one call.
- 🎲 **Random device profiles** (Samsung, Pixel, Xiaomi, OnePlus, iPhone, Desktop) recognised by Telegram's servers.
- 🧰 **Single API** for both file-based and string-based sessions.
- 💻 **CLI** for terminal-driven workflows.
- 🪶 **Zero hard dependencies** — install the optional extras only when you need them.
- ⚡ **Batch conversion** for folders full of sessions.

---

## 📦 Installation

```bash
pip install telemorph

# Or with all optional backends:
pip install "telemorph[all]"
```

Extras available:
- `telemorph[telethon]` — Telethon backend.
- `telemorph[pyrogram]` — Pyrogram backend.
- `telemorph[kurigram]` — Kurigram backend.
- `telemorph[opentele]` — opentele2 tdata support.
- `telemorph[all]` — all of the above.

---

## 🚀 Quickstart

### Convert a session

```python
import asyncio
from telemorph import TeleMorph


async def main():
    tm = TeleMorph()

    # Telethon → Tdata
    out = await tm.convert("session.session", "tdata", destination="my_tdata")
    print(f"Saved to {out}")

    # Pyrogram string → Telethon file
    out = await tm.convert("user.pyrogram", "telethon", destination="user.session")
    print(f"Saved to {out}")


asyncio.run(main())
```

### Use the device randomizer

```python
from telemorph import get_random_device

device = get_random_device(platform="android")
print(device.device_model, device.system_version, device.app_version)
```

### Pick a platform explicitly

```python
from telemorph import TeleMorph

tm = TeleMorph(platform="ios")        # always use iPhone-style fingerprints
tm = TeleMorph(randomize_device=True) # randomise on every call
```

---

## 🧬 Direct Session API

For more control, drop down to the Session classes:

```python
from telemorph import (
    TelethonSession,
    PyrogramSession,
    TdataSession,
    KurigramSession,
    get_random_device,
)

device = get_random_device(platform="android")
tdata = TdataSession.from_folder("my_tdata", device=device)

pyrogram = tdata.to_pyrogram()
pyrogram.save("my_session.pyrogram")
```

Supported conversions:

| From        | → Telethon | → Pyrogram | → Kurigram | → Tdata |
|-------------|:---------:|:---------:|:---------:|:------:|
| Telethon    | ✅        | ✅        | ✅        | ✅     |
| Pyrogram    | ✅        | ✅        | ✅        | ✅     |
| Kurigram    | ✅        | ✅        | ✅        | ✅     |
| Tdata       | ✅        | ✅        | ✅        | ✅     |

---

## 💻 Command-line interface

```bash
telemorph list-formats
telemorph list-api-types

telemorph info session.session
telemorph convert session.session -t pyrogram -o session.pyrogram

telemorph batch-convert ./sessions -t tdata -o ./tdata_out --randomize-device
```

---

## 🧪 Examples

The `examples/` folder contains runnable scripts:

```bash
python examples/basic_usage.py
```

---

## 🧱 Project layout

```
TeleMorph/
├── telemorph/
│   ├── __init__.py        # public API
│   ├── core.py            # TeleMorph façade
│   ├── sessions.py        # Session subclasses
│   ├── converters.py      # Conversion engine
│   ├── devices.py         # Device randomizer
│   ├── utils.py           # Helpers
│   └── cli.py             # `telemorph` command
├── examples/
│   └── basic_usage.py
├── setup.py
├── requirements.txt
└── README.md
```

---

## 🤝 Credits

TeleMorph stands on the shoulders of giants:

- [TGConvertor](https://github.com/nazar220160/TGConvertor) by [@nazar220160](https://github.com/nazar220160) — original multi-format converter.
- [opentele2](https://github.com/DedInc/opentele2) by [@DedInc](https://github.com/DedInc) — Tdata ↔ Telethon engine.
- [Telethon](https://github.com/LonamiWebs/Telethon), [Pyrogram](https://github.com/pyrogram/pyrogram), [Kurigram](https://github.com/KurimuzonAkuma/kurigram) — the underlying MTProto libraries.

---

## 📄 License

[MIT](LICENSE) © TeleMorph Team