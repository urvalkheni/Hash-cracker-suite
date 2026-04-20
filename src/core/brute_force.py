"""
Brute Force Attack Module

Implements hash cracking by generating every combination from a charset
up to a maximum length.

Educational purpose: Demonstrates why short/weak passwords are vulnerable.
"""

from itertools import product

from .hash_utils import (
    UnsupportedAlgorithmError,
    generate_hash,
    validate_hash_input,
)


class BruteForceError(Exception):
    """Raised when brute-force attack encounters an error."""


def run_brute_force(
    target_hash: str,
    algorithm: str = "sha256",
    charset: str = "abcdefghijklmnopqrstuvwxyz",
    max_length: int = 4,
    show_progress: bool = False,
    progress_interval: int = 1000,
) -> tuple[bool, str | None, int]:
    """
    Perform brute-force attack on a target hash.

    Args:
        target_hash: Hash to crack (hexadecimal string)
        algorithm: Hash algorithm (md5, sha1, sha256)
        charset: Characters to use for candidate generation
        max_length: Maximum candidate length to try (starts at length 1)
        show_progress: Whether to print periodic progress updates
        progress_interval: Print progress every N attempts when show_progress is True

    Returns:
        Tuple (found, password, attempts)
        - found: True if password matched, else False
        - password: Matching password if found, else None
        - attempts: Total attempted candidates

    Raises:
        BruteForceError: For invalid input or runtime errors
    """
    if not isinstance(target_hash, str) or not target_hash.strip():
        raise BruteForceError("target_hash must be a non-empty string")

    if not isinstance(charset, str) or not charset:
        raise BruteForceError("charset must be a non-empty string")

    if not isinstance(max_length, int) or max_length < 1:
        raise BruteForceError("max_length must be an integer >= 1")

    if not isinstance(progress_interval, int) or progress_interval < 1:
        raise BruteForceError("progress_interval must be an integer >= 1")

    attempts = 0

    try:
        target_hash_lower = validate_hash_input(target_hash, algorithm)

        for length in range(1, max_length + 1):
            for chars in product(charset, repeat=length):
                candidate = "".join(chars)
                attempts += 1

                if show_progress and attempts % progress_interval == 0:
                    print(f"[*] Attempts: {attempts} | Trying: {candidate}")

                candidate_hash = generate_hash(candidate, algorithm)
                if candidate_hash.lower() == target_hash_lower:
                    return (True, candidate, attempts)

        return (False, None, attempts)

    except UnsupportedAlgorithmError as e:
        raise BruteForceError(str(e)) from e
    except BruteForceError:
        raise
    except Exception as e:
        raise BruteForceError(f"Error during brute-force attack: {e}") from e
