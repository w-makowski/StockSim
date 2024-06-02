from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from models.basic_base import Base
from datetime import datetime
import enum


class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    symbol = Column(String, unique=True, nullable=False)
    prev_day_close_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    current_volume = Column(Integer, nullable=False)
    current_datetime = Column(DateTime, default=datetime.utcnow(), nullable=False)
    transactions = relationship("Transaction", back_populates="stock")

    def __init__(self, name, symbol, prev_day_close_price, current_price, current_volume, current_datatime):
        super().__init__()
        self.name = name
        self.symbol = symbol
        self.prev_day_close_price = prev_day_close_price
        self.current_price = current_price
        self.current_volume = current_volume
        self.current_datatime = current_datatime

    def __repr__(self):
        return (f"<Stock(name={self.name}, symbol={self.symbol}, prev_day_close_price={self.prev_day_close_price}, "
                f"current_price={self.current_price}, volume={self.current_volume})>")


class TransactionType(enum.Enum):
    BUY = 'buy'
    SELL = 'sell'


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    stock_id = Column(Integer, ForeignKey('stock.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    transaction_datetime = Column(DateTime, default=datetime.utcnow(), nullable=False)
    user = relationship("User", back_populates="transactions")
    stock = relationship("Stock", back_populates="transactions")

    def __init__(self, user_id, stock_id, amount, price, transaction_type, transaction_datetime):
        super().__init__()
        self.user_id = user_id
        self.stock_id = stock_id
        self.amount = amount
        self.price = price
        self.transaction_type = transaction_type
        self.transaction_datetime = transaction_datetime

    def __repr__(self):
        return (f"<Transaction(user_id={self.user_id}, stock_id={self.stock_id}, amount={self.amount}, "
                f"price={self.price}, type={self.transaction_type}, datetime={self.transaction_datetime})>")

