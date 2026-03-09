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

    # replace NaN with empty string so Google Sheets doesn't choke
    df = df.fillna("")

    # push each category to its own tab
    for category, group in df.groupby("category"):
        print(f"  📤 Pushing {category} — {len(group)} rows")

        # create tab if it doesn't exist
        try:
            worksheet = sheet.worksheet(category)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title=category, rows=1000, cols=20)

        worksheet.clear()
        worksheet.update([group.columns.tolist()] + group.values.tolist())

    print(f"✅ Done! {len(df)} total rows pushed to Google Sheets")


if __name__ == "__main__":
    df = pd.read_csv("jumia_phones.csv")
    push_to_sheets(df, "https://docs.google.com/spreadsheets/d/1iXoPlCIDyo_s6VV7zXkPvZn4fuUS6Hks1lBdiQgWI5Q/edit")