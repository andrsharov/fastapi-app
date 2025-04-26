from fastapi import HTTPException, status, APIRouter, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db, Books, Users
from app.schemas.books import BookSchema

routers = APIRouter(prefix="/books", tags=["Книги"])
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    user = db.query(Users).filter(Users.user_bearer_access_token == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный Bearer токен авторизации",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@routers.post("/books", status_code=status.HTTP_201_CREATED)
def add_book(
        book_data: BookSchema,
        db: Session = Depends(get_db),
        current_user: Users = Depends(get_current_user)
):
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
def get_books(
        db: Session = Depends(get_db),
        current_user: Users = Depends(get_current_user)
):
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
def get_book(
        book_id: int,
        db: Session = Depends(get_db),
        current_user: Users = Depends(get_current_user)
):
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
        book_data: BookSchema,
        db: Session = Depends(get_db),
        current_user: Users = Depends(get_current_user)
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


@routers.delete("/books/{book_id}", response_model=dict)
def delete_book(
        book_id: int,
        db: Session = Depends(get_db),
        current_user: Users = Depends(get_current_user)
):
    """
    Удалить книгу по ID из базы данных
    """
    # Находим книгу в базе данных
    db_book = db.query(Books).filter(Books.book_id == book_id).first()

    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с id {book_id} не найдена"
        )

    # Удаляем книгу
    db.delete(db_book)
    db.commit()

    return {
        "message": f"Книга с id {book_id} успешно удалена",
        "deleted_book": {
            "id": db_book.book_id,
            "title": db_book.book_title,
            "author": db_book.book_author,
            "publication_year": db_book.book_year
        }
    }