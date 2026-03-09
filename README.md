# 🛒 Jumia Market Intelligence Scraper

A live web scraper that collects product pricing, discount, seller, 
and rating data from Jumia Nigeria across multiple categories.
Auto-updates every 2 hours and pushes to Google Sheets.

## 📊 What it collects
- Product name & category
- Price & discount
- Seller name & seller score
- Star rating & review count
- Stock status

## 🗂️ Categories tracked
- Phones & Tablets
- Televisions
- Women's Clothing
- Health & Beauty
- Home & Office

## ⚡ How it works
1. `scraper.py` — scrapes Jumia listing + product detail pages
2. `sheets.py` — pushes clean data to Google Sheets (one tab per category)
3. `scheduler.py` — runs automatically every 2 hours

## 🚀 Setup
```bash
python -m venv jumvenv
source jumvenv/bin/activate
pip install -r requirements.txt
python scheduler.py
```

## 🛠️ Built with
- Python, BeautifulSoup, Requests
- Pandas
- gspread + Google Sheets API
- schedule
