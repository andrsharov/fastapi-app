from pydantic import BaseModel

class BookSchema(BaseModel):
    book_title: str
    book_author: str
    book_year: int

    class Config:
        json_schema_extra = {
            "example": {
                "book_title": "Название книги",
                "book_author": "Автор книги",
                "book_year": 2023
            }
        }
