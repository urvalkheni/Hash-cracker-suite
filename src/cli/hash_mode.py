"""Hash mode handler."""

from argparse import Namespace

from src.core.hash_utils import (
    UnsupportedAlgorithmError,
    generate_hash,
    validate_hash_input,
    verify_hash,
)


def handle_hash_mode(args: Namespace) -> bool:
    """Handle hash generation and verification."""
    print("\n" + "=" * 60)
    print("Hash Cracker Suite - Hash Utility")
    print("=" * 60 + "\n")

    if not args.text:
        print("[!] Error: --text is required for hash mode")
        return False

    try:
        if args.algorithm in ("md5", "sha1"):
            print(
                "[!] WARNING: MD5/SHA1 are cryptographically broken "
                "and should not be used in real systems."
            )

        if args.hash:
            validate_hash_input(args.hash, args.algorithm)

        generated_hash = generate_hash(args.text, args.algorithm)

        print(f"[+] Text: {args.text}")
        print(f"[+] Algorithm: {args.algorithm.upper()}")
        print(f"[+] Generated Hash: {generated_hash}\n")

        if args.hash:
            is_match = verify_hash(args.text, args.hash, args.algorithm)
            print("[*] Verification:")
            print(f"[*] Target Hash: {args.hash}")
            print(f"[*] Generated Hash: {generated_hash}")
            if is_match:
                print(f"[+] MATCH FOUND! Password is: {args.text}\n")
            else:
                print("[-] No match. Hashes do not match.\n")
            return is_match

        return True

    except (UnsupportedAlgorithmError, ValueError, TypeError) as e:
        print(f"[-] Error: {e}")
        return False
    except Exception as e:
        print(f"[-] Unexpected error: {e}")
        return False
