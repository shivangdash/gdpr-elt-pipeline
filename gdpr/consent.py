"""Consent tracking integration points."""

from __future__ import annotations


def requires_consent(consent_type: str) -> bool:
    return consent_type in {"marketing_email", "profiling", "third_party_sharing"}
