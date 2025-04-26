from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from app.database import get_db, Books
from app.schemas.books import BookCreate

routers = APIRouter(prefix="/books", tags=["Книги"])

@routers.post("/books", status_code=status.HTTP_201_CREATED)
def add_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """
    Добавить новую книгу в базу данных
    """
    # Создаем объект модели SQLAlchemy
    new_book = Books(
        book_title=book_data.book_title,
        book_author=book_data.book_author,
        book_year=book_data.book_year
    )

    # Добавляем в сессию и сохраняем
    db.add(new_book)
    db.commit()
    db.refresh(new_book)  # Обновляем объект для получения сгенерированного ID

    return {
        "message": "Книга успешно добавлена",
        "book": {
            "id": new_book.book_id,
            "title": new_book.book_title,
            "author": new_book.book_author,
            "publication_year": new_book.book_year
        }
    }

@routers.get("/books", response_model=dict)
def get_books(db: Session = Depends(get_db)):
    """
    Получаем список всех книг из базы данных
    """
    books = db.query(Books).all()

    return {
        "books": [
            {
                "id": book.book_id,
                "title": book.book_title,
                "author": book.book_author,
                "publication_year": book.book_year
            }
            for book in books
        ]
    }

@routers.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Книга с id {book_id} не найдена"
    )

@routers.put("/books/{book_id}")
async def update_book(book_id: int, book_data: BookCreate):
    for i, book in enumerate(books):
        if book.id == book_id:
            updated_book = Book(**book_data.dict(), id=book_id)
            books[i] = updated_book
            return {
                "message": "Книга успешно обновлена",
                "book": updated_book
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Книга с id {book_id} не найдена"
    )
