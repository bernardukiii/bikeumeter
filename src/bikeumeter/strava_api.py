# make requests to strava API
import requests, os
from dotenv import load_dotenv

load_dotenv()

STRAVA_API = os.environ.get("STRAVA_API")
STRAVA_ACCESS_TOKEN = os.environ.get("STRAVA_ACCESS_TOKEN")

def get_activities():
    url = f"{STRAVA_API}"
    headers = {
        "Authorization": f"Bearer {STRAVA_ACCESS_TOKEN}"
    }