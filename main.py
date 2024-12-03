from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
import requests
from spotify_service import generate_auth_url, get_api_token, get_valid_access_token

app = FastAPI()

USER_PROFILE_ENDPOINT = "https://api.spotify.com/v1/me"
SEARCH_ENDPOINT = "https://api.spotify.com/v1/search"
TOP_TRACKS_ENDPOINT = f"{USER_PROFILE_ENDPOINT}/top/tracks"

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

@app.get("/search")
def search(search_term: str, type: str = "track", limit: int = 5):
    if not search_term.strip():
        raise HTTPException(status_code=400, detail="Has de agregar al menos un término de búsqueda.")
    
    access_token = get_valid_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    request_params = {
        "q": search_term,
        "type": type,
        "limit": limit
    }
    
    response = requests.get(SEARCH_ENDPOINT, headers=headers, params=request_params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

@app.get("/top-tracks")
def get_top_tracks(time_range: str = "medium_term", limit: int = 10):
    access_token = get_valid_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    request_params = {
        "time_range": time_range,
        "limit": limit
    }

    response = requests.get(TOP_TRACKS_ENDPOINT, headers=headers, params=request_params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()