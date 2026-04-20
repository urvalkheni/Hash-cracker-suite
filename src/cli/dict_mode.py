"""Dictionary mode handler."""

from argparse import Namespace

from src.core.dictionary_attack import (
    DictionaryAttackError,
    run_dictionary_attack,
    validate_wordlist,
)
from src.core.hash_utils import validate_hash_input


def handle_dict_mode(args: Namespace) -> bool:
    """Handle dictionary attack."""
    print("\n" + "=" * 60)
    print("Hash Cracker Suite - Dictionary Attack")
    print("=" * 60 + "\n")

    if not args.hash:
        print("[!] Error: --hash is required for dictionary mode")
        return False

    if not args.wordlist:
        print("[!] Error: --wordlist is required for dictionary mode")
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

    is_valid, validation_msg = validate_wordlist(args.wordlist)
    if not is_valid:
        print(f"[-] {validation_msg}")
        return False

    print(f"[+] Target Hash: {args.hash}")
    print(f"[+] Algorithm: {args.algorithm.upper()}")
    print(f"[+] Wordlist: {args.wordlist}")
    print(f"[+] {validation_msg}")
    print()

    try:
        found, password, attempts = run_dictionary_attack(
            target_hash=args.hash,
            wordlist_path=args.wordlist,
            algorithm=args.algorithm,
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

    except DictionaryAttackError as e:
        print(f"[-] Error: {e}")
        return False
    except Exception as e:
        print(f"[-] Unexpected error: {e}")
        return False
