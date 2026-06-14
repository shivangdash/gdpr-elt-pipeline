"""Key management and crypto-shredding demo utilities."""

from __future__ import annotations

import json
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from cryptography.fernet import Fernet


class KeyNotFoundError(KeyError):
    """Raised when a requested encryption key is unavailable."""


@dataclass
class KeyManager:
    """Simple key manager supporting RTBF via key deletion."""

    audit_log_path: str | None = None
    _keys: dict[str, bytes] = field(default_factory=dict)
    _audit_events: list[dict[str, str]] = field(default_factory=list)

    def create_key(self, subject_id: str) -> str:
        key_id = f"key_{subject_id}_{secrets.token_hex(6)}"
        self._keys[key_id] = Fernet.generate_key()
        self._log("create_key", key_id)
        return key_id

    def encrypt(self, key_id: str, plaintext: str) -> str:
        cipher = Fernet(self._lookup_key(key_id))
        payload = cipher.encrypt(plaintext.encode("utf-8")).decode("utf-8")
        self._log("encrypt", key_id)
        return payload

    def decrypt(self, key_id: str, ciphertext: str) -> str:
        cipher = Fernet(self._lookup_key(key_id))
        plaintext = cipher.decrypt(ciphertext.encode("utf-8")).decode("utf-8")
        self._log("decrypt", key_id)
        return plaintext

    def shred_key(self, key_id: str) -> None:
        if key_id in self._keys:
            del self._keys[key_id]
        self._log("shred_key", key_id)

    def list_audit_events(self) -> list[dict[str, str]]:
        return list(self._audit_events)

    def _lookup_key(self, key_id: str) -> bytes:
        key = self._keys.get(key_id)
        if key is None:
            raise KeyNotFoundError(f"Encryption key '{key_id}' is unavailable")
        return key

    def _log(self, operation: str, key_id: str) -> None:
        entry = {"operation": operation, "key_id": key_id, "timestamp": datetime.now(timezone.utc).isoformat()}
        self._audit_events.append(entry)
        if self.audit_log_path:
            path = Path(self.audit_log_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry) + "\n")
