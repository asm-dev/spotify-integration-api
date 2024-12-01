from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from spotify_service import generate_auth_url, handle_callback

app = FastAPI()

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
    
    token_data = handle_callback(code)

    return JSONResponse(content=token_data)