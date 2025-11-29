from __future__ import annotations
from typing import Any
from pathlib import Path
import json


def ensure_dirs(*paths: str) -> None:
    """
    Creates the given directories if they do not already exist.
    Keeps file handling tidy and predictable.
    """
    for p in paths:
        Path(p).mkdir(parents=True, exist_ok=True)


def save_json(obj: Any, path: str) -> None:
    """
    Serialises an object to JSON with basic formatting.
    Useful for snapshots and replay.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def save_text(text: str, path: str) -> None:
    """
    Writes plain text or Markdown content to disk.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
