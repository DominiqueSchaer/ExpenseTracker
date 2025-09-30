from __future__ import annotations
from datetime import date as Date
from decimal import Decimal
from sqlalchemy import String, Date as SA_Date, Enum, Numeric, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

Role = ("Mila", "MaPi")
Status = ("pending", "approved", "rejected")

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    date: Mapped[Date] = mapped_column(SA_Date, index=True)
    description: Mapped[str] = mapped_column(String(300))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))  # store as 2dp
    claimed_by: Mapped[str] = mapped_column(Enum(*Role, name="role"))
    status: Mapped[str] = mapped_column(Enum(*Status, name="status"))

Index("ix_expenses_status_claimedby_date", Expense.status, Expense.claimed_by, Expense.date.desc())
