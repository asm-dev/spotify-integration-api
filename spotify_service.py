import time
from dotenv import load_dotenv
from fastapi import HTTPException
import os
import random
import string
import urllib
import requests

#Loads .env file
load_dotenv()

AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
REDIRECT_URL = "http://localhost:8000/callback"
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

stored_token = {
    "access_token": None,
    "refresh_token": None,
    "expiration_time": None,
}

def create_random_state(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_auth_url():
    state = create_random_state()
    scope = "user-top-read user-read-private user-read-email"
    
    query = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URL,
        "scope": scope,
        "state": state
    }

    return f"{AUTH_URL}?{urllib.parse.urlencode(query)}"

def get_token(code: str):
    client_token = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URL,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    response = requests.post(SPOTIFY_TOKEN_URL, data=client_token)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"No se ha devuelto ningún token: {response.text}")

    received_token = response.json()

    access_token = received_token.get("access_token")
    refresh_token = received_token.get("refresh_token")
    expiration_time = time.time() + received_token.get("expires_in", 0)

    if not access_token:
        raise ValueError("No se recibió el access_token del servidor de Spotify.")
    
    stored_token["access_token"] = access_token
    stored_token["refresh_token"] = refresh_token
    stored_token["expiration_time"] = expiration_time

    if not stored_token["refresh_token"]:
        raise ValueError("No se ha recibido el token de refresco.")

def refresh_token():
    refresh_token = stored_token["refresh_token"]

    if not refresh_token:
        raise ValueError("No se puede refrescar el token de acceso sin token de refresco.")
    
    refresh_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    response = requests.post(SPOTIFY_TOKEN_URL, data=refresh_data)

    if not response.status_code is 200:
        raise Exception("No se ha podido refrescar el token de acceso.")
    
    new_token = response.json()

    stored_token["access_token"] = new_token["access_token"]
    stored_token["expiration_time"] = time.time() + new_token["expires_in"]

def get_valid_access_token():
    accessToken = stored_token["access_token"]
    tokenExpiration = stored_token["expiration_time"]

    if accessToken is None:
        raise ValueError("El token de acceso no está definido. Por favor ve a /login")
    if tokenExpiration is None:
        raise ValueError("Tiempo de expiración del token de acceso sin definir.")
    
    isExpired = tokenExpiration < time.time()

    if accessToken and not isExpired:
        return accessToken

    return refresh_token()