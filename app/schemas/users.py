from pydantic import BaseModel

class UserSchema(BaseModel):
    user_name: str
    user_full_name: str
    user_bearer_access_token: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_name": "Имя пользователя (Логин)",
                "user_full_name": "Полное имя пользователя (ФИО)",
                "user_bearer_access_token": "Bearer токен"
            }
        }
