import pytest
from src.core.hash_utils import (
    UnsupportedAlgorithmError,
    generate_hash,
    get_algorithm_info,
    validate_hash_input,
    verify_hash,
)


def test_generate_hash_md5():
    assert generate_hash("password", "md5") == "5f4dcc3b5aa765d61d8327deb882cf99"


def test_generate_hash_sha1():
    assert generate_hash("password", "sha1") == "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8"


def test_generate_hash_sha256():
    assert (
        generate_hash("password", "sha256")
        == "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
    )


def test_verify_hash_match():
    assert verify_hash("password", "5f4dcc3b5aa765d61d8327deb882cf99", "md5") is True


def test_verify_hash_no_match():
    assert verify_hash("wrong", "5f4dcc3b5aa765d61d8327deb882cf99", "md5") is False


def test_verify_hash_case_insensitive_target():
    assert verify_hash("password", "5F4DCC3B5AA765D61D8327DEB882CF99", "md5") is True


def test_unsupported_algorithm_error():
    with pytest.raises(UnsupportedAlgorithmError):
        generate_hash("password", "md2")


def test_algorithm_info_md5():
    info = get_algorithm_info("md5")
    assert info["md5"]["name"] == "MD5"
    assert info["md5"]["digest_size"] == 16


@pytest.mark.parametrize(
    "target_hash,algorithm",
    [
        ("zzzz", "md5"),
        ("12345", "md5"),
        ("5f4dcc3b5aa765d61d8327deb882cf99", "sha1"),
    ],
)
def test_validate_hash_input_rejects_invalid(target_hash, algorithm):
    with pytest.raises(ValueError):
        validate_hash_input(target_hash, algorithm)


def test_validate_hash_input_accepts_valid():
    value = validate_hash_input("5F4DCC3B5AA765D61D8327DEB882CF99", "md5")
    assert value == "5f4dcc3b5aa765d61d8327deb882cf99"
