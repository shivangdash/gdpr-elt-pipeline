"""Utilities for GDPR-safe PII masking and tokenization."""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone

PII_FIELDS = {"name", "email", "phone", "ssn", "address"}


def hash_value(value: str, salt: str | None = None) -> str:
    if value is None:
        return ""
    resolved_salt = salt if salt is not None else os.getenv("PII_HASH_SALT", "default-salt")
    digest = hashlib.sha256(f"{resolved_salt}:{value}".encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


@dataclass
class TokenVault:
    """In-memory token vault for reversible pseudonymization demos."""

    token_to_value: dict[str, str] = field(default_factory=dict)
    audit_log: list[dict[str, str]] = field(default_factory=list)

    def tokenize(self, value: str) -> str:
        token = f"tok_{secrets.token_hex(8)}"
        self.token_to_value[token] = value
        self.audit_log.append({"operation": "tokenize", "token": token, "timestamp": _utc_now()})
        return token

    def detokenize(self, token: str) -> str:
        self.audit_log.append({"operation": "detokenize", "token": token, "timestamp": _utc_now()})
        return self.token_to_value[token]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def mask_record(record: dict[str, str], environment: str, vault: TokenVault | None = None) -> dict[str, str]:
    """Mask PII for staging/prod environments.

    - staging: tokenization (reversible pseudonymization)
    - production: salted hashing (irreversible anonymization)
    """

    masked = dict(record)
    token_vault = vault or TokenVault()

    for field in PII_FIELDS:
        if field not in masked or masked[field] in (None, ""):
            continue
        value = str(masked[field])

        if environment.lower() == "production":
            masked[field] = hash_value(value)
        else:
            masked[field] = token_vault.tokenize(value)

    masked["masking_environment"] = environment
    return masked


def safe_compare(left: str, right: str) -> bool:
    return hmac.compare_digest(left, right)
