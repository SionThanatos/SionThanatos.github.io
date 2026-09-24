#!/usr/bin/env python3
"""Utility script to regenerate index.json for the faux C: drive tree."""
from __future__ import annotations

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_FILE = BASE_DIR / "index.json"
SITE_PREFIX = Path("./assets/c_drive")


def build_index() -> dict:
    folders = []
    for entry in sorted(BASE_DIR.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        folder_rel = SITE_PREFIX / entry.name
        files = []
        for child in sorted(entry.iterdir()):
            if child.is_file() and not child.name.startswith("."):
                files.append(
                    {
                        "name": child.stem,
                        "path": str(folder_rel / child.name).replace("\\", "/"),
                    }
                )
        folders.append(
            {
                "name": entry.name,
                "path": str(folder_rel).replace("\\", "/"),
                "files": files,
            }
        )
    return {"folders": folders}


def write_index(data: dict) -> None:
    OUTPUT_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    data = build_index()
    write_index(data)
    print(f"Wrote {OUTPUT_FILE} with {len(data['folders'])} folder(s).")


if __name__ == "__main__":
    main()
