from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
import os

#Loads .env file
load_dotenv()

API_BASE_URL = "https://api.spotify.com/v1"

SPOTY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTY_REDIRECT_URL = os.getenv("SPOTIFY_REDIRECT")
SPOTY_AUTH_URL = "https://accounts.spotify.com/authorize"

@app.get("/login")
def login():
    #TODO: Conseguir parametros para auth, falta scope y state SEGURIDAD!
    query_data = {
        "response_type": "code",
        "client_id":SPOTY_CLIENT_ID,
        "redirect_url": SPOTY_REDIRECT_URL
    }

    auth_redirect_url = f"{SPOTY_AUTH_URL}?{(query_data)}"

    http_redirect_response = RedirectResponse(auth_redirect_url)

    return http_redirect_response