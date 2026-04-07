"""
Test suite for dictionary attack module.

Run with: python -m pytest tests/test_dictionary_attack.py
Or: python tests/test_dictionary_attack.py
"""

import sys
import tempfile
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.dictionary_attack import (
    run_dictionary_attack,
    validate_wordlist,
    DictionaryAttackError,
)


def test_dictionary_attack_found_md5():
    """Test dictionary attack with matching hash (MD5)."""
    # Create temp wordlist
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("notpassword\n")
        f.write("password\n")
        f.write("admin\n")
        wordlist_path = Path(f.name)

    try:
        found, password, attempts = run_dictionary_attack(
            target_hash="5f4dcc3b5aa765d61d8327deb882cf99",
            wordlist_path=wordlist_path,
            algorithm="md5",
            show_progress=False,
        )

        assert found is True, "Should find password"
        assert password == "password", f"Expected 'password', got '{password}'"
        assert attempts == 2, f"Expected 2 attempts, got {attempts}"
        print("✓ Dictionary attack (found, MD5): PASS")
    finally:
        wordlist_path.unlink()


def test_dictionary_attack_found_sha256():
    """Test dictionary attack with matching hash (SHA-256)."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("notpassword\n")
        f.write("password\n")
        f.write("admin\n")
        wordlist_path = Path(f.name)

    try:
        found, password, attempts = run_dictionary_attack(
            target_hash="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            wordlist_path=wordlist_path,
            algorithm="sha256",
            show_progress=False,
        )

        assert found is True, "Should find password"
        assert password == "password", f"Expected 'password', got '{password}'"
        assert attempts == 2, f"Expected 2 attempts, got {attempts}"
        print("✓ Dictionary attack (found, SHA-256): PASS")
    finally:
        wordlist_path.unlink()


def test_dictionary_attack_not_found():
    """Test dictionary attack with non-matching hash."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("word1\n")
        f.write("word2\n")
        f.write("word3\n")
        wordlist_path = Path(f.name)

    try:
        found, password, attempts = run_dictionary_attack(
            target_hash="nonexistenthash123456",
            wordlist_path=wordlist_path,
            algorithm="md5",
            show_progress=False,
        )

        assert found is False, "Should not find password"
        assert password is None, f"Expected None, got '{password}'"
        assert attempts == 3, f"Expected 3 attempts, got {attempts}"
        print("✓ Dictionary attack (not found): PASS")
    finally:
        wordlist_path.unlink()


def test_dictionary_attack_missing_file():
    """Test dictionary attack with missing wordlist."""
    try:
        run_dictionary_attack(
            target_hash="somehash",
            wordlist_path=Path("/nonexistent/path/wordlist.txt"),
            algorithm="md5",
            show_progress=False,
        )
        assert False, "Should raise DictionaryAttackError"
    except DictionaryAttackError as e:
        assert "not found" in str(e).lower()
        print("✓ Dictionary attack (missing file error): PASS")


def test_dictionary_attack_empty_wordlist():
    """Test dictionary attack with empty wordlist."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        # Write nothing
        wordlist_path = Path(f.name)

    try:
        found, password, attempts = run_dictionary_attack(
            target_hash="somehash",
            wordlist_path=wordlist_path,
            algorithm="md5",
            show_progress=False,
        )

        assert found is False, "Should not find anything"
        assert password is None, "Password should be None"
        assert attempts == 0, f"Expected 0 attempts, got {attempts}"
        print("✓ Dictionary attack (empty wordlist): PASS")
    finally:
        wordlist_path.unlink()


def test_validate_wordlist_valid():
    """Test wordlist validation with valid file."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("word1\n")
        f.write("word2\n")
        f.write("word3\n")
        wordlist_path = Path(f.name)

    try:
        is_valid, message = validate_wordlist(wordlist_path)
        assert is_valid is True, "Should be valid"
        assert "3 words" in message, f"Message should mention word count: {message}"
        print("✓ Wordlist validation (valid): PASS")
    finally:
        wordlist_path.unlink()


def test_validate_wordlist_missing():
    """Test wordlist validation with missing file."""
    is_valid, message = validate_wordlist(Path("/nonexistent/wordlist.txt"))
    assert is_valid is False, "Should be invalid"
    assert "not found" in message.lower(), f"Message should mention not found: {message}"
    print("✓ Wordlist validation (missing file): PASS")


def test_validate_wordlist_empty():
    """Test wordlist validation with empty file."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        # Write nothing
        wordlist_path = Path(f.name)

    try:
        is_valid, message = validate_wordlist(wordlist_path)
        assert is_valid is False, "Should be invalid for empty file"
        assert "empty" in message.lower(), f"Message should mention empty: {message}"
        print("✓ Wordlist validation (empty file): PASS")
    finally:
        wordlist_path.unlink()


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Dictionary Attack Test Suite")
    print("=" * 60 + "\n")

    tests = [
        test_dictionary_attack_found_md5,
        test_dictionary_attack_found_sha256,
        test_dictionary_attack_not_found,
        test_dictionary_attack_missing_file,
        test_dictionary_attack_empty_wordlist,
        test_validate_wordlist_valid,
        test_validate_wordlist_missing,
        test_validate_wordlist_empty,
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
