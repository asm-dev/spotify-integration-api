from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
import requests
from spotify_service import generate_auth_url, get_api_token, get_valid_access_token

app = FastAPI()

USER_PROFILE_ENDPOINT = "https://api.spotify.com/v1/me"

@app.get("/login")
def login():
    auth_url = generate_auth_url()
    return RedirectResponse(url=auth_url)

@app.get("/callback")
async def api_callback(request: Request):
    code = request.query_params.get("code")
    error = request.query_params.get("error")

    if error:
        raise HTTPException(status_code=400, detail=f"Spotify ha retornado el siguiente error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="No se ha retornado código de autorización")
    
    get_api_token(code)

    return JSONResponse(content={"message": "El token ha sido almacenado corectamente."})

@app.get("/call_spotify_api")
def call_spotify_api():
    access_token = get_valid_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(USER_PROFILE_ENDPOINT, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()