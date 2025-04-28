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

# Маршрут для парсинга новостей по категории
@app.get("/parse")
def parse_news(category: str):
    # Базовый URL для BBC News
    base_url = "https://www.bbc.com/news"
    
    # Словарь категорий
    categories = {
        "world": "/world",
        "technology": "/technology",
        "business": "/business",
        "science": "/science",
        "health": "/health",
    }

    # Проверяем, если категория существует
    if category not in categories:
        return {"error": "Invalid category. Available categories: world, technology, business, science, health."}

    # Формируем URL для парсинга
    url = base_url + categories[category]
    
    # Запрашиваем страницу
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": f"Failed to retrieve news. Status code: {response.status_code}"}

    # Парсим HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем все заголовки новостей
    titles = soup.find_all('h3')
    
    # Собираем заголовки в список
    news_list = [title.get_text(strip=True) for title in titles]

    # Возвращаем список новостей
    return {"category": category, "news": news_list}

# Запуск сервера с правильным портом
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))  # Берём порт из переменной окружения или 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
