from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.expenses import router as expenses_router

app = FastAPI(title="Mila Expense Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

app.include_router(expenses_router, prefix="/api", tags=["expenses"])


