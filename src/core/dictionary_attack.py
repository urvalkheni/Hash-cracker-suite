"""
Dictionary Attack Module

Implements password cracking using a wordlist/dictionary.
Effective against weak passwords that appear in common word lists.

Educational purpose: Understanding dictionary attack vulnerabilities.
"""

from pathlib import Path
from typing import Optional, Tuple
import sys

from .hash_utils import generate_hash, UnsupportedAlgorithmError


class DictionaryAttackError(Exception):
    """Raised when dictionary attack encounters an error."""

    pass


def run_dictionary_attack(
    target_hash: str,
    wordlist_path: Path,
    algorithm: str = "sha256",
    show_progress: bool = True,
) -> Tuple[bool, Optional[str], int]:
    """
    Perform dictionary attack on target hash using wordlist.

    Args:
        target_hash: Hash to crack (hexadecimal string)
        wordlist_path: Path to wordlist file (one word per line)
        algorithm: Hash algorithm (md5, sha1, sha256)
        show_progress: Whether to display progress output

    Returns:
        Tuple of (found: bool, password: Optional[str], attempts: int)
        - found: True if password matched, False otherwise
        - password: Matched password string if found, None otherwise
        - attempts: Total number of words tried

    Raises:
        DictionaryAttackError: If wordlist file issues or other errors

    Examples:
        >>> found, pwd, attempts = run_dictionary_attack(
        ...     target_hash="5f4dcc3b5aa765d61d8327deb882cf99",
        ...     wordlist_path=Path("wordlist.txt"),
        ...     algorithm="md5"
        ... )
        >>> if found:
        ...     print(f"Found: {pwd} in {attempts} attempts")
    """

    # Validate target hash
    if not isinstance(target_hash, str) or not target_hash:
        raise DictionaryAttackError("target_hash must be a non-empty string")

    # Validate wordlist path
    if not isinstance(wordlist_path, Path):
        wordlist_path = Path(wordlist_path)

    if not wordlist_path.exists():
        raise DictionaryAttackError(f"Wordlist file not found: {wordlist_path}")

    if not wordlist_path.is_file():
        raise DictionaryAttackError(f"Not a file: {wordlist_path}")

    attempts = 0
    target_hash_lower = target_hash.lower()

    try:
        # Open and read wordlist
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                # Strip whitespace and skip empty lines
                word = line.strip()
                if not word:
                    continue

                attempts += 1

                # Show progress
                if show_progress:
                    print(f"[*] Trying: {word}")

                try:
                    # Hash the word
                    word_hash = generate_hash(word, algorithm)

                    # Compare with target hash (case-insensitive)
                    if word_hash.lower() == target_hash_lower:
                        if show_progress:
                            print()  # Blank line for clarity
                        return (True, word, attempts)

                except UnsupportedAlgorithmError as e:
                    raise DictionaryAttackError(f"Invalid algorithm: {e}")

        # No match found
        return (False, None, attempts)

    except DictionaryAttackError:
        raise
    except Exception as e:
        raise DictionaryAttackError(f"Error during dictionary attack: {e}")


def validate_wordlist(wordlist_path: Path) -> Tuple[bool, str]:
    """
    Validate wordlist file and return useful information.

    Args:
        wordlist_path: Path to wordlist file

    Returns:
        Tuple of (is_valid: bool, message: str)

    Examples:
        >>> is_valid, msg = validate_wordlist(Path("wordlist.txt"))
        >>> print(f"Valid: {is_valid}, {msg}")
    """
    if not isinstance(wordlist_path, Path):
        wordlist_path = Path(wordlist_path)

    # Check existence
    if not wordlist_path.exists():
        return (False, f"File not found: {wordlist_path}")

    # Check if it's a file
    if not wordlist_path.is_file():
        return (False, f"Not a file: {wordlist_path}")

    # Count lines
    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            word_count = sum(1 for line in f if line.strip())

        if word_count == 0:
            return (False, "Wordlist is empty")

        return (True, f"Valid wordlist with {word_count} words")

    except Exception as e:
        return (False, f"Error reading file: {e}")
