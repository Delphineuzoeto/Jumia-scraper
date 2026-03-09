import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# ── Add or remove URLs here anytime ───────────────────────────
URLS = [
    "https://www.jumia.com.ng/phones-tablets/",
    "https://www.jumia.com.ng/televisions/",
    "https://www.jumia.com.ng/women-clothing/",
    "https://www.jumia.com.ng/health-beauty/",
    "https://www.jumia.com.ng/home-office/",
]


def get_product_details(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        sellers = soup.select_one("p.-m.-pbs")
        sellers_score = soup.select_one("bdo.-m.-prxs")
        rating = soup.select_one(".stars._m._al")
        reviews = soup.select_one("a.-plxs._more")

        return {
            "sellers": sellers.text.strip() if sellers else None,
            "sellers_score": sellers_score.text.strip() if sellers_score else None,
            "rating": rating.text.strip().replace(" out of 5", "") if rating else None,
            "reviews": reviews.text.strip().replace("(", "").replace(")", "").replace(" verified ratings", "") if reviews else None
        }
    except Exception as e:
        print(f"⚠️ Failed: {url} — {e}")
        return {"sellers": None, "sellers_score": None, "rating": None, "reviews": None}


def scrape_category(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.select('article.prd')
    
    # extract category name from URL
    category = url.split(".com.ng/")[1].replace("/", "")

    data = []
    for product in products:
        name = product.select_one(".name").text.strip()
        price = product.select_one(".prc").text.strip()
        discount = product.select_one(".bdg._dsct")
        discount = discount.text.strip() if discount else "No discount"
        product_url = "https://www.jumia.com.ng" + product.select_one("a.core")["href"]

        data.append({
            "category": category,
            "name": name,
            "price": price,
            "discount": discount,
            "url": product_url
        })

    return data


def run_scraper(urls=URLS):
    all_data = []

    for url in urls:
        print(f"\n🛒 Scraping: {url}")
        data = scrape_category(url)
        print(f"  Found {len(data)} products")

        enriched_data = []
        for item in data:
            print(f"  → {item['name'][:50]}")
            details = get_product_details(item['url'])
            enriched_data.append({**item, **details})
            time.sleep(1)

        all_data.extend(enriched_data)
        print(f"  ✅ Category done — {len(enriched_data)} products")

    df = pd.DataFrame(all_data)
    df['reviews'] = df['reviews'].fillna(0)
    print(f"\n✅ Total products scraped: {len(df)}")
    return df


if __name__ == "__main__":
    df = run_scraper()
    df.to_csv("jumia_phones.csv", index=False)
    print(f"✅ Saved to jumia_phones.csv")