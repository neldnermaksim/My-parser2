from fastapi import FastAPI, Query
import requests
from bs4 import BeautifulSoup
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Парсер цитат на порту 8080 готов!"}

@app.get("/quotes")
def get_quotes(author: str = Query(None), limit: int = Query(10)):
    url = "http://quotes.toscrape.com"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Не удалось получить страницу"}

    soup = BeautifulSoup(response.text, "html.parser")
    quotes_html = soup.find_all("div", class_="quote")

    quotes = []
    for quote_block in quotes_html:
        text = quote_block.find("span", class_="text").get_text(strip=True)
        quote_author = quote_block.find("small", class_="author").get_text(strip=True)

        if author and author.lower() not in quote_author.lower():
            continue  # Пропустить, если автор не совпадает

        quotes.append({
            "author": quote_author,
            "quote": text
        })

        if len(quotes) >= limit:
            break

    return {"quotes": quotes}

# Запуск на Railway через порт 8080
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
