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
print(values_list)

