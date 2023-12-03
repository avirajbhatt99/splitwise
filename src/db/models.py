import enum
from datetime import datetime
from sqlalchemy import Column, String, BigInteger, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from .postgre import Base
from uuid import uuid4
from sqlalchemy import Enum


class User(Base):
    """
    users table class
    """

    __tablename__ = "users"

    id = Column(String, primary_key=True, default=uuid4().hex)
    name = Column(String)
    email = Column(String)
    mobile_number = Column(BigInteger)


class ExpenseType(enum.Enum):
    """
    expense type enum
    """

    EQUAL = "equal"
    EXACT = "exact"
    PERCENT = "percent"


class Expense(Base):
    """
    expenses table class
    """

    __tablename__ = "expenses"

    id = Column(String, primary_key=True)
    name = Column(String)
    date = Column(DateTime(timezone=True), default=datetime.now())
    amount = Column(Float)
    payer_id = Column(String, ForeignKey("users.id"))
    expense_type = Column(Enum(ExpenseType))
    payer = relationship("User")


class Passbook(Base):
    """
    passbook table class
    """

    __tablename__ = "passbook"

    id = Column(String, primary_key=True)
    expense_id = Column(String, ForeignKey("expenses.id"))
    user_id = Column(String, ForeignKey("users.id"))
    amount_owes = Column(Float)
    expense = relationship("Expense")
    user = relationship("User")
