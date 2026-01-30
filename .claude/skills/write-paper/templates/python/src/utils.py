"""utils.py - Utility functions and CUD colors."""
import json
from pathlib import Path

# CUD Color Palette (Okabe-Ito)
CUD_COLORS = {
    "black": "#000000",
    "orange": "#E69F00",
    "skyblue": "#56B4E9",
    "bluishgreen": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermilion": "#D55E00",
    "reddishpurple": "#CC79A7",
}


def load_config(path: str = "config/parameters.json") -> dict:
    """Load config from JSON file."""
    with open(path, "r") as f:
        return json.load(f)


def load_json(path: str) -> dict:
    """Load JSON file."""
    with open(path, "r") as f:
        return json.load(f)


def save_json(data: dict, path: str) -> None:
    """Save data to JSON file."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {path}")


def cud(name: str) -> str:
    """Get CUD color by name."""
    return CUD_COLORS.get(name, "#000000")
