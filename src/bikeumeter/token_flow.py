import os
import requests

STRAVA_CLIENT_ID = os.environ.get("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.environ.get("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.environ.get("STRAVA_REFRESH_TOKEN")

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

    print("✅ Tokens refreshed successfully!")

    # On GitHub Actions, you can’t write .env — return them instead
    return tokens["access_token"], tokens["refresh_token"]
