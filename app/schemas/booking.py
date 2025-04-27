from pydantic import BaseModel
from datetime import datetime

class BookingSchema(BaseModel):
    book_id: int
    user_id: int

    class Config:
        schema_extra = {
            "example": {
                "book_id": "ID Книги",
                "user_id": "ID Пользователя"
            }
        }

class BookingCreate(BookingSchema):
    pass

class BookingFinish(BookingSchema):
    pass