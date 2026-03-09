import gspread
from google.oauth2.service_account import Credentials
import pandas as pd


def connect_to_sheets():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    return client


def push_to_sheets(df, sheet_url):
    client = connect_to_sheets()
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0)
    worksheet.clear()
    # convert column headers into a list +  converts data rows into a list of lists
    worksheet.update([df.columns.tolist()] + df.values.tolist())
    print(f"✅ {len(df)} rows pushed to Google Sheets")


if __name__ == "__main__":
    print("Starting...")
    df = pd.read_csv("jumia_phones.csv")
    print(f"Loaded {len(df)} rows")
    push_to_sheets(df, "https://docs.google.com/spreadsheets/d/1iXoPlCIDyo_s6VV7zXkPvZn4fuUS6Hks1lBdiQgWI5Q/edit")