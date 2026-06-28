"""
Batch convert every Telethon ``.session`` file in a directory.

Replace ``./sessions`` with your real folder. By default TeleMorph
writes the converted files next to the originals — pass ``output_dir``
to redirect them somewhere else.
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

from telemorph import TeleMorph


async def main() -> None:
    src_dir = Path("./sessions")
    out_dir = Path("./converted")

    if not src_dir.exists():
        print(f"❌ Directory not found: {src_dir}")
        return

    files = sorted(str(p) for p in src_dir.glob("*.session"))
    if not files:
        print("⚠️  No .session files to convert.")
        return

    tm = TeleMorph(randomize_device=True)

    results = await tm.convert_many(
        files,
        "tdata",
        output_dir=str(out_dir),
    )

    print(f"✅ Converted {len(results)} sessions:")
    for src, dst in zip(files, results):
        print(f"   {os.path.basename(src)} → {dst}")


if __name__ == "__main__":
    asyncio.run(main())