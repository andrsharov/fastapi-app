from pydantic import BaseModel

books = []
current_id = 1

class BookCreate(BaseModel):
    title: str
    author: str
    year: int

class Book(BookCreate):
    id: int