"""
Command-line interface for TeleMorph.

Usage:

    telemorph list-formats
    telemorph list-api-types
    telemorph info session.session
    telemorph convert SOURCE -t FORMAT -o OUTPUT
    telemorph batch-convert DIR -t FORMAT -o OUTPUT_DIR
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from typing import Sequence

from .core import TeleMorph
from .utils import SUPPORTED_API_TYPES, SUPPORTED_FORMATS


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="telemorph",
        description="Unified Telegram session conversion.",
    )
    parser.add_argument("--api-id", type=int, default=4)
    parser.add_argument(
        "--api-hash",
        type=str,
        default="014b35b6184100b085b0d0572f9b5103",
    )
    parser.add_argument(
        "--platform",
        choices=SUPPORTED_API_TYPES,
        default=None,
        help="Force a specific client platform (android / ios / desktop ...).",
    )
    parser.add_argument(
        "--randomize-device",
        action="store_true",
        help="Pick a fresh device fingerprint for every conversion.",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-formats", help="List supported conversion formats.")
    sub.add_parser("list-api-types", help="List supported client API types.")

    info = sub.add_parser("info", help="Show metadata about a session file.")
    info.add_argument("source")

    convert = sub.add_parser("convert", help="Convert a single session file.")
    convert.add_argument("source")
    convert.add_argument("-t", "--to", dest="target", required=True,
                         choices=SUPPORTED_FORMATS)
    convert.add_argument("-o", "--output", dest="output", default=None)

    batch = sub.add_parser(
        "batch-convert", help="Convert every session in a directory."
    )
    batch.add_argument("source_dir")
    batch.add_argument("-t", "--to", dest="target", required=True,
                       choices=SUPPORTED_FORMATS)
    batch.add_argument("-o", "--output-dir", dest="output_dir", default=None)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.command == "list-formats":
        for fmt in SUPPORTED_FORMATS:
            print(fmt)
        return 0

    if args.command == "list-api-types":
        for api in SUPPORTED_API_TYPES:
            print(api)
        return 0

    tm = TeleMorph(
        api_id=args.api_id,
        api_hash=args.api_hash,
        platform=args.platform,
        randomize_device=args.randomize_device,
    )

    if args.command == "info":
        info = tm.info_sync(args.source)
        for key, value in info.items():
            print(f"{key}: {value}")
        return 0

    if args.command == "convert":
        out = tm.convert_sync(args.source, args.target, destination=args.output)
        print(out)
        return 0

    if args.command == "batch-convert":
        files = sorted(
            os.path.join(args.source_dir, f)
            for f in os.listdir(args.source_dir)
            if f.endswith((".session", ".pyrogram", ".pyrosession", ".kurigram"))
        )
        results = tm.convert_many_sync(
            files, args.target, output_dir=args.output_dir
        )
        for r in results:
            print(r)
        return 0

    return 2


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())