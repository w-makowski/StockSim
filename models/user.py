from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from models.basic_base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    balance = Column(DECIMAL(12, 2), default=0.00)
    transactions = relationship("Transaction", back_populates="user")

    def __init__(self, username, password_hash, balance=0.00):
        super().__init__()
        self.username = username
        self.password_hash = password_hash
        self.balance = balance

    def __repr__(self):
        return f"<User(username={self.username}, balance={self.balance})>"
