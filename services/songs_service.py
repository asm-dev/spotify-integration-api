import json
import os

SONGS = os.path.join("data", "user_songs.json")

def retrieve_songs():
    try:
        with open(SONGS, "r", encoding="utf-8") as file:
            return json.load(file)
    except not SONGS.exists():
        raise ValueError("No existe fichero de almacenado de canciones.")
    except json.JSONDecodeError:
        raise ValueError("Error en el JSON.")

def save_songs(songs):
    with open(SONGS, "w", encoding="utf-8") as file:
        json.dump(songs, file, indent=4)