from pydantic import BaseModel

class UserSchema(BaseModel):
    user_name: str
    user_full_name: str
    user_jwt_access_token: int

    class Config:
        schema_extra = {
            "example": {
                "user_name": "Имя пользователя (Логин)",
                "user_full_name": "Полное имя пользователя (ФИО)",
                "user_jwt_access_token": "JWT токен"
            }
        }
