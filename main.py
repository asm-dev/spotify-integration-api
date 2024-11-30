from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from spotify_service import generate_auth_url

app = FastAPI()

@app.get("/login")
def login():
    auth_url = generate_auth_url()
    return RedirectResponse(url=auth_url)