import os
import psycopg2
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="DevOps Production Portal")

# Динамічно зчитуємо змінні з системи (зручно для CI/CD)
DB_HOST = os.getenv("DB_HOST", "")
DB_USER = os.getenv("DB_USER", "portal_user")  # за замовчуванням portal_user
DB_PASSWORD = os.getenv("DB_PASSWORD", "my_password")

DB_PARAMS = {
    "dbname": "portal_db",
    "user": DB_USER,
    "password": DB_PASSWORD
}

# Якщо ми на GitHub (де вказано хост), додаємо мережеві налаштування
if DB_HOST:
    DB_PARAMS["host"] = DB_HOST
    DB_PARAMS["port"] = "5432"

# Ця функція автоматично створює таблицю в PostgreSQL при запуску сервера
@app.on_event("startup")
def setup_database():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        # 🌟 Тільки чисте створення таблиці для збереження коротких посилань
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id SERIAL PRIMARY KEY,
                short_code VARCHAR(50) UNIQUE NOT NULL,
                long_url TEXT NOT NULL
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Успішно підключено до PostgreSQL. Таблиця 'urls' готова!")
    except Exception as e:
        print(f"❌ Помилка ініціалізації бази даних: {e}")

# 1. Головна сторінка з HTML-формою
@app.get("/", response_class=HTMLResponse)
def home():
    html_content = """
    <html>
        <head><title>DevOps URL Shortener</title></head>
        <body>
            <h2>🚀 Мій DevOps Портал (Python + PostgreSQL)</h2>
            <p>Заповніть форму, щоб зберегти посилання в базу даних:</p>
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

# 2. Ендпоінт, який записує дані в PostgreSQL
@app.post("/shorten", response_class=HTMLResponse)
def shorten_url(short_code: str = Form(...), long_url: str = Form(...)):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        # Записуємо нове посилання в таблицю
        cursor.execute(
            "INSERT INTO urls (short_code, long_url) VALUES (%s, %s);",
            (short_code, long_url)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return f"""
        <html>
            <body>
                <h3>🎉 Дані успішно збережено в PostgreSQL!</h3>
                <p>Ваше коротке посилання: <a href="http://127.0.0{short_code}">http://127.0.0{short_code}</a></p>
                <a href="/"> <- Повернутися назад</a>
            </body>
        </html>
        """
    except psycopg2.errors.UniqueViolation:
        raise HTTPException(status_code=400, detail="Цей код вже зайнятий у базі даних!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка бази даних: {e}")

# 3. Ендпоінт для редіректу (читання з PostgreSQL)
@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    # Шукаємо посилання за кодом
    cursor.execute("SELECT long_url FROM urls WHERE short_code = %s;", (short_code,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        # result повертає кортеж, наприклад ('https://google.com',), тому беремо [0]
        return RedirectResponse(url=result[0])
    raise HTTPException(status_code=404, detail="Посилання не знайдено в базі даних")
