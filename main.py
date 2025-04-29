from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import html
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API для парсинга BingX P2P работает!"}

@app.get("/p2p")
def get_p2p_data():
    url = "https://bingx.paycat.com/ru-ru/p2p/self-selection?fiat=KZT&type=1"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Для Railway нужно указать путь к драйверу явно
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nickname")))

        page_source = driver.page_source
        tree = html.fromstring(page_source)

        nicknames = tree.xpath('//span[contains(@class, "ellipsis") and contains(@class, "nickname")]/text()')
        amounts = tree.xpath('//span[contains(@class, "rubik-font") and contains(@class, "amount") and contains(text(), "USDT")]/text()')
        price_ranges = tree.xpath('//span[contains(@class, "c2c-calc-formula") and contains(@class, "amount")]/text()')
        prices = tree.xpath('//div[contains(@class, "rubik-font") and contains(@class, "format-price")]/text()')
        payments = [block.xpath('.//span[contains(@class, "paymethod")]/text()') for block in tree.xpath('//div[contains(@class, "payments-list")]')]

        data = []
        for i, (nickname, amount, price_range, price, payment_methods) in enumerate(zip(nicknames, amounts, price_ranges, prices, payments)):
            data.append({
                "nickname": nickname,
                "price": price,
                "available": amount,
                "limits": price_range,
                "payment_methods": payment_methods
            })

        return {"data": data}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        driver.quit()

# Запуск на Railway (порт 8080)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

