# API reference

## `TeleMorph`

```python
from telemorph import TeleMorph

tm = TeleMorph(
    api_id: int = 4,
    api_hash: str = "014b35b6184100b085b0d0572f9b5103",
    platform: Optional[str] = None,        # android | ios | desktop | macos | web
    randomize_device: bool = False,
)
```

### Methods

| Method                            | Description                                      |
|-----------------------------------|--------------------------------------------------|
| `tm.device()`                     | Return the next device fingerprint.              |
| `tm.from_file(path)`              | Auto-detect format and return a Session.         |
| `tm.from_telethon_file(path)`     | Load a Telethon session.                         |
| `tm.from_pyrogram_file(path)`     | Load a Pyrogram session.                         |
| `tm.from_kurigram_file(path)`     | Load a Kurigram session.                         |
| `tm.from_tdata(folder)`           | Load a Tdata folder.                             |
| `tm.from_telethon_string(value)`  | Load a Telethon string session.                  |
| `tm.from_pyrogram_string(value)`  | Load a Pyrogram string session.                  |
| `tm.from_kurigram_string(value)`  | Load a Kurigram string session.                  |
| `tm.convert(src, fmt, dest=...)`  | Async single conversion.                         |
| `tm.convert_sync(...)`            | Sync single conversion.                          |
| `tm.convert_many(sources, fmt)`   | Async batch conversion.                          |
| `tm.convert_many_sync(...)`       | Sync batch conversion.                           |
| `tm.info(src)`                    | Inspect a session.                               |
| `tm.info_sync(src)`               | Sync inspect.                                    |

## Sessions

```python
from telemorph import TelethonSession, PyrogramSession, KurigramSession, TdataSession

s = TelethonSession.from_file("session.session")
s.to_pyrogram()  # → PyrogramSession
s.to_kurigram()  # → KurigramSession
s.to_tdata(folder="my_tdata")  # → TdataSession
s.save("out.session")
```

## Device

```python
from telemorph import Device

Device(
    device_model="Pixel 8 Pro",
    system_version="14",
    app_version="10.7.5",
    sdk=34,
    manufacturer="Google",
    app_build="48123",
    lang_pack="android",
    api_id=4,
    api_hash="...",
)
```