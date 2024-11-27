from dotenv import load_dotenv
import requests
import os

#Loads .env file
load_dotenv()

API_BASE_URL = "https://api.spotify.com/v1"
TOKEN = os.getenv("SPOTY_TOKEN")