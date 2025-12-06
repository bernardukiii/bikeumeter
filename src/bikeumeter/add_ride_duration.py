# temporary script to go over past activities and get the ride duration

# make requests to strava API
import time
import requests, os
from dotenv import load_dotenv
import gspread, os, json
from google.oauth2.service_account import Credentials
from token_flow import refresh_access_token

load_dotenv()

STRAVA_API = "https://www.strava.com/api/v3/athlete/activities"
STRAVA_CLIENT_ID = os.environ.get("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.environ.get("STRAVA_CLIENT_SECRET")
STRAVA_CLIENT_SECRET = os.environ.get("STRAVA_CLIENT_SECRET")
scopes = ["https://www.googleapis.com/auth/spreadsheets"]

access_token, new_refresh_token = refresh_access_token()

# When on github action it should go to the first if, for local runs, it should go to the else
if "GOOGLE_SHEETS_CREDS" in os.environ:
    service_account_info = json.loads(os.environ["GOOGLE_SHEETS_CREDS"])
else:
    with open("../../sheets_creds.json") as f:
        service_account_info = json.load(f)

creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
client = gspread.authorize(creds)

sheet_id = os.environ.get("GOOGLE_SHEET_ID")
sheet = client.open_by_key(sheet_id)
db_sheet = sheet.sheet1



def get_activities(access_token):
    commute_acts = []
    page = 1
    per_page = 100  # safe number

    while True:
        url = STRAVA_API
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"per_page": per_page, "page": page}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        acts = response.json()
        if not acts:
            break  # no more activities

        for act in acts:
            if 'commute' in act['name'].lower():
                commute_acts.append(act)

        page += 1
        time.sleep(5)

    return commute_acts




# function to write the activities to the sheet
def write_activity_to_sheet(activities):
    for act in activities:
        db_sheet.append_row([act["elapsed_time"]])


