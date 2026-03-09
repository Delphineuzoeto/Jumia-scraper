import schedule
import time
from scraper import run_scraper
from sheets import push_to_sheets
import pandas as pd

def job():
    print(('starting scheduled scrape...'))
     # Scrape
    data = run_scraper()
    #save to CSV
    df = pd.DataFrame
    df.to_csv("jumia_phonnes.csv", index=False)
    #push to sheets
    push_to_sheets(df, "https://docs.google.com/spreadsheets/d/1iXoPlCIDyo_s6VV7zXkPvZn4fuUS6Hks1lBdiQgWI5Q/edit")
    print("✅ Done! Sheet updated.")


# run immediately on start
job()

#Run every 2 hours
schedule.every(2).hours.do(job)

print('scheduler running..press  Ctrl+c to stop')
while True:
    schedule.run_pending()
    time.sleep(60)

