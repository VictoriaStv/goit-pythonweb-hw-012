from sqlalchemy import Column, Integer, String, Boolean
from src.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255), nullable=False)
    confirmed = Column(Boolean, default=False)
    avatar = Column(String, nullable=True)
    role = Column(String, default="user") 
