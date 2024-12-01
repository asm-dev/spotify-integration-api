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
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
REDIRECT_URL = os.getenv("SPOTIFY_REDIRECT")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

token = {
    "access_token": None,
    "refresh_token": None,
    "expiration_time": None,
}

def create_random_state(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_auth_url():
    state = create_random_state()
    scope = "user-read-private user-read-email"
    
    query = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URL,
        "scope": scope,
        "state": state
    }

    return f"{AUTH_URL}?{urllib.parse.urlencode(query)}"

def get_api_token(code: str):
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

    token["access_token"] = received_token["access_token"]
    token["refresh_token"] = received_token["refresh_token"]
    token["expiration_time"] = received_token["expires_in"]

def refresh_token():
    refresh_token = token["refresh_token"]

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
    
    new_token = response.json

    token["access_token"] = new_token["access_token"]
    token["expiration_time"] = time.time() + new_token["expires_in"]

def get_valid_access_token():
    if token["access_token"] and token["expiration_time"] > time.time():
        return token["access_token"]

    return refresh_token()