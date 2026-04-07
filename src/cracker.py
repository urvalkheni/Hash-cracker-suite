#!/usr/bin/env python3
"""
Hash Cracker Suite - Main CLI Interface

Usage:
    python cracker.py --help
"""

import argparse
import sys
from pathlib import Path

# Import hash utilities
from core.hash_utils import (
    generate_hash,
    verify_hash,
    get_algorithm_info,
    UnsupportedAlgorithmError,
)

# Import attack modules
from core.dictionary_attack import (
    run_dictionary_attack,
    validate_wordlist,
    DictionaryAttackError,
)
from core.brute_force import run_brute_force, BruteForceError


def create_parser():
    """Create and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Hash Cracker Suite - Crack hashes using multiple techniques",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    Generate Hash:
        python cracker.py --mode hash --text password --algorithm md5

    Verify Hash:
        python cracker.py --mode hash --text password --hash 5f4dcc3b5aa765d61d8327deb882cf99 --algorithm md5

    Dictionary Attack (Phase 3):
        python cracker.py --mode dict --hash <hash> --wordlist data/wordlists/sample.txt

    Brute Force (Phase 4):
        python cracker.py --mode brute --hash <hash> --algorithm md5 --max-length 3

    Rainbow Table (Not Implemented Yet):
        python cracker.py --mode rainbow --hash <hash>
                """,
        )

    parser.add_argument(
        "--mode",
        choices=["hash", "dict", "brute", "rainbow"],
        required=True,
        help="Operation mode: hash (generate/verify), dict, brute, rainbow",
    )

    parser.add_argument(
        "--hash",
        help="Target hash to crack or verify against",
    )

    parser.add_argument(
        "--text",
        help="Text to hash or verify",
    )

    parser.add_argument(
        "--algorithm",
        choices=["md5", "sha1", "sha256"],
        default="sha256",
        help="Hash algorithm (default: sha256)",
    )

    parser.add_argument(
        "--wordlist",
        type=Path,
        help="Path to wordlist file (for dictionary attack)",
    )

    parser.add_argument(
        "--max-length",
        dest="max_length",
        type=int,
        default=4,
        help="Maximum password length for brute-force (default: 4)",
    )

    parser.add_argument(
        "--charset",
        default="abcdefghijklmnopqrstuvwxyz",
        help="Character set for brute-force (default: lowercase a-z)",
    )

    return parser


def handle_hash_mode(args):
    """Handle hash generation and verification."""
    print("\n" + "=" * 60)
    print("Hash Cracker Suite - Hash Utility (Phase 2)")
    print("=" * 60 + "\n")

    # Validate required arguments
    if not args.text:
        print("[!] Error: --text is required for hash mode")
        print("[*] Usage: python cracker.py --mode hash --text <text> --algorithm <algo>")
        return False

    try:
        # Generate hash
        generated_hash = generate_hash(args.text, args.algorithm)

        print(f"[+] Text: {args.text}")
        print(f"[+] Algorithm: {args.algorithm.upper()}")
        print(f"[+] Generated Hash: {generated_hash}\n")

        # If target hash provided, verify
        if args.hash:
            is_match = verify_hash(args.text, args.hash, args.algorithm)

            print(f"[*] Verification:")
            print(f"[*] Target Hash: {args.hash}")
            print(f"[*] Generated Hash: {generated_hash}")

            if is_match:
                print(f"[+] ✓ MATCH FOUND! Password is: {args.text}\n")
            else:
                print(f"[-] ✗ No match. Hashes do not match.\n")

            return is_match

        return True

    except UnsupportedAlgorithmError as e:
        print(f"[-] Error: {e}")
        return False
    except Exception as e:
        print(f"[-] Unexpected error: {e}")
        return False


def handle_dict_mode(args):
    """Handle dictionary attack."""
    print("\n" + "=" * 60)
    print("Hash Cracker Suite - Dictionary Attack (Phase 3)")
    print("=" * 60 + "\n")

    # Validate required arguments
    if not args.hash:
        print("[!] Error: --hash is required for dictionary mode")
        return False

    if not args.wordlist:
        print("[!] Error: --wordlist is required for dictionary mode")
        return False

    # Validate wordlist
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
        # Run dictionary attack
        found, password, attempts = run_dictionary_attack(
            target_hash=args.hash,
            wordlist_path=args.wordlist,
            algorithm=args.algorithm,
            show_progress=True,
        )

        # Display results
        print("=" * 60)
        if found:
            print(f"[+] ✓ MATCH FOUND: {password}")
            print(f"[+] Attempts: {attempts}")
            print("=" * 60 + "\n")
            return True
        else:
            print(f"[-] ✗ No match found")
            print(f"[-] Attempts: {attempts}")
            print("=" * 60 + "\n")
            return False

    except DictionaryAttackError as e:
        print(f"[-] Error: {e}")
        return False
    except Exception as e:
        print(f"[-] Unexpected error: {e}")
        return False


def handle_brute_mode(args):
    """Handle brute-force attack."""
    print("\n" + "=" * 60)
    print("Hash Cracker Suite - Brute Force Attack (Phase 4)")
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

    print(f"[+] Target Hash: {args.hash}")
    print(f"[+] Algorithm: {args.algorithm.upper()}")
    print(f"[+] Charset: {args.charset}")
    print(f"[+] Max Length: {args.max_length}")
    print("\n[*] Trying combinations...\n")

    try:
        found, password, attempts = run_brute_force(
            target_hash=args.hash,
            algorithm=args.algorithm,
            charset=args.charset,
            max_length=args.max_length,
            show_progress=True,
            progress_interval=1000,
        )

        print("=" * 60)
        if found:
            print(f"[+] ✓ MATCH FOUND: {password}")
            print(f"[+] Attempts: {attempts}")
            print("=" * 60 + "\n")
            return True

        print("[-] ✗ No match found")
        print(f"[-] Attempts exhausted: {attempts}")
        print("=" * 60 + "\n")
        return False

    except BruteForceError as e:
        print(f"[-] Error: {e}")
        return False
    except Exception as e:
        print(f"[-] Unexpected error: {e}")
        return False


def handle_rainbow_mode(args):
    """Handle rainbow table lookup (Phase 4)."""
    print("\n[!] Rainbow table lookup coming in Phase 4...\n")
    return False


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    try:
        # Route to appropriate handler
        if args.mode == "hash":
            success = handle_hash_mode(args)
        elif args.mode == "dict":
            if not args.hash:
                parser.error("--hash is required for dictionary attack mode")
            if not args.wordlist:
                parser.error("--wordlist is required for dictionary attack mode")
            success = handle_dict_mode(args)
        elif args.mode == "brute":
            if not args.hash:
                parser.error("--hash is required for brute-force mode")
            if args.max_length is None:
                parser.error("--max-length is required for brute-force mode")
            success = handle_brute_mode(args)
        elif args.mode == "rainbow":
            if not args.hash:
                parser.error("--hash is required for rainbow table mode")
            success = handle_rainbow_mode(args)
        else:
            parser.error(f"Unknown mode: {args.mode}")

        # Exit with appropriate code
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\n[!] Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[-] Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
