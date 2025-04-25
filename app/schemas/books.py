from pydantic import BaseModel

class BookSchema(BaseModel):
    book_title: str
    book_author: str
    book_year: int

class BookCreate(BaseModel):
    title: str
    author: str
    year: int

class Book(BookCreate):
    id: int