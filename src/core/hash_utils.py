"""
Hash Utility Module

Provides hash generation and verification functions.
Supports MD5, SHA-1, SHA-256 algorithms.

Educational purpose: Understanding hash functions and verification.
"""

import hashlib
from collections.abc import Callable
from typing import Any, Literal, Protocol, TypeAlias, cast

AlgorithmName: TypeAlias = Literal["md5", "sha1", "sha256"]
AlgorithmInfo = dict[str, dict[str, int | str]]


class HashObject(Protocol):
    """Minimal protocol shared by hashlib hash objects."""

    digest_size: int
    block_size: int

    def hexdigest(self) -> str:
        """Return the hexadecimal digest."""


# Supported hash algorithms
SUPPORTED_ALGORITHMS: dict[AlgorithmName, Callable[..., Any]] = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
}

HASH_LENGTHS: dict[AlgorithmName, int] = {
    "md5": 32,
    "sha1": 40,
    "sha256": 64,
}


class UnsupportedAlgorithmError(Exception):
    """Raised when an unsupported hash algorithm is requested."""


def _validate_algorithm(algorithm: str) -> AlgorithmName:
    """Validate and normalize algorithm name."""
    normalized = algorithm.lower()
    if normalized not in SUPPORTED_ALGORITHMS:
        raise UnsupportedAlgorithmError(
            f"Unsupported algorithm: {algorithm}. "
            f"Supported algorithms: {', '.join(SUPPORTED_ALGORITHMS.keys())}"
        )
    return normalized


def validate_hash_input(target_hash: str, algorithm: str) -> str:
    """
    Validate hash format for a specific algorithm.

    Rules:
    - hex characters only
    - exact length per algorithm
    """
    if not isinstance(target_hash, str) or not target_hash:
        raise ValueError("target_hash must be a non-empty string")

    normalized_algorithm = _validate_algorithm(algorithm)
    normalized_hash = target_hash.lower().strip()

    if not all(char in "0123456789abcdef" for char in normalized_hash):
        raise ValueError("target_hash must contain only hexadecimal characters")

    expected_length = HASH_LENGTHS[normalized_algorithm]
    if len(normalized_hash) != expected_length:
        raise ValueError(
            f"target_hash length invalid for {normalized_algorithm}. "
            f"Expected {expected_length} characters"
        )

    return normalized_hash


def generate_hash(text: str, algorithm: str = "sha256") -> str:
    """
    Generate a hash for the given text using the specified algorithm.

    Args:
        text: The text to hash
        algorithm: Hash algorithm to use (md5, sha1, sha256)
                  Default: sha256

    Returns:
        Hexadecimal hash string

    Raises:
        UnsupportedAlgorithmError: If algorithm is not supported
        TypeError: If text is not a string

    Examples:
        >>> generate_hash("password")
        '5e884898da28047151d0e56f8dc62927...'

        >>> generate_hash("password", "md5")
        '5f4dcc3b5aa765d61d8327deb882cf99'
    """
    # Validate algorithm
    algorithm = _validate_algorithm(algorithm)

    # Validate text input
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")

    # Generate hash
    hash_obj = cast(HashObject, SUPPORTED_ALGORITHMS[algorithm](text.encode("utf-8")))
    return hash_obj.hexdigest()


def verify_hash(
    text: str,
    target_hash: str,
    algorithm: str = "sha256",
) -> bool:
    """
    Verify if the given text matches the target hash.

    Args:
        text: The text to verify
        target_hash: The hash to compare against (hexadecimal string)
        algorithm: Hash algorithm to use (md5, sha1, sha256)
                  Default: sha256

    Returns:
        True if text hashes to target_hash, False otherwise

    Raises:
        UnsupportedAlgorithmError: If algorithm is not supported
        TypeError: If inputs are not strings

    Examples:
        >>> verify_hash("password", "5f4dcc3b5aa765d61d8327deb882cf99", "md5")
        True

        >>> verify_hash("wrong", "5f4dcc3b5aa765d61d8327deb882cf99", "md5")
        False
    """
    # Validate inputs
    if not isinstance(text, str):
        raise TypeError(f"text must be string, got {type(text).__name__}")

    if not isinstance(target_hash, str):
        raise TypeError(f"target_hash must be string, got {type(target_hash).__name__}")

    # Validate algorithm and hash format
    algorithm = _validate_algorithm(algorithm)
    normalized_target = validate_hash_input(target_hash, algorithm)

    # Generate hash and compare
    generated_hash = generate_hash(text, algorithm)
    return generated_hash.lower() == normalized_target


def _get_algorithm_metadata(algorithm: AlgorithmName) -> dict[str, int | str]:
    """Build metadata for a supported algorithm."""
    hash_obj = cast(HashObject, SUPPORTED_ALGORITHMS[algorithm]())
    return {
        "name": algorithm.upper(),
        "digest_size": hash_obj.digest_size,
        "block_size": hash_obj.block_size if hasattr(hash_obj, "block_size") else "N/A",
    }


def get_algorithm_info(algorithm: str | None = None) -> AlgorithmInfo:
    """
    Get information about supported hash algorithms.

    Args:
        algorithm: Specific algorithm to get info for, or None for all

    Returns:
        Dictionary with algorithm information

    Examples:
        >>> get_algorithm_info("md5")
        {'md5': {'name': 'MD5', 'digest_size': 16, ...}}
    """
    if algorithm is None:
        return {algo: _get_algorithm_metadata(algo) for algo in SUPPORTED_ALGORITHMS}

    normalized_algorithm = _validate_algorithm(algorithm)
    return {normalized_algorithm: _get_algorithm_metadata(normalized_algorithm)}
