import uuid
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import requests
from services.songs_service import retrieve_songs, save_songs
from services.spotify_service import get_auth_url, get_access_token, get_valid_token
from services.users_service import retrieve_users, save_users, get_user_by_id, create_user, update_user, delete_user


app = FastAPI()

USER_PROFILE_ENDPOINT = "https://api.spotify.com/v1/me"
SEARCH_ENDPOINT = "https://api.spotify.com/v1/search"
TOP_TRACKS_ENDPOINT = f"{USER_PROFILE_ENDPOINT}/top/tracks"

@app.get("/login")
def login():
    return RedirectResponse(url=get_auth_url())

@app.get("/callback")
async def api_callback(request: Request):
    code = request.query_params.get("code")
    error = request.query_params.get("error")

    if error:
        raise HTTPException(status_code=400, detail=f"Spotify ha retornado el siguiente error: {error}")
    if not code:
        raise HTTPException(status_code=400, detail="No se ha retornado código de autorización")
    
    get_access_token(code)

    return HTMLResponse(content=f'''
        <html>
            <body>
                <h1>El token ha sido almacenado correctamente.</h1>
                <p>Puedes ir a la documentación para probar los endpoints <a href="/docs">aquí</a>.</p>
            </body>
        </html>
    ''')

@app.get("/search")
def search(search_term: str, type: str = "track", limit: int = 5):
    if not search_term.strip():
        raise HTTPException(status_code=400, detail="Has de agregar al menos un término de búsqueda.")
    
    access_token = get_valid_token()
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
    access_token = get_valid_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    request_params = {
        "time_range": time_range,
        "limit": limit
    }

    response = requests.get(TOP_TRACKS_ENDPOINT, headers=headers, params=request_params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

@app.post("/songs/")
def create_song(title: str, artist: str, album: str):
    songs = retrieve_songs()
    new_song = {
        "id": str(uuid.uuid4()),
        "title": title,
        "artist": artist,
        "album": album
    }
    songs.append(new_song)
    save_songs(songs)

    return {
        "message": f'La nueva canción "{new_song["title"]}" ha sido creada con éxito.',
        "song": new_song
    }

@app.get("/songs/")
def read_songs_data():
    return retrieve_songs()

@app.get("/songs/{song_id}")
def read_song(song_id: str):
    songs = retrieve_songs()
    for song in songs:
        if song["id"] == song_id:
            return {
                "message": f'La canción "{song["title"]}" ha sido encontrada.',
                "song": song
            }
    raise HTTPException(status_code=404, detail="Canción no encontrada")

@app.put("/songs/{song_id}")
def update_song(song_id: str, title: str, artist: str, album: str):
    songs = retrieve_songs()
    for song in songs:
        if song["id"] == song_id:
            song["title"] = title
            song["artist"] = artist
            song["album"] = album
            save_songs(songs)
            return song
    raise HTTPException(status_code=404, detail="Canción no encontrada")

@app.delete("/songs/{song_id}")
def delete_song(song_id: str):
    songs = retrieve_songs()
    for song in songs:
        if song["id"] == song_id:
            songs.remove(song)
            save_songs(songs)
            return {"message": f'La canción "{song["title"]}" ha sido eliminada.'}
    raise HTTPException(status_code=404, detail="Canción no encontrada")

@app.delete("/songs/")
def delete_all_songs():
    save_songs([])

    return {"message": "Todas las canciones han sido eliminadas exitosamente."}

@app.post("/save-top-tracks")
def save_top_tracks(time_range: str = "medium_term", limit: int = 10):
    top_tracks = get_top_tracks(time_range, limit)

    if not top_tracks.get("items"):
        raise HTTPException(status_code=404, detail="Error. No se han recibido canciones desde la API de Spotify.")

    for track in top_tracks["items"]:
        create_song(
            title=track["name"],
            artist=", ".join([artist["name"] for artist in track["artists"]]),
            album=track["album"]["name"]
        )

    return {"message": f"Se han guardado tus {len(top_tracks['items'])} canciones favoritas."}

@app.get("/users/")
def get_all_users():
    return retrieve_users()

@app.get("/users/{user_id}")
def get_user(user_id: str):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return user

@app.post("/users/")
def create_new_user(name: str, email: str):
    if not name.strip() or not email.strip():
        raise HTTPException(status_code=400, detail="Nombre y correo electrónico son obligatorios.")

    new_user = create_user(name, email)
    return {
        "message": f"El usuario '{new_user['name']}' ha sido creado.",
        "user": new_user
    }

@app.put("/users/{user_id}")
def update_existing_user(user_id: str, name: str = None, email: str = None):
    if not name and not email:
        raise HTTPException(status_code=400, detail="Por favor proporciona al menos un campo para actualizar (nombre o email).")

    try:
        updated_user = update_user(user_id, name=name, email=email)
        return {
            "message": f"El usuario '{updated_user['name']}' ha sido actualizado correctamente.",
            "user": updated_user
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@app.delete("/users/{user_id}")
def delete_existing_user(user_id: str):
    try:
        delete_user(user_id)
        return {"message": f"El usuario con ID '{user_id}' ha sido eliminado con éxito."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/users/")
def delete_all_users():
    save_users([])
    return {"message": "Todos los usuarios han sido eliminados"}
