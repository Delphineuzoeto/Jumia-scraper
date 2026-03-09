
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time


url = "https://www.jumia.com.ng/phones-tablets/"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')


# grab all the products on the page
products = soup.select('article.prd')

#find the seller name 
# print(products[0].prettify())


# curate a function to call the product details and return a dictionary of the details
def get_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    raw_html = response.text

    sellers = soup.select_one("p.-m.-pbs")
    sellers_score = soup.select_one("bdo.-m.-prxs")
    rating = soup.select_one(".stars._m._al")
    reviews = soup.select_one("a.-plxs._more")

    return{
        "sellers": sellers.text.strip() if sellers else None,
        "sellers_score": sellers_score.text.strip() if sellers_score else None,
        "rating": rating.text.strip().replace(" out of 5", "") if rating else None,
        "reviews": reviews.text.strip().replace("(", "").replace(")", "").replace(" verified ratings", "") if reviews else None
    }



data = []

for product in products:
    name = product.select_one(".name").text.strip()
    price = product.select_one(".prc").text.strip()
    discount = product.select_one(".bdg._dsctt")
    discount = discount.text.strip() if discount else "No discount"
    url = "https://www.jumia.com.ng" + product.select_one("a.core")["href"]

    data.append({
        "name": name,
        "price": price,
        "discount": discount,
        "url": url
    })



#loop through the products and get the data for product in products:
enriched_data = []

for item in data:
    print(f"Scraping:{item['name'][:50]}")
    details = get_product_details(item['url'])
    enriched_data.append({**item, **details})
    time.sleep(2)
    print(f"Done! {len(enriched_data)} products scraped")
    # print(f"collected {len(data)} products")
    # print(data[0])

# save the data to a CSV file
# df = pd.DataFrame(data)
# df.to_csv("jumia_phones.csv", index=False)

print()

test_url = data[0]['url']
# print(test_url)
test_response = requests.get(test_url)
# print(test_response.status_code)

test_soup = BeautifulSoup(test_response.text, 'html.parser') 
# print(test_soup.prettify()[50000:53000])

scripts = test_soup.find_all("scripts")

for script in scripts:
    if script.string and "FINET" in script.string:
        print(script.string[:2000], 'printed')
        break

#find the index of the string "FINET" in the raw HTML and print a portion of the HTML around it 
raw_html = test_response.text
index = raw_html.find("FINET")
# print(raw_html[index-200:index+200])

sellers = test_soup.select_one("p.-m.-pbs").text.strip()
sellers_score = test_soup.select_one("bdo.-m.-prxs").text.strip()
print(f"Sellers: {sellers}, Sellers Score: {sellers_score}")

index = raw_html.find("reviews")
print(raw_html[index-200:index+200])

rating = test_soup.select_one(".stars._m._al")
reviews = test_soup.select_one("a.-plxs._more")

rating = rating.text.strip().replace(" out of 5", "") if rating else None
reviews = reviews.text.strip().replace("(", "").replace(")", "").replace(" verified ratings", "") if reviews else None

print("Rating:", rating)
print("Reviews:", reviews)

details = get_product_details(data[0]['url'])
print(details)

df_enriched = pd.DataFrame(enriched_data)
df_enriched.to_csv("jumia_phones.csv", index=False)
print(df_enriched.head())
print(df_enriched.columns.tolist())
