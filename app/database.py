from datetime import datetime
from sqlalchemy import  create_engine, Column, String, Integer, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite3"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

class Books(Base):
    __tablename__ = "books"
    book_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_title = Column(String, index=True)
    book_author = Column(String, index=True)
    book_year = Column(Integer, index=True)

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String, unique=True, index=True)
    user_full_name = Column(String)
    user_bearer_access_token = Column(String)

def init_database():
     Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()