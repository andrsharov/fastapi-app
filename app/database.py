"""Database settings"""
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite3"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

class Books(Base):  # pylint: disable=too-few-public-methods
    """Table books"""
    __tablename__ = "books"
    book_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_title = Column(String, index=True)
    book_author = Column(String, index=True)
    book_year = Column(Integer, index=True)

class Users(Base):  # pylint: disable=too-few-public-methods
    """Table users"""
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String, unique=True, index=True)
    user_full_name = Column(String)
    user_bearer_access_token = Column(String)

class Booking(Base):  # pylint: disable=too-few-public-methods
    """Table booking"""
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.book_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    date_start = Column(DateTime(timezone=True), nullable=True)
    date_end = Column(DateTime(timezone=True), nullable=True)
    status = Column(Integer, nullable=False)

def init_database():
    """Init database if not exists"""
    Base.metadata.create_all(engine)

def get_db():
    """Connect to database"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
