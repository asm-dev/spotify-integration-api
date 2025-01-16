import json
import os
import uuid

USERS_FILE = os.path.join("data", "users.json")

def retrieve_users():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        raise ValueError("Error en el JSON de usuarios.")

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)

def get_user_by_id(user_id):
    users = retrieve_users()
    for user in users:
        if user["id"] == user_id:
            return user
    return None

def create_user(name, email):
    users = retrieve_users()
    new_user = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "preferences": []
    }
    users.append(new_user)
    save_users(users)
    return new_user

def update_user(user_id, name=None, email=None):
    users = retrieve_users()
    for user in users:
        if user["id"] == user_id:
            if name:
                user["name"] = name
            if email:
                user["email"] = email
            save_users(users)
            return user
    raise ValueError("Usuario no encontrado.")

def delete_user(user_id):
    users = retrieve_users()
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            save_users(users)
            return True
    raise ValueError("Usuario no encontrado.")