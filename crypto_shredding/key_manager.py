"""Key management and crypto-shredding demo utilities."""

from __future__ import annotations

import base64
import hashlib
import json
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


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
        self._keys[key_id] = secrets.token_bytes(32)
        self._log("create_key", key_id)
        return key_id

    def encrypt(self, key_id: str, plaintext: str) -> str:
        key = self._lookup_key(key_id)
        encrypted = _xor_with_keystream(plaintext.encode("utf-8"), key)
        payload = base64.urlsafe_b64encode(encrypted).decode("utf-8")
        self._log("encrypt", key_id)
        return payload

    def decrypt(self, key_id: str, ciphertext: str) -> str:
        key = self._lookup_key(key_id)
        decoded = base64.urlsafe_b64decode(ciphertext.encode("utf-8"))
        plaintext = _xor_with_keystream(decoded, key).decode("utf-8")
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


def _xor_with_keystream(data: bytes, key: bytes) -> bytes:
    stream = hashlib.sha256(key).digest()
    return bytes([byte ^ stream[idx % len(stream)] for idx, byte in enumerate(data)])
