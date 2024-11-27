from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello_spoty():
    return {"message": "Hello Spotify!"}