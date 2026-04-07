import pytest

from src.core.password_strength import analyze_password_strength


def test_weak_password():
    result = analyze_password_strength("password123")
    assert result["strength"] == "Weak"
    assert "common pattern" in result["reason"]


def test_medium_or_strong_password():
    result = analyze_password_strength("Abcd1234")
    assert result["strength"] in ("Medium", "Strong")


def test_strong_password():
    result = analyze_password_strength("Aq7!zP9@Lm#2")
    assert result["strength"] == "Strong"
    assert result["score"] == 5


def test_invalid_password_raises():
    with pytest.raises(ValueError):
        analyze_password_strength("")
