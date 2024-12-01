from dotenv import load_dotenv
import os
import random
import string
import urllib
from fastapi import HTTPException
import requests

#Loads .env file
load_dotenv()

AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
REDIRECT_URL = os.getenv("SPOTIFY_REDIRECT")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

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

def handle_callback(code: str):
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

    return response.json()