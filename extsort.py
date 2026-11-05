#!/usr/bin/env python3
"""Sort files in a folder into subfolders by file extension."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def extension_label(path: Path) -> str:
    suffix = path.suffix.lower().lstrip(".")
    return suffix if suffix else "_no_ext"


def collect_files(folder: Path, recursive: bool) -> list[Path]:
    if recursive:
        return [p for p in folder.rglob("*") if p.is_file()]
    return [p for p in folder.iterdir() if p.is_file()]


def plan_moves(folder: Path, files: list[Path]) -> list[tuple[Path, Path]]:
    moves: list[tuple[Path, Path]] = []
    for src in files:
        # Skip files already sitting inside an extension folder we manage
        if src.parent != folder and src.parent.parent == folder:
            if src.parent.name == extension_label(src) or src.parent.name == "_no_ext":
                continue
        dest_dir = folder / extension_label(src)
        dest = dest_dir / src.name
        if src.resolve() == dest.resolve():
            continue
        moves.append((src, dest))
    return moves


def apply_moves(moves: list[tuple[Path, Path]], dry_run: bool) -> int:
    count = 0
    for src, dest in moves:
        if dry_run:
            print(f"would move: {src.name} -> {dest.parent.name}/")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                print(f"skip (exists): {dest}", file=sys.stderr)
                continue
            shutil.move(str(src), str(dest))
            print(f"moved: {src.name} -> {dest.parent.name}/")
        count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sort files in a folder into subfolders named by extension."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=".",
        help="Folder to sort (default: current directory)",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Show what would move without changing anything",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Include files in subfolders (still sorts into top-level ext folders)",
    )
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        print(f"Not a folder: {folder}", file=sys.stderr)
        return 1

    files = collect_files(folder, args.recursive)
    # Only sort files that currently live directly in the target folder
    # unless --recursive is set (then we still land them in top-level ext dirs).
    if not args.recursive:
        files = [p for p in files if p.parent == folder]

    moves = plan_moves(folder, files)
    if not moves:
        print("Nothing to sort.")
        return 0

    n = apply_moves(moves, args.dry_run)
    print(f"{'Would sort' if args.dry_run else 'Sorted'} {n} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
