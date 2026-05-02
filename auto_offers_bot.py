from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from notifier import message_user

URL = "https://www.mercadolibre.com.ar/ofertas"

CHECK_INTERVAL = 300  # 5 minutos
MIN_DISCOUNT = 40     # %

seen_products = set()

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

def scan():
    print("Escaneando ofertas...\n")
    
    driver.get(URL)
    time.sleep(5)

    items = driver.find_elements(By.CSS_SELECTOR, "li.ui-search-layout__item")

    print(f"Productos encontrados: {len(items)}")

    new_found = 0

    for item in items:
        try:
            title = item.find_element(By.TAG_NAME, "h2").text

            price = item.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text
            price = int(price.replace(".", ""))

            try:
                old_price = item.find_element(By.CLASS_NAME, "andes-money-amount--previous").text
                old_price = int(old_price.replace(".", "").replace("$", "").strip())

                discount = int((old_price - price) / old_price * 100)

                product_id = f"{title}-{price}"

                if discount >= MIN_DISCOUNT and product_id not in seen_products:
                    seen_products.add(product_id)

                    message_user(f"🔥 OFERTA 🔥\n{title}\nAhora: ${price}\nAntes: ${old_price}\nDescuento: {discount}%")
                    print(title)
                    print(f"Ahora: ${price}")
                    print(f"Antes: ${old_price}")
                    print(f"Descuento: {discount}%")
                    print("-" * 50)

                    new_found += 1

            except:
                continue

        except:
            continue

    if new_found == 0:
        print("No hay ofertas nuevas relevantes.")

def main():
    print("Bot de ofertas iniciado...\n")
    
    try:
        while True:
            scan()
            print(f"\nEsperando {CHECK_INTERVAL} segundos...\n")
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("Bot detenido.")
        driver.quit()

if __name__ == "__main__":
    main()