"""pydantic schemas for /users"""
from pydantic import BaseModel

class UserSchema(BaseModel):  # pylint: disable=too-few-public-methods
    """UserSchema Model"""
    user_name: str
    user_full_name: str
    user_bearer_access_token: str

    class ConfigDict:  # pylint: disable=too-few-public-methods
        """Configuration Model"""
        json_schema_extra = {
            "example": {
                "user_name": "Имя пользователя (Логин)",
                "user_full_name": "Полное имя пользователя (ФИО)",
                "user_bearer_access_token": "Bearer токен"
            }
        }
