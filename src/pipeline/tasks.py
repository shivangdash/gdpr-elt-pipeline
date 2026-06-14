"""Pipeline task utilities used by the Airflow DAG."""

from __future__ import annotations

import csv
import logging
from pathlib import Path
from random import randint

LOGGER = logging.getLogger(__name__)
DATA_DIR = Path("/tmp/gdpr_pipeline_data")


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def ingest_batch_transactions() -> str:
    _ensure_data_dir()
    path = DATA_DIR / "batch_transactions.csv"
    rows = [
        {"order_id": f"ORD-{idx}", "customer_id": f"CUS-{idx}", "amount": randint(10, 500)}
        for idx in range(1, 6)
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["order_id", "customer_id", "amount"])
        writer.writeheader()
        writer.writerows(rows)
    LOGGER.info("Batch ingestion completed: %s", path)
    return str(path)


def ingest_stream_transactions() -> str:
    _ensure_data_dir()
    path = DATA_DIR / "stream_transactions.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["event_id", "payment_id", "amount"])
        writer.writeheader()
        for idx in range(1, 6):
            writer.writerow({"event_id": f"EVT-{idx}", "payment_id": f"PAY-{idx}", "amount": randint(10, 500)})
    LOGGER.info("Streaming ingestion simulation completed: %s", path)
    return str(path)


def run_dbt_transformations() -> str:
    LOGGER.info("dbt transformations would run with: dbt run --project-dir dbt --profiles-dir dbt")
    return "dbt run simulated"
