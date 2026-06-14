"""Retention policy helpers for data minimization controls."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone


def cutoff_timestamp(days: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days)
