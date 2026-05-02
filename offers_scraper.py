import requests
from bs4 import BeautifulSoup
from price_getter import mercadolibre_offers

URL = "https://www.mercadolibre.com.ar/ofertas"

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("Buscando ofertas...")

res = requests.get(URL, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

products = mercadolibre_offers(soup)

print(f"Encontrados {len(products)} productos\n")

for title, price, old_price, discount in products:
    if discount >= 40:
        print(f"{title}")
        print(f"Ahora: ${price}")
        print(f"Antes: ${old_price}")
        print(f"Descuento: {discount}%")
        print("-" * 40)