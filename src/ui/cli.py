"""Command-line interface (simple argparse stub)."""
from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="soundscape-manager")
    parser.add_argument("--list", action="store_true", help="List available scenes")
    parser.add_argument("--activate", metavar="SCENE", help="Activate a named scene")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    ns = parser.parse_args(argv)
    if ns.list:
        print("(stub) scenes: none")
    if ns.activate:
        print(f"(stub) activate {ns.activate}")


if __name__ == "__main__":
    main()
