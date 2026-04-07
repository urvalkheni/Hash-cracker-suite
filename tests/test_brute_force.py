"""
Test suite for brute-force attack module.

Run with:
    python tests/test_brute_force.py
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.brute_force import run_brute_force, BruteForceError


def test_brute_force_md5_success():
    """Should find 'abc' from lowercase charset up to length 3."""
    found, password, attempts = run_brute_force(
        target_hash="900150983cd24fb0d6963f7d28e17f72",
        algorithm="md5",
        charset="abcdefghijklmnopqrstuvwxyz",
        max_length=3,
        show_progress=False,
    )
    assert found is True
    assert password == "abc"
    assert attempts == 731
    print("PASS: test_brute_force_md5_success")


def test_brute_force_not_found():
    """Should exhaust attempts when no candidate matches."""
    found, password, attempts = run_brute_force(
        target_hash="deadbeef",
        algorithm="md5",
        charset="ab",
        max_length=2,
        show_progress=False,
    )
    assert found is False
    assert password is None
    assert attempts == 6  # a, b, aa, ab, ba, bb
    print("PASS: test_brute_force_not_found")


def test_brute_force_invalid_max_length():
    """Should reject invalid max_length values."""
    try:
        run_brute_force(target_hash="abc", max_length=0, show_progress=False)
        raise AssertionError("Expected BruteForceError for max_length=0")
    except BruteForceError:
        print("PASS: test_brute_force_invalid_max_length")


def test_brute_force_invalid_charset():
    """Should reject empty charset."""
    try:
        run_brute_force(target_hash="abc", charset="", show_progress=False)
        raise AssertionError("Expected BruteForceError for empty charset")
    except BruteForceError:
        print("PASS: test_brute_force_invalid_charset")


def run_all_tests() -> bool:
    tests = [
        test_brute_force_md5_success,
        test_brute_force_not_found,
        test_brute_force_invalid_max_length,
        test_brute_force_invalid_charset,
    ]
    passed = 0
    failed = 0

    print("\nBrute Force Test Suite\n" + "=" * 40)
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"FAIL: {test.__name__} -> {e}")
            failed += 1

    print("=" * 40)
    print(f"Results: {passed} passed, {failed} failed\n")
    return failed == 0


if __name__ == "__main__":
    ok = run_all_tests()
    sys.exit(0 if ok else 1)