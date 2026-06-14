"""Data lineage tracker for GDPR processing visibility."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class LineageTracker:
    output_path: str = os.getenv("LINEAGE_LOG_PATH", "./logs/lineage.jsonl")

    def record(self, source: str, target: str, operation: str) -> None:
        path = Path(self.output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": source,
            "target": target,
            "operation": operation,
        }
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event) + "\n")
