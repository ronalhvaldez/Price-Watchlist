import requests
from bs4 import BeautifulSoup

prices_requested = 0

def mercadolibre(parser: BeautifulSoup) -> int | None:
    try:
        innerText = [
            "cc" if "cuotas" in s else int(s.replace(".", ""))
            for s in parser.find_all(class_="ui-pdp-price__main-container")[0]
            .get_text(separator="\n")
            .split("\n")
            if s.replace(".", "").isdigit() or "cuotas" in s
        ]
        return int(innerText[-1 if "cc" not in innerText else innerText.index("cc") - 1])
    except:
        return None


def ebay(parser: BeautifulSoup) -> float | None:
    try:
        return float(parser.select(".x-price-primary")[0].text.replace("US $", ""))
    except:
        return None


def amazon(parser: BeautifulSoup) -> float | None:
    try:
        return float(parser.select(".aok-offscreen")[0].text.split(" ")[0].replace("US$", ""))
    except:
        return None


def mediaworld(parser: BeautifulSoup) -> float | None:
    try:
        for s in parser.find_all(class_="mms-ui-mBgaT"):
            maybe_price = s.get_text().split("\n")[0][:-1]
            if maybe_price.replace(",", "").isdigit():
                return float(maybe_price.replace(",", "."))
    except:
        return None
    return None


# 🆕 NUEVO: scraper de ofertas
def mercadolibre_offers(parser: BeautifulSoup):
    products = []

    items = parser.select("li.ui-search-layout__item")

    for item in items:
        try:
            title = item.select_one("h2").text.strip()

            price = item.select_one(".andes-money-amount__fraction").text
            price = int(price.replace(".", ""))

            old_price_tag = item.select_one(".andes-money-amount--previous")

            if old_price_tag:
                old_price = old_price_tag.text
                old_price = int(old_price.replace(".", "").replace("$", "").strip())

                discount = int((old_price - price) / old_price * 100)

                products.append((title, price, old_price, discount))
        except:
            continue

    return products


def get_price(link: str) -> int | float | None:
    global prices_requested

    shop = link.split(".")[1]
    allow_list = [mercadolibre, ebay, amazon, mediaworld]

    if shop not in [s.__name__ for s in allow_list]:
        print("Link is not from the allowed shops!")
        print(f"Allow list: {[s.__name__ for s in allow_list]}")
        return None

    user_agents = [
        "Mozilla/5.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    ]

    headers = {
        "User-Agent": user_agents[prices_requested % len(user_agents)]
    }

    prices_requested += 1

    req = requests.get(link, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")

    try:
        return allow_list[[s.__name__ for s in allow_list].index(shop)](soup)
    except:
        return None