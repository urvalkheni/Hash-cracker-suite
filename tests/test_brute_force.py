import pytest

from src.core.brute_force import BruteForceError, run_brute_force


def test_brute_force_md5_success():
    found, password, attempts = run_brute_force(
        target_hash="900150983cd24fb0d6963f7d28e17f72",
        algorithm="md5",
        charset="abcdefghijklmnopqrstuvwxyz",
        max_length=3,
    )
    assert found is True
    assert password == "abc"
    assert attempts == 731


def test_brute_force_not_found():
    found, password, attempts = run_brute_force(
        target_hash="5f4dcc3b5aa765d61d8327deb882cf99",
        algorithm="md5",
        charset="ab",
        max_length=2,
    )
    assert found is False
    assert password is None
    assert attempts == 6


def test_brute_force_invalid_max_length():
    with pytest.raises(BruteForceError):
        run_brute_force(target_hash="5f4dcc3b5aa765d61d8327deb882cf99", max_length=0)


def test_brute_force_invalid_charset():
    with pytest.raises(BruteForceError):
        run_brute_force(target_hash="5f4dcc3b5aa765d61d8327deb882cf99", charset="")


def test_brute_force_invalid_hash_format():
    with pytest.raises(BruteForceError):
        run_brute_force(target_hash="not-a-hash", algorithm="md5", charset="ab", max_length=2)
