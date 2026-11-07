import os
import psycopg2
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="DevOps Production Portal")

# Динамічно зчитуємо змінні оточення (важливо для CI/CD автоматизації)
DB_HOST = os.getenv("DB_HOST", "")  # Порожній на Fedora (Unix-сокет), '127.0.0.1' на GitHub
DB_USER = os.getenv("DB_USER", "portal_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "my_password")
DB_NAME = os.getenv("DB_NAME", "portal_db")

DB_PARAMS = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD
}

# Якщо хост вказано (середовище GitHub), використовуємо TCP/IP мережу
if DB_HOST:
    DB_PARAMS["host"] = DB_HOST
    DB_PARAMS["port"] = os.getenv("DB_PORT", "5432")

@app.on_event("startup")
def setup_database():
    """Ініціалізація бази даних при старті додатка"""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
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

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Головна сторінка з формою скорочення посилань"""
    return """
    <html>
        <head><title>Мій DevOps Портал</title></head>
        <body>
            <h1>Успіх! Вітаємо на Production-шарі проєкту!</h1>
            <p>База даних PostgreSQL успішно підключена.</p>
            <form action="/shorten" method="post">
                <input type="text" name="short_code" placeholder="Короткий код (напр. google)" required><br><br>
                <input type="url" name="long_url" placeholder="Повне посилання (https://...)" required><br><br>
                <button type="submit">Зберегти посилання</button>
            </form>
        </body>
    </html>
    """

@app.post("/shorten")
def create_short_url(short_code: str = Form(...), long_url: str = Form(...)):
    """Ендпоінт для створення короткого посилання"""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        # Записуємо дані у таблицю
        cursor.execute(
            "INSERT INTO urls (short_code, long_url) VALUES (%s, %s) ON CONFLICT (short_code) DO UPDATE SET long_url = EXCLUDED.long_url;",
            (short_code, long_url)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return HTMLResponse(content=f"<h2>Дані успішно збережено в PostgreSQL! Код: {short_code}</h2><a href='/'>Назад</a>")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка бази даних: {str(e)}")

@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    """Ендпоінт для редіректу за коротким кодом"""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        cursor.execute("SELECT long_url FROM urls WHERE short_code = %s;", (short_code,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return RedirectResponse(url=result[0])
        raise HTTPException(status_code=444, detail="Посилання не знайдено")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка редіректу: {str(e)}")
