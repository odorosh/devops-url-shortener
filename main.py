import os
from fastapi import FastAPI, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# 1. Dynamiczne pobieranie zmiennych środowiskowych
DB_HOST = os.getenv("DB_HOST", "")
DB_USER = os.getenv("DB_USER", "portal_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "my_password")
DB_NAME = os.getenv("DB_NAME", "portal_db")

if DB_HOST:
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
else:
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}"

# 2. Inicjalizacja silnika i sesji SQLAlchemy
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Definicja modelu bazy danych
class URLModel(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(50), unique=True, index=True, nullable=False)
    long_url = Column(String, nullable=False)

app = FastAPI(title="DevOps Production Portal")

@app.on_event("startup")
def setup_database():
    """Automatyczne tworzenie tabel przy starcie aplikacji"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Pomyślnie połączono z PostgreSQL przez SQLAlchemy!")
    except Exception as e:
        print(f"❌ Błąd inicjalizacji bazy danych: {e}")

# 🌟 Najważniejsza zmiana DevOps: Bezpieczne zarządzanie sesjami bazy danych (Dependency Injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head><title>Мій DevOps Портал</title></head>
        <body>
            <h1>Успіх! Вітаємо на Production-шарі проєкту!</h1>
            <p>База даних PostgreSQL працює через SQLAlchemy i Dependency Injection.</p>
            <form action="/shorten" method="post">
                <input type="text" name="short_code" placeholder="Короткий код (напр. google)" required><br><br>
                <input type="url" name="long_url" placeholder="Повне посилання (https://...)" required><br><br>
                <button type="submit">Зберегти посилання</button>
            </form>
        </body>
    </html>
    """

@app.post("/shorten")
def create_short_url(short_code: str = Form(...), long_url: str = Form(...), db: Session = Depends(get_db)):
    try:
        existing = db.query(URLModel).filter(URLModel.short_code == short_code).first()
        if existing:
            existing.long_url = long_url
        else:
            new_url = URLModel(short_code=short_code, long_url=long_url)
            db.add(new_url)
        db.commit()
        return HTMLResponse(content=f"<h2>Дані успішно збережено в PostgreSQL! Код: {short_code}</h2><a href='/'>Назад</a>")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Błąd bazy danych: {str(e)}")

@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    try:
        result = db.query(URLModel).filter(URLModel.short_code == short_code).first()
        if result:
            return RedirectResponse(url=result.long_url)
        raise HTTPException(status_code=444, detail="Посилання не знайдено")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd przekierowania: {str(e)}")
