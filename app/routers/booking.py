from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timezone
from app.database import get_db, Booking, Books, Users
from app.schemas.booking import BookingCreate, BookingFinish, BookingGetResponse
from app.auth.auth_handler import get_current_user

routers = APIRouter(prefix="/booking", tags=["Бронирование"])


@routers.post("/issue", status_code=status.HTTP_201_CREATED, response_model=BookingCreate)
def issue_book(
        booking_data: BookingCreate,
        db: Session = Depends(get_db),
        current_user: Users = Depends(get_current_user)
):
    # Проверка существования книги
    book = db.query(Books).filter(Books.book_id == booking_data.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена в каталоге"
        )

    # Проверка активной брони
    active_booking = db.query(Booking).filter(
        Booking.book_id == booking_data.book_id,
        Booking.status == 1
    ).first()

    if active_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Книга уже выдана другому пользователю"
        )

    # Создание записи о выдаче
    new_booking = Booking(
        book_id=booking_data.book_id,
        user_id=current_user.user_id,
        date_start=datetime.now(timezone.utc),
        status=1
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking

@routers.put("/return/{booking_id}", response_model=BookingFinish)
def return_book(
        booking_id: int,
        db: Session = Depends(get_db),
        current_user: Users = Depends(get_current_user)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.user_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись о бронировании не найдена"
        )

    if booking.status == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Книга уже была возвращена ранее"
        )

    # Обновление данных
    booking.date_end = datetime.now(timezone.utc)
    booking.status = 0

    db.commit()
    db.refresh(booking)

    return booking


@routers.get("/get/{booking_id}", response_model=BookingGetResponse)
def get_booking(
        booking_id: int,
        db: Session = Depends(get_db),
        current_user: Users = Depends(get_current_user)
):
    """
    Получить данные бронирования по ID
    """
    # Ищем бронирование
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.user_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бронирование не найдено"
        )

    return booking