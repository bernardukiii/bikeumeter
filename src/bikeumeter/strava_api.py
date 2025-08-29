# make requests to strava API
import requests, os
from dotenv import load_dotenv

load_dotenv()

STRAVA_API = os.environ.get("STRAVA_API")
STRAVA_ACCESS_TOKEN = os.environ.get("STRAVA_ACCESS_TOKEN")

def get_activities(access_token):
    commute_acts = [] # local list || not global

    url = f"{STRAVA_API}"
    headers = { "Authorization": f"Bearer {access_token}" }
    params = { "per_page": 10 } # i'm only interested in the latest ones || 4 in case I do 2 commute activities per day, but could be 2

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status() # if errors
    # raw activities = all of them
    unfiltered_acts = response.json()
    # filter activities
    for act in unfiltered_acts:
        act_name = act['name'].lower()
        if 'commute' in act_name:
            commute_acts.append(act)
    return commute_acts
