from typing import List, Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

Status = Literal["pending", "approved", "reimbursed"]

class ExpenseIn(BaseModel):
    date: str
    description: str
    amount: float

class ExpenseOut(ExpenseIn):
    id: str
    status: Status
    submittedBy: Literal["Mila"] = "Mila"

# Temporary in-memory store for local dev
_DB: List[ExpenseOut] = [
    ExpenseOut(id="1", date="2025-09-23", description="School supplies", amount=18.5, status="pending"),
    ExpenseOut(id="2", date="2025-09-22", description="Bus ticket", amount=3.2, status="approved"),
]

@router.get("/expenses", response_model=List[ExpenseOut])
async def list_expenses() -> List[ExpenseOut]:
    return _DB

@router.post("/expenses", response_model=ExpenseOut)
async def add_expense(body: ExpenseIn) -> ExpenseOut:
    new = ExpenseOut(
        id=str(len(_DB) + 1),
        date=body.date,
        description=body.description,
        amount=body.amount,
        status="pending",
    )
    _DB.append(new)
    return new

@router.post("/expenses/{expense_id}/approve", response_model=ExpenseOut)
async def approve_expense(expense_id: str) -> ExpenseOut:
    for e in _DB:
        if e.id == expense_id:
            e.status = "approved"  # type: ignore
            return e
    raise HTTPException(status_code=404, detail="Not found")

class ReimburseIn(BaseModel):
    amount: float

class ReimburseOut(BaseModel):
    remaining: float

@router.post("/reimburse", response_model=ReimburseOut)
async def reimburse(_: ReimburseIn) -> ReimburseOut:
    total = sum(e.amount for e in _DB)
    # For demo, do nothing but return current total
    return ReimburseOut(remaining=total)


