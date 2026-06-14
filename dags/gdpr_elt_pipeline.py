"""Airflow DAG for GDPR-compliant ELT ingestion and transformation."""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.pipeline.tasks import ingest_batch_transactions, ingest_stream_transactions, run_dbt_transformations

DEFAULT_ARGS = {
    "owner": "data-platform",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="gdpr_elt_pipeline",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2025, 1, 1),
    schedule="*/15 * * * *",
    catchup=False,
    tags=["gdpr", "elt"],
) as dag:
    batch_ingest = PythonOperator(task_id="ingest_batch_transactions", python_callable=ingest_batch_transactions)
    stream_ingest = PythonOperator(task_id="ingest_stream_transactions", python_callable=ingest_stream_transactions)
    dbt_run = PythonOperator(task_id="run_dbt_transformations", python_callable=run_dbt_transformations)

    [batch_ingest, stream_ingest] >> dbt_run
