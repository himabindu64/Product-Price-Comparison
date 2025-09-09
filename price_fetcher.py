# utils/price_fetcher.py
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# 🔍 Amazon
def search_amazon(product_name):
    url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return []

    soup = BeautifulSoup(res.text, "lxml")
    results = []

    for item in soup.select(".s-result-item"):
        title = item.select_one("h2 span")
        price_whole = item.select_one(".a-price-whole")
        price_fraction = item.select_one(".a-price-fraction")
        link = item.select_one("a.a-link-normal")

        if title and price_whole and link:
            href = link["href"]
            # ✅ Only keep valid product links
            if "/dp/" in href or "/gp/product/" in href:
                price = price_whole.text + (price_fraction.text if price_fraction else "")
                results.append({
                    "store": "Amazon",
                    "title": title.text.strip(),
                    "price": f"₹{price}",
                    "url": "https://www.amazon.in" + href.split("?")[0]
                })
    return results[:5]


# 🌍 eBay
def search_ebay(product_name):
    url = f"https://www.ebay.com/sch/i.html?_nkw={product_name.replace(' ', '+')}"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return []

    soup = BeautifulSoup(res.text, "lxml")
    results = []

    for item in soup.select(".s-item"):
        title = item.select_one(".s-item__title")
        price = item.select_one(".s-item__price")
        link = item.select_one(".s-item__link")

        if title and price and link:
            results.append({
                "store": "eBay",
                "title": title.text.strip(),
                "price": price.text.strip(),
                "url": link["href"].split("?")[0]
            })
    return results[:5]


# ✅ Wrapper
def fetch_all_sites(product_name):
    return (
        search_amazon(product_name)
        + search_ebay(product_name)
    )


if __name__ == "__main__":
    product = input("Enter product name to search: ")
    for item in fetch_all_sites(product):
        print(f"{item['store']}: {item['title']} - {item['price']}")
        print(f"URL: {item['url']}\n")