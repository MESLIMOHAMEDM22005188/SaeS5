"""Reusable verification-code primitives."""
from datetime import timedelta
import secrets

from django.utils import timezone

CODE_TTL = timedelta(minutes=10)


def generate_verification_code():
    """Return a cryptographically random six-digit verification code."""
    return f"{secrets.randbelow(900_000) + 100_000}"


def verification_expiration():
    """Return the expiration timestamp for a newly generated code."""
    return timezone.now() + CODE_TTL
