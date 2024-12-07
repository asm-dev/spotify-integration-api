import json
import os

STORED_TOKEN = os.path.join("data", "access_token.json")

def load_stored_token():
    try:
        with open(STORED_TOKEN, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise ValueError("No existe fichero de almacenado del token.")
    except json.JSONDecodeError:
        raise ValueError("Error en el JSON.")

def save_token(data):
    with open(STORED_TOKEN, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def reset_token():
    initial_data = {
        "access_token": None,
        "refresh_token": None,
        "expiration_time": None
    }
    with open(STORED_TOKEN, "w", encoding="utf-8") as file:
        json.dump(initial_data, file, indent=4)