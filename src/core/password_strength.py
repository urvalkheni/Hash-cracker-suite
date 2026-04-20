"""
Password Strength Analyzer Module

Provides a simple, educational password strength analysis that balances
readability and practical feedback.

This is a simplified educational estimator and not a real-world
password audit tool.
"""

import math
from typing import TypedDict


class PasswordChecks(TypedDict):
    """Character composition checks for a password."""

    lowercase: bool
    uppercase: bool
    digits: bool
    special: bool


class PasswordAnalysis(TypedDict):
    """Structured password strength analysis result."""

    password: str
    length: int
    score: int
    strength: str
    entropy_bits: float
    checks: PasswordChecks
    reason: str


def analyze_password_strength(password: str) -> PasswordAnalysis:
    """
    Analyze password strength using simple rules.

    Args:
        password: Password text to evaluate

    Returns:
        Dictionary with rating, score, entropy estimate, and explanation

    Raises:
        ValueError: If password is not a non-empty string
    """
    if not isinstance(password, str) or not password:
        raise ValueError("password must be a non-empty string")

    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    score = 0
    reasons = []

    # Length checks
    if length >= 8:
        score += 1
    else:
        reasons.append("too short")

    if length >= 12:
        score += 1

    # Character-type checks
    if has_lower and has_upper:
        score += 1
    else:
        reasons.append("missing mixed case")

    if has_digit:
        score += 1
    else:
        reasons.append("no digits")

    if has_special:
        score += 1
    else:
        reasons.append("no special characters")

    # Simple common-pattern penalty
    lowered = password.lower()
    common_patterns = ("password", "123456", "qwerty", "admin")
    if any(pattern in lowered for pattern in common_patterns):
        score -= 1
        reasons.append("common pattern")

    # Clamp score into a simple 0..5 range
    score = max(0, min(score, 5))

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    # Basic entropy estimate: length * log2(character pool)
    pool_size = 0
    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_special:
        pool_size += 32

    entropy_bits = round(length * math.log2(pool_size), 2) if pool_size > 0 else 0.0

    explanation = "good length and character variety" if not reasons else ", ".join(reasons)

    return {
        "password": password,
        "length": length,
        "score": score,
        "strength": strength,
        "entropy_bits": entropy_bits,
        "checks": {
            "lowercase": has_lower,
            "uppercase": has_upper,
            "digits": has_digit,
            "special": has_special,
        },
        "reason": explanation,
    }
