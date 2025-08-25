import gspread, os
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("sheets_creds.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = os.environ.get("GOOGLE_SHEET_ID")



