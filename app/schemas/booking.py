"""pydantic schemas for /booking"""
from datetime import datetime
from pydantic import BaseModel

class BookingSchema(BaseModel):  # pylint: disable=too-few-public-methods
    """BookingSchema Model"""
    book_id: int
    user_id: int

    class ConfigDict:  # pylint: disable=too-few-public-methods
        """Configuration Model"""
        json_schema_extra = {
            "example": {
                "book_id": 1,
                "user_id": 1
            }
        }

class BookingCreate(BookingSchema):
    """BookingCreate Model"""# pylint: disable=too-few-public-methods

    class ConfigDict:  # pylint: disable=too-few-public-methods
        """Configuration Model"""
        json_schema_extra = {
            "example": {
                "book_id": 1,
                "user_id": 1
            }
        }

class BookingFinish(BookingSchema):  # pylint: disable=too-few-public-methods
    """BookingFinish Model"""

class BookingGetResponse(BookingSchema):  # pylint: disable=too-few-public-methods
    """BookingGetResponse Model"""
    id: int
    book_id: int
    user_id: int
    date_start: datetime | None
    date_end: datetime | None
    status: int

    class ConfigDict:  # pylint: disable=too-few-public-methods
        """Configuration Model"""
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

class BookingDeleteResponse(BaseModel):  # pylint: disable=too-few-public-methods
    """BookingDeleteResponse Model"""
    message: str
    deleted_id: int

    class ConfigDict:  # pylint: disable=too-few-public-methods
        """Configuration Model"""
        json_schema_extra = {
            "example": {
                "message": "Бронирование успешно удалено",
                "deleted_id": 1
            }
        }
