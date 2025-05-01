from pydantic import BaseModel
from datetime import datetime

class BookingSchema(BaseModel):
    book_id: int
    user_id: int

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "book_id": 1,
                "user_id": 1
            }
        }

class BookingCreate(BookingSchema):

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "book_id": 1,
                "user_id": 1
            }
        }

class BookingFinish(BookingSchema):
    pass

class BookingGetResponse(BookingSchema):
    id: int
    book_id: int
    user_id: int
    date_start: datetime | None
    date_end: datetime | None
    status: int

    class ConfigDict:
        from_attributes = True  # Включаем поддержку ORM
        json_schema_extra = {
            "example": {
                "id": 1,
                "book_id": 5,
                "user_id": 3,
                "date_start": "2023-10-05T12:00:00",
                "date_end": None,
                "status": 1
            }
        }

class BookingDeleteResponse(BaseModel):
    message: str
    deleted_id: int

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "message": "Бронирование успешно удалено",
                "deleted_id": 1
            }
        }