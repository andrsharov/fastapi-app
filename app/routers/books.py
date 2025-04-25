from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from app.database import get_db, Books
from app.schemas.books import BookCreate

routers = APIRouter(prefix="/books", tags=["Книги"])

# books = []
# current_id = 1

@routers.post("/books", status_code=status.HTTP_201_CREATED)
def add_book(book_data: BookCreate):
    global current_id
    new_book = Book(**book_data.dict(), id=current_id)
    books.append(new_book)
    current_id += 1
    return {
        "message": "Книга успешно добавлена",
        "book": new_book
    }

@routers.get("/books", response_model=dict)
def get_books(db: Session = Depends(get_db)):
    """
    Get all books from the database (synchronous version)
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
