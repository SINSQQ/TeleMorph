# CLI reference

```
telemorph [-h] [--api-id ID] [--api-hash HASH] [--platform PLATFORM]
          [--randomize-device]
          <command> [...]
```

## Commands

### `list-formats`

Print every supported conversion format.

```bash
$ telemorph list-formats
telethon
pyrogram
kurigram
tdata
```

### `list-api-types`

Print every supported client API type.

```bash
$ telemorph list-api-types
android
ios
desktop
macos
web
```

### `info`

Show metadata about a session.

```bash
$ telemorph info session.session
fmt: telethon
device_model: Pixel 7
system_version: 14
app_version: 10.7.5
api_id: 4
has_auth_key: True
```

### `convert`

Convert a single session file.

```bash
telemorph convert session.session -t pyrogram -o session.pyrogram
```

### `batch-convert`

Convert every session in a directory.

```bash
telemorph batch-convert ./sessions -t tdata -o ./out --randomize-device
```