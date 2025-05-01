from fastapi import status, APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db, Users
from app.schemas.users import UserSchema

routers = APIRouter(prefix="/users", tags=["Пользователи"])

@routers.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
def add_user(user_data: UserSchema, db: Session = Depends(get_db)):
    """
    Добавить нового пользователя в базу данных
    """
    # Создаем объект модели SQLAlchemy
    new_user = Users(
        user_name=user_data.user_name,
        user_full_name=user_data.user_full_name,
        user_bearer_access_token=user_data.user_bearer_access_token
    )

    # Добавляем в сессию и сохраняем
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Обновляем объект для получения сгенерированного ID

    return {
        "message": "Пользователь успешно добавлен",
        "book": {
            "user_id": new_user.user_id,
            "user_name": new_user.user_name,
            "user_full_name": new_user.user_full_name,
            "user_bearer_access_token": new_user.user_bearer_access_token
        }
    }