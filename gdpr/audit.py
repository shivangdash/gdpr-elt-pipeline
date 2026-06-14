"""Audit log utility for data access and key operations."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def write_audit_event(actor: str, action: str, resource: str) -> None:
    path = Path(os.getenv("AUDIT_LOG_PATH", "./logs/audit.jsonl"))
    path.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor": actor,
        "action": action,
        "resource": resource,
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event) + "\n")
