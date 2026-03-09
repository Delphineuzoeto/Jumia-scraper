import pandas as pd
import requests
from bs4 import BeautifulSoup
import time


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

# ── SCRAPE LISTING PAGE ────────────────────────────────────────
url = "https://www.jumia.com.ng/phones-tablets/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
products = soup.select('article.prd')

data = []
# for product in products:
#     name = product.select_one(".name").text.strip()
#     price = product.select_one(".prc").text.strip()
#     discount = product.select_one(".bdg._dsct")
#     discount = discount.text.strip() if discount else "No discount"
#     product_url = "https://www.jumia.com.ng" + product.select_one("a.core")["href"]

#     data.append({
#         "name": name,
#         "price": price,
#         "discount": discount,
#         "url": product_url
#     })

# ── ENRICH WITH PRODUCT DETAILS ────────────────────────────────
# enriched_data = []
# for item in data:
#     print(f"Scraping: {item['name'][:50]}")
#     details = get_product_details(item['url'])
#     enriched_data.append({**item, **details})
#     time.sleep(2)

# ── SAVE ───────────────────────────────────────────────────────
# df = pd.DataFrame(enriched_data)
# df.to_csv("jumia_phones.csv", index=False)
# print(f"\n✅ Done! {len(df)} products saved to jumia_phones.csv")
# print(df.head())

df = pd.read_csv("jumia_phones.csv")
print(df.columns.tolist())
print(df.shape)

#check null values
print(df.isnull().sum())

#get the name, sellers and rating thats still null
print(df[df['reviews'].isnull()][['name', 'sellers', 'rating']])

#fill the null reviews with 0
df['reviews'] = df["reviews"].fillna(0)
df.to_csv("jumia_phones.csv", index=False)
print("\n✅ Null reviews filled with 0 and saved to jumia_phones.csv")