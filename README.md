# GDPR-Compliant ELT Data Pipeline

This repository provides a reference implementation of a GDPR-oriented ELT stack using:
- **Apache Airflow** for orchestration
- **dbt** for staged transformations
- **PostgreSQL** for source/serving storage
- **Python utilities** for PII masking and crypto-shredding
- **Docker Compose** for local development

## Project Structure

- `/dags` - Airflow DAGs for batch + streaming ingestion orchestration
- `/src/pipeline` - ingestion task implementations and dbt run hook
- `/dbt` - dbt project (`staging`, `intermediate`, `marts`) with model tests/docs
- `/pii_masking` - hashing + tokenization masking utilities
- `/crypto_shredding` - key lifecycle management and RTBF crypto-shredding
- `/database` - PostgreSQL schema, SQLAlchemy connection utility, mock data seed
- `/gdpr` - lineage, audit, retention, and consent integration helpers
- `/tests` - focused unit tests for masking and key shredding behavior

## GDPR Controls Implemented

### 1) Pipeline Orchestration
- `dags/gdpr_elt_pipeline.py` defines scheduled orchestration, retries, and dependency flow.
- `src/pipeline/tasks.py` includes batch and streaming mock transaction ingestion.

### 2) Transformation Layer (dbt)
- Staging model: `dbt/models/staging/stg_customer_data.sql`
- Intermediate model: `dbt/models/intermediate/int_customer_orders.sql`
- Mart model: `dbt/models/marts/fct_gdpr_orders.sql`
- Tests/docs: `dbt/models/schema.yml`

### 3) PII Masking & Anonymization
- PII fields covered: `name`, `email`, `phone`, `ssn`, `address`
- **Staging** uses tokenization (reversible pseudonymization)
- **Production** uses salted SHA-256 hashing (irreversible anonymization)
- Implemented in `pii_masking/masker.py`

### 4) Crypto-Shredding / RTBF
- `crypto_shredding/key_manager.py` provides key create/encrypt/decrypt/shred operations.
- RTBF is enforced by deleting key material (`shred_key`) so encrypted data becomes unreadable.
- All key operations produce audit entries.

### 5) Database Support
- PostgreSQL schema in `database/schema.sql`
- SQLAlchemy pooled connection in `database/connection.py`
- Mock data generation in `database/seed_mock_data.py`

### 6) Compliance Features
- **Data lineage** logging: `gdpr/lineage.py`
- **Audit logs**: `gdpr/audit.py` and key-manager audit trail
- **Retention policy helper**: `gdpr/retention.py`
- **Consent integration point**: `gdpr/consent.py`

## Local Development

1. Copy env defaults if needed:
   ```bash
   cp .env.example .env
   ```
2. Start services:
   ```bash
   docker compose up --build
   ```
3. Run tests:
   ```bash
   python -m unittest discover -s tests -v
   ```

## Notes

- This is a functional demo scaffold intended for extension in production environments.
- Integrate enterprise KMS/HSM and persistent token vaults for production-hardening.
