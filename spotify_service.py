from dotenv import load_dotenv
import os
import random
import string
import urllib

#Loads .env file
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
REDIRECT_URL = os.getenv("SPOTIFY_REDIRECT")
AUTH_URL = "https://accounts.spotify.com/authorize"

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