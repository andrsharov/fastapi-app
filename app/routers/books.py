from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
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

@routers.get("/books/{book_id}", response_model=dict)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Получить книгу по ID из базы данных
    """
    # Ищем книгу в базе данных
    book = db.query(Books).filter(Books.book_id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с id {book_id} не найдена"
        )

    return {
        "id": book.book_id,
        "title": book.book_title,
        "author": book.book_author,
        "publication_year": book.book_year
    }

@routers.put("/books/{book_id}", response_model=dict)
def update_book(
        book_id: int,
        book_data: BookCreate,
        db: Session = Depends(get_db)
):
    """
    Обновить данные книги по ID
    """
    # Находим книгу в базе данных
    db_book = db.query(Books).filter(Books.book_id == book_id).first()

    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с id {book_id} не найдена"
        )

    # Обновляем поля
    db_book.book_title = book_data.book_title
    db_book.book_author = book_data.book_author
    db_book.book_year = book_data.book_year

    # Сохраняем изменения
    db.commit()
    db.refresh(db_book)

    return {
        "message": "Книга успешно обновлена",
        "book": {
            "id": db_book.book_id,
            "title": db_book.book_title,
            "author": db_book.book_author,
            "publication_year": db_book.book_year
        }
    }