from __future__ import annotations
from typing import List, Optional, Literal
from uuid import uuid4
from decimal import Decimal
from datetime import date as Date
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import select, func, desc, case, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Expense
from app.schemas import ExpenseIn, ExpenseOut, SummaryOut, chf

router = APIRouter()

Role = Literal["Mila", "MaPi"]
Status = Literal["pending", "approved", "rejected"]

def to_out(e: Expense) -> ExpenseOut:
    return ExpenseOut(
        id=e.id, date=e.date, description=e.description,
        amount=Decimal(e.amount), claimed_by=e.claimed_by, status=e.status
    )

@router.get("/expenses", response_model=List[ExpenseOut])
async def list_expenses(
    status: Optional[Status] = Query(default=None),
    claimed_by: Optional[Role] = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> List[ExpenseOut]:
    stmt = select(Expense)
    if status:
        stmt = stmt.where(Expense.status == status)
    if claimed_by:
        stmt = stmt.where(Expense.claimed_by == claimed_by)
    stmt = stmt.order_by(desc(Expense.date), desc(Expense.id)).offset(offset).limit(limit)
    rows = (await db.execute(stmt)).scalars().all()
    return [to_out(e) for e in rows]

@router.post("/expenses", response_model=ExpenseOut)
async def add_expense(body: ExpenseIn, db: AsyncSession = Depends(get_db)) -> ExpenseOut:
    new = Expense(
        id=str(uuid4()),
        date=body.date,
        description=body.description.strip(),
        amount=body.amount,  # validated & rounded by pydantic validator + chf
        claimed_by=body.claimed_by,
        status="approved" if body.claimed_by == "MaPi" else "pending",
    )
    db.add(new)
    await db.commit()
    await db.refresh(new)
    return to_out(new)

async def _get_or_404(db: AsyncSession, expense_id: str) -> Expense:
    e = await db.get(Expense, expense_id)
    if not e:
        raise HTTPException(status_code=404, detail="Not found")
    return e

@router.post("/expenses/{expense_id}/approve", response_model=ExpenseOut)
async def approve_expense(expense_id: str, db: AsyncSession = Depends(get_db)) -> ExpenseOut:
    e = await _get_or_404(db, expense_id)
    if e.claimed_by != "Mila":
        raise HTTPException(status_code=400, detail="Only Mila's claims require approval.")
    if e.status != "pending":
        raise HTTPException(status_code=409, detail=f"Cannot approve from state {e.status}.")
    e.status = "approved"
    await db.commit()
    await db.refresh(e)
    return to_out(e)

@router.post("/expenses/{expense_id}/reject", response_model=ExpenseOut)
async def reject_expense(expense_id: str, db: AsyncSession = Depends(get_db)) -> ExpenseOut:
    e = await _get_or_404(db, expense_id)
    if e.claimed_by != "Mila":
        raise HTTPException(status_code=400, detail="Only Mila's claims can be rejected.")
    if e.status != "pending":
        raise HTTPException(status_code=409, detail=f"Cannot reject from state {e.status}.")
    e.status = "rejected"
    await db.commit()
    await db.refresh(e)
    return to_out(e)

@router.get("/summary", response_model=SummaryOut)
async def summary(db: AsyncSession = Depends(get_db)) -> SummaryOut:
    q = select(
        func.coalesce(
            func.sum(case((Expense.claimed_by == "MaPi", Expense.amount), else_=0)), 0
        ),
        func.coalesce(
            func.sum(case((and_(Expense.claimed_by == "Mila", Expense.status == "approved"), Expense.amount), else_=0)), 0
        ),
        func.coalesce(
            func.sum(case((and_(Expense.claimed_by == "Mila", Expense.status == "pending"), Expense.amount), else_=0)), 0
        ),
        func.coalesce(
            func.sum(case((and_(Expense.claimed_by == "Mila", Expense.status == "pending"), 1), else_=0)), 0
        ),
    )

    mapi_approved, mila_approved, mila_pending, mila_pending_count = (await db.execute(q)).one()

    mapi_approved = chf(Decimal(mapi_approved))
    mila_approved = chf(Decimal(mila_approved))
    mila_pending  = chf(Decimal(mila_pending))
    net_for_mila  = chf(mapi_approved - mila_approved)

    return SummaryOut(
        approved_total_mapi_claims=mapi_approved,
        approved_total_mila_claims=mila_approved,
        net_balance_for_mila=net_for_mila,
        pending_total_mila_claims=mila_pending,
        pending_count_mila_claims=int(mila_pending_count),
    )
