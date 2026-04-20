"""Brute-force mode handler."""

from argparse import Namespace

from src.core.brute_force import BruteForceError, run_brute_force
from src.core.hash_utils import validate_hash_input

_SIGNIFICANT_COMBINATIONS = 100000


def _estimate_combinations(charset_size: int, max_length: int) -> int:
    """Estimate total combinations from length 1..max_length."""
    if charset_size <= 1:
        return max_length
    return int((charset_size * (pow(charset_size, max_length) - 1)) / (charset_size - 1))


def handle_brute_mode(args: Namespace) -> bool:
    """Handle brute-force attack."""
    print("\n" + "=" * 60)
    print("Hash Cracker Suite - Brute Force Attack")
    print("=" * 60 + "\n")

    if not args.hash:
        print("[!] Error: --hash is required for brute mode")
        return False

    if args.max_length < 1:
        print("[!] Error: --max-length must be >= 1")
        return False

    if not args.charset:
        print("[!] Error: --charset must not be empty")
        return False

    try:
        validate_hash_input(args.hash, args.algorithm)
    except ValueError as e:
        print(f"[-] Invalid hash: {e}")
        return False

    if args.algorithm in ("md5", "sha1"):
        print(
            "[!] WARNING: MD5/SHA1 are cryptographically broken "
            "and should not be used in real systems."
        )

    estimated = _estimate_combinations(len(args.charset), args.max_length)
    print(f"[+] Estimated combinations: {estimated:,}")

    if estimated > _SIGNIFICANT_COMBINATIONS and not args.force:
        print("[!] This may take significant time.")
        print("[!] Use --force to continue.")
        return False

    print(f"[+] Target Hash: {args.hash}")
    print(f"[+] Algorithm: {args.algorithm.upper()}")
    print(f"[+] Charset: {args.charset}")
    print(f"[+] Max Length: {args.max_length}")
    print()

    if args.verbose:
        print("[*] Trying combinations...\n")

    try:
        found, password, attempts = run_brute_force(
            target_hash=args.hash,
            algorithm=args.algorithm,
            charset=args.charset,
            max_length=args.max_length,
            show_progress=args.verbose,
            progress_interval=args.progress_interval,
        )

        print("=" * 60)
        if found:
            print(f"[+] MATCH FOUND: {password}")
            print(f"[+] Attempts: {attempts}")
            print("=" * 60 + "\n")
            return True

        print("[-] No match found")
        print(f"[-] Attempts exhausted: {attempts}")
        print("=" * 60 + "\n")
        return False

    except BruteForceError as e:
        print(f"[-] Error: {e}")
        return False
    except Exception as e:
        print(f"[-] Unexpected error: {e}")
        return False
