import os, requests
from dotenv import load_dotenv

load_dotenv()

STRAVA_CLIENT_ID = os.environ.get("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.environ.get("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.environ.get("STRAVA_REFRESH_TOKEN")
ENV_FILE = ".env"

def get_access_token():
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

    new_refresh_token = tokens["refresh_token"]

    # Only rewrite .env if token rotated
    if new_refresh_token != STRAVA_REFRESH_TOKEN:
        print("🔄 Refresh token rotated, updating .env...")
        update_env_file("STRAVA_REFRESH_TOKEN", new_refresh_token)

    return tokens["access_token"], tokens["expires_at"]


def update_env_file(key, value):
    # Overwrite or add a key=value in the .env file.
    lines = []
    found = False

    with open(ENV_FILE, "r") as f:
        for line in f:
            if line.startswith(f"{key}="):
                lines.append(f"{key}={value}\n")
                found = True
            else:
                lines.append(line)

    if not found:
        lines.append(f"{key}={value}\n")

    with open(ENV_FILE, "w") as f:
        f.writelines(lines)
