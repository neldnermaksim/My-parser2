# Импортируем библиотеки
from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import os

# Создаём приложение FastAPI
app = FastAPI()

# Маршрут проверки сервера
@app.get("/")
def read_root():
    return {"message": "Парсер работает!"}

# Маршрут парсинга новостей с Hacker News
@app.get("/parse")
def parse_news():
    url = 'https://news.ycombinator.com/'  # Сайт для парсинга
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    titles = soup.find_all('a', class_='storylink')  # Ищем заголовки новостей
    news_list = [title.text for title in titles]

    return {"news": news_list}

# Дополнительный интересный API: получить случайную шутку
@app.get("/joke")
def get_joke():
    joke_url = "https://official-joke-api.appspot.com/random_joke"
    joke_response = requests.get(joke_url).json()
    return {
        "setup": joke_response["setup"],
        "punchline": joke_response["punchline"]
    }

# Дополнительный интересный API: получить случайный факт
@app.get("/fact")
def get_fact():
    fact_url = "https://uselessfacts.jsph.pl/random.json?language=en"
    fact_response = requests.get(fact_url).json()
    return {
        "fact": fact_response["text"]
    }

# Запуск сервера с правильным портом (для Railway)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))  # Берём порт из переменной окружения или 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
