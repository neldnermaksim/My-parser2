from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Корневой маршрут — проверка запуска
@app.get("/")
def root():
    return {"message": "Парсер цитат работает на порту 8080!"}

# Маршрут парсинга цитат
@app.get("/quotes")
def get_quotes():
    url = "http://quotes.toscrape.com"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Не удалось получить страницу"}

    soup = BeautifulSoup(response.text, "html.parser")
    quotes_html = soup.find_all("div", class_="quote")

    quotes = []
    for quote_block in quotes_html:
        text = quote_block.find("span", class_="text").get_text(strip=True)
        author = quote_block.find("small", class_="author").get_text(strip=True)
        quotes.append({
            "author": author,
            "quote": text
        })

    return {"quotes": quotes}

# Явный запуск на порту 8080
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

