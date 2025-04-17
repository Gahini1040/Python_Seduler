# utils.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import CREDENTIALS_FILE

def get_gsheet_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    return gspread.authorize(creds)
