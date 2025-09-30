from __future__ import annotations
from typing import Literal, Optional
from datetime import date as Date
from decimal import Decimal, ROUND_HALF_UP
from pydantic import BaseModel, field_validator

Role = Literal["Mila", "MaPi"]
Status = Literal["pending", "approved", "rejected"]

def chf(amount: Decimal) -> Decimal:
    # Banker's rounding can be confusing; use HALF_UP for family finance
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

class ExpenseIn(BaseModel):
    date: Date
    description: str
    amount: Decimal
    claimed_by: Role

    @field_validator("amount")
    @classmethod
    def positive_amount(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("amount must be > 0")
        return chf(v)

class ExpenseOut(ExpenseIn):
    id: str
    status: Status

class SummaryOut(BaseModel):
    currency: Literal["CHF"] = "CHF"
    approved_total_mapi_claims: Decimal
    approved_total_mila_claims: Decimal
    net_balance_for_mila: Decimal  # >0 => Mila owes MaPi
    pending_total_mila_claims: Decimal
    pending_count_mila_claims: Optional[int] = None
