import json
from pathlib import Path

JSON_FILE = Path("user_songs.json")

def retrieve_songs():
    if not JSON_FILE.exists():
        return []
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_songs(songs):
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(songs, file, indent=4)