# migrations/env.py
from __future__ import annotations

import os
import sys
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

# ---- Windows fix for psycopg async only ----
# Safe to keep even if you use asyncpg; it's a no-op elsewhere.
if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass
# --------------------------------------------

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# App-specific imports
from settings import settings           # loads .env
from app.db import Base                     # your Declarative Base
import app.models as models                           # ensure metadata is populated

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = os.getenv("ALEMBIC_DATABASE_URL", settings.DATABASE_URL)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    """Run migrations with a sync connection (Alembic expects this)."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' (async) mode."""
    url = os.getenv("ALEMBIC_DATABASE_URL", settings.DATABASE_URL)
    connectable: AsyncEngine = create_async_engine(url, poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
