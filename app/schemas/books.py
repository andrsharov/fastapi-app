"""pydantic schemas for /books"""
from pydantic import BaseModel

class BookSchema(BaseModel):  # pylint: disable=too-few-public-methods
    """BookSchema Model"""
    book_title: str
    book_author: str
    book_year: int

    class ConfigDict:  # pylint: disable=too-few-public-methods
        """Configuration Model"""
        json_schema_extra = {
            "example": {
                "book_title": "Название книги",
                "book_author": "Автор книги",
                "book_year": 2023
            }
        }
