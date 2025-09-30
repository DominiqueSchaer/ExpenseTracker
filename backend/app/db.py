from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# Use asyncpg + require SSL for Neon:
DATABASE_URL = (
    "postgresql+asyncpg://neondb_owner:"
    "npg_WDZ0d4mhUBPt"
    "@ep-polished-mouse-agnqozc5-pooler.c-2.eu-central-1.aws.neon.tech/neondb"
    "?ssl=require"
)

class Base(DeclarativeBase):
    pass

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with SessionLocal() as session:
        yield session
