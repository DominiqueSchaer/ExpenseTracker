from __future__ import annotations
from typing import List, Literal, Optional
from uuid import uuid4
from decimal import Decimal, ROUND_HALF_UP
from datetime import date as Date
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, field_validator

router = APIRouter()

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

# Temporary in-memory store
_DB: List[ExpenseOut] = [
    ExpenseOut(
        id="1",
        date=Date.fromisoformat("2025-09-23"),
        description="School supplies",
        amount=Decimal("18.50"),
        claimed_by="Mila",
        status="pending",
    ),
    ExpenseOut(
        id="2",
        date=Date.fromisoformat("2025-09-22"),
        description="Bus ticket",
        amount=Decimal("3.20"),
        claimed_by="MaPi",
        status="approved",
    ),
]

def _find(expense_id: str) -> ExpenseOut:
    for e in _DB:
        if e.id == expense_id:
            return e
    raise HTTPException(status_code=404, detail="Not found")

@router.get("/expenses", response_model=List[ExpenseOut])
async def list_expenses(
    status: Optional[Status] = Query(default=None),
    claimed_by: Optional[Role] = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> List[ExpenseOut]:
    items = _DB
    if status:
        items = [e for e in items if e.status == status]
    if claimed_by:
        items = [e for e in items if e.claimed_by == claimed_by]
    items = sorted(items, key=lambda e: (e.date, e.id), reverse=True)
    return items[offset: offset + limit]

@router.post("/expenses", response_model=ExpenseOut)
async def add_expense(body: ExpenseIn) -> ExpenseOut:
    new = ExpenseOut(
        id=str(uuid4()),
        date=body.date,
        description=body.description.strip(),
        amount=chf(body.amount),
        claimed_by=body.claimed_by,
        status="approved" if body.claimed_by == "MaPi" else "pending",
    )
    _DB.append(new)
    return new

@router.post("/expenses/{expense_id}/approve", response_model=ExpenseOut)
async def approve_expense(expense_id: str) -> ExpenseOut:
    e = _find(expense_id)
    if e.claimed_by != "Mila":
        raise HTTPException(status_code=400, detail="Only Mila's claims require approval.")
    if e.status != "pending":
        raise HTTPException(status_code=409, detail=f"Cannot approve from state {e.status}.")
    e.status = "approved"  # type: ignore
    return e

@router.post("/expenses/{expense_id}/reject", response_model=ExpenseOut)
async def reject_expense(expense_id: str) -> ExpenseOut:
    e = _find(expense_id)
    if e.claimed_by != "Mila":
        raise HTTPException(status_code=400, detail="Only Mila's claims can be rejected.")
    if e.status != "pending":
        raise HTTPException(status_code=409, detail=f"Cannot reject from state {e.status}.")
    e.status = "rejected"  # type: ignore
    return e

class SummaryOut(BaseModel):
    currency: Literal["CHF"] = "CHF"
    approved_total_mapi_claims: Decimal
    approved_total_mila_claims: Decimal
    net_balance_for_mila: Decimal  # >0 => Mila owes MaPi

@router.get("/summary", response_model=SummaryOut)
async def summary() -> SummaryOut:
    mapi_approved = sum((e.amount for e in _DB if e.claimed_by == "MaPi" and e.status == "approved"), Decimal("0"))
    mila_approved = sum((e.amount for e in _DB if e.claimed_by == "Mila" and e.status == "approved"), Decimal("0"))
    mapi_approved = chf(mapi_approved)
    mila_approved = chf(mila_approved)
    net_for_mila = chf(mapi_approved - mila_approved)
    return SummaryOut(
        approved_total_mapi_claims=mapi_approved,
        approved_total_mila_claims=mila_approved,
        net_balance_for_mila=net_for_mila,
    )
