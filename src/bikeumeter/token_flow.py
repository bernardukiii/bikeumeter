import os
import requests
from dotenv import load_dotenv

load_dotenv()

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

def refresh_access_token():
    url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": STRAVA_REFRESH_TOKEN,
    }

    response = requests.post(url, data=payload)
    response.raise_for_status()

    tokens = response.json()

    new_access_token = tokens["access_token"]
    new_refresh_token = tokens["refresh_token"]

    # overwrite .env with updated refresh token
    lines = []
    with open(".env", "r") as f:
        for line in f:
            if line.startswith("STRAVA_REFRESH_TOKEN="):
                lines.append(f"STRAVA_REFRESH_TOKEN={new_refresh_token}\n")
            else:
                lines.append(line)

    with open(".env", "w") as f:
        f.writelines(lines)

    print("✅ Tokens refreshed and stored successfully!")
    return new_access_token
