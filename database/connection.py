"""SQLAlchemy connection utilities with pooling and env-based credentials."""

from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_database_url() -> str:
    return os.getenv(
        "DATABASE_URL",
        "******localhost:5432/gdpr",
    )


def create_db_engine() -> Engine:
    return create_engine(get_database_url(), pool_size=5, max_overflow=10, pool_pre_ping=True)
