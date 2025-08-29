import gspread, os, json
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
service_account_info = json.loads(os.environ["GOOGLE_SHEETS_CREDS"])
creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
client = gspread.authorize(creds)

sheet_id = os.environ.get("GOOGLE_SHEET_ID")
sheet = client.open_by_key(sheet_id)
db_sheet = sheet.sheet1


# function to write the activities to the sheet
def write_activity_to_sheet(activities):
    id_list = set(db_sheet.col_values(1))

    for act in activities:
        if str(act["id"]) not in id_list:
            # I do need to add the public transport fare to this append_row function - but when I manage to calculate it by scraping
            db_sheet.append_row([act["id"], act["name"], act["start_location"], act["end_location"], act["distance"], act["start_date"]])
        else: 
            print('Activity already in sheet')