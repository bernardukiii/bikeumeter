# make requests to strava API
import requests, os
from dotenv import load_dotenv

load_dotenv()

STRAVA_API = "https://www.strava.com/api/v3/athlete/activities"

def get_activities(access_token):
    commute_acts = [] # local list || not global

    url = f"{STRAVA_API}"
    headers = { "Authorization": f"Bearer {access_token}" }
    params = { "per_page": 1 } # i'm only interested in the latest ones || 4 in case I do 2 commute activities per day

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status() # if errors
    # raw activities = all of them
    unfiltered_acts = response.json()
    # filter activities
    for act in unfiltered_acts:
        act_name = act['name'].lower()
        if 'commute' in act_name or 'swpf' in act_name or 'swapfiets' in act_name:
            commute_acts.append(act)
    return commute_acts
