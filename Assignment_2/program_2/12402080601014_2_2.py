import re
from html import unescape

def read_products(path):
    with open(path, "r", encoding="utf-8") as file:
        html = unescape(file.read())

    pattern = r'<div class="product" data-name="(.*?)" data-price="(.*?)" data-rating="(.*?)"></div>'
    matches = re.findall(pattern, html)

    products = []

    for name, price, rating in matches:
        price = float(re.sub(r"[^\d.]", "", price))
        rating = float(rating)

        products.append({
            "name": name,
            "price": price,
            "rating": rating
        })

    return products

p, k = map(int, input("Enter number of files and K: ").split())
files = [input("Enter HTML file path: ") for _ in range(p)]

unique_products = {}

for path in files:
    for product in read_products(path):
        key = product["name"].lower()

        if key not in unique_products:
            unique_products[key] = product
        else:
            old = unique_products[key]
            if (product["rating"], -product["price"]) > (
                old["rating"], -old["price"]
            ):
                unique_products[key] = product

products = sorted(
    unique_products.values(),
    key=lambda x: (-x["rating"], x["price"], x["name"].lower())
)

for product in products[:k]:
    print(product["name"], f'{product["price"]:g}', product["rating"])