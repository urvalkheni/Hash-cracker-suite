"""
Test suite for hash utilities.

Run with: python -m pytest tests/test_hash_utils.py
Or: python tests/test_hash_utils.py
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.hash_utils import (
    generate_hash,
    verify_hash,
    get_algorithm_info,
    UnsupportedAlgorithmError,
)


def test_generate_hash_md5():
    """Test MD5 hash generation."""
    text = "password"
    expected = "5f4dcc3b5aa765d61d8327deb882cf99"
    result = generate_hash(text, "md5")
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ MD5 hash generation: PASS")


def test_generate_hash_sha1():
    """Test SHA-1 hash generation."""
    text = "password"
    expected = "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8"
    result = generate_hash(text, "sha1")
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ SHA-1 hash generation: PASS")


def test_generate_hash_sha256():
    """Test SHA-256 hash generation."""
    text = "password"
    expected = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
    result = generate_hash(text, "sha256")
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ SHA-256 hash generation: PASS")


def test_verify_hash_match():
    """Test hash verification - matching case."""
    text = "password"
    target_hash = "5f4dcc3b5aa765d61d8327deb882cf99"
    result = verify_hash(text, target_hash, "md5")
    assert result is True, "Verification should return True for matching hash"
    print("✓ Hash verification (match): PASS")


def test_verify_hash_no_match():
    """Test hash verification - non-matching case."""
    text = "wrong"
    target_hash = "5f4dcc3b5aa765d61d8327deb882cf99"
    result = verify_hash(text, target_hash, "md5")
    assert result is False, "Verification should return False for non-matching hash"
    print("✓ Hash verification (no match): PASS")


def test_case_insensitive_verification():
    """Test that hash verification is case-insensitive."""
    text = "password"
    target_hash = "5F4DCC3B5AA765D61D8327DEB882CF99"  # Uppercase
    result = verify_hash(text, target_hash, "md5")
    assert result is True, "Verification should be case-insensitive"
    print("✓ Case-insensitive verification: PASS")


def test_unsupported_algorithm():
    """Test error handling for unsupported algorithm."""
    try:
        generate_hash("password", "md2")
        assert False, "Should raise UnsupportedAlgorithmError"
    except UnsupportedAlgorithmError:
        print("✓ Unsupported algorithm error: PASS")


def test_algorithm_info():
    """Test algorithm info retrieval."""
    info = get_algorithm_info("md5")
    assert "md5" in info, "Should contain md5 key"
    assert info["md5"]["name"] == "MD5", "Should have correct name"
    assert info["md5"]["digest_size"] == 16, "MD5 should have 16 byte digest"
    print("✓ Algorithm info: PASS")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Hash Utilities Test Suite")
    print("=" * 60 + "\n")

    tests = [
        test_generate_hash_md5,
        test_generate_hash_sha1,
        test_generate_hash_sha256,
        test_verify_hash_match,
        test_verify_hash_no_match,
        test_case_insensitive_verification,
        test_unsupported_algorithm,
        test_algorithm_info,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: FAIL - {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: ERROR - {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
