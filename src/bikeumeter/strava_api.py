# make requests to strava API
import requests, os
from dotenv import load_dotenv

load_dotenv()

STRAVA_API = os.environ.get("STRAVA_API")
STRAVA_ACCESS_TOKEN = os.environ.get("STRAVA_ACCESS_TOKEN")

commute_acts = []

def get_activities():
    url = f"{STRAVA_API}"
    headers = {
        "Authorization": f"Bearer {STRAVA_ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status() # if errors
    # raw activities = all of them
    unfiltered_acts = response.json()
    # filter activities
    for act in unfiltered_acts:
        act_name = act['name'].lower()
        print('activity', act)
        print('Activity name: ', act_name)
        if 'commute' in act_name:
            commute_acts.append(act)
    return commute_acts