from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# Наша тимчасова база даних у пам'яті
db_links = {
    "fedora": "https://getfedora.org"
}

# 1. Головна сторінка з чистою HTML-формою (ЖОДНОГО JavaScript!)
@app.get("/", response_class=HTMLResponse)
def home():
    html_content = """
    <html>
        <head><title>DevOps URL Shortener</title></head>
        <body>
            <h2>🚀 Мій DevOps Портал (Pure Python & HTML)</h2>
            <p>Заповніть форму, щоб створити коротке посилання:</p>

            <!-- Класична форма HTML. При натисканні кнопки вона сама відправить POST-запит -->
            <form action="/shorten" method="post">
                <label>Короткий код:</label><br>
                <input type="text" name="short_code" placeholder="Наприклад: google" required><br><br>

                <label>Повне посилання:</label><br>
                <input type="url" name="long_url" placeholder="https://..." required><br><br>

                <button type="submit">Скоротити посилання</button>
            </form>
        </body>
    </html>
    """
    return html_content

# 2. Функція приймає дані з форми
@app.post("/shorten", response_class=HTMLResponse)
def shorten_url(short_code: str = Form(...), long_url: str = Form(...)):
    db_links[short_code] = long_url

    # Повертаємо сторінку з результатом
    return f"""
    <html>
        <body>
            <h3>🎉 Готово!</h3>
            <p>Ваше коротке посилання: <a href="http://127.0.0{short_code}">http://127.0.0{short_code}</a></p>
            <a href="/"> <- Повернутися назад</a>
        </body>
    </html>
    """

# 3. Функція редіректу
@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    if short_code in db_links:
        return RedirectResponse(url=db_links[short_code])
    raise HTTPException(status_code=404, detail="Посилання не знайдено")
