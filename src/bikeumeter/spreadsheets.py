import gspread, os
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("../../sheets_creds.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = os.environ.get("GOOGLE_SHEET_ID")
sheet = client.open_by_key(sheet_id)

values_list = sheet.sheet1.row_values(1)


# function to write the activities to the sheet - takes the arg activity
def write_activity_to_sheet(activity):
    # I do need to add the public transport fare to this append_row function - but when I manage to calculate it by scraping
    sheet.append_row([activity["id"], activity["name"], activity["start_location"], activity["end_location"], activity["distance"], activity["date"]])
