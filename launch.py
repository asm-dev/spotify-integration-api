import atexit
import uvicorn
import webbrowser
from services.token_store_service import reset_token

if __name__ == "__main__":
    atexit.register(reset_token)
    webbrowser.open("http://127.0.0.1:8000/login")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)