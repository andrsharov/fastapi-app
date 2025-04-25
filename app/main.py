from fastapi import FastAPI
from app.routers import (books)
from app.database import init_database

#Инициализируем базу данных
init_database()
#Создаю объект приложения
app = FastAPI(
    title="Система управления каталогом книг",
    description="Простейшая система каталогом книг, основанная на "
                "фреймворке FastAPI.",
    version="0.0.1",
    contact={
        "name": "Andrei Sharov",
        "url": "https://github.com/andrsharov/fastapi-app",
        "email": "andrsharov@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

app.include_router(books.routers)
