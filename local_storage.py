import json
import pathlib

# Using a dotfile in the user's home directory to persist settings
STORAGE_FILE = pathlib.Path.home() / ".cards_app_data.json"

def get(key):
    if not STORAGE_FILE.exists():
        return None
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(key)
    except Exception:
        return None

def set(key, value):
    data = {}
    if STORAGE_FILE.exists():
        try:
            with open(STORAGE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            pass
    data[key] = value
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
