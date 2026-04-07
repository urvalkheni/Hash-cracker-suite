#!/usr/bin/env python3
"""
Hash Cracker Suite - Main CLI Interface
"""

import argparse
import sys
from pathlib import Path

from src.cli.hash_mode import handle_hash_mode
from src.cli.dict_mode import handle_dict_mode
from src.cli.brute_mode import handle_brute_mode
from src.cli.check_mode import handle_check_mode


def create_parser() -> argparse.ArgumentParser:
    """Create and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Hash Cracker Suite - Hashing, cracking, and password analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Hash generate:
        python -m src.cracker hash --text password --algorithm md5

  Hash verify:
        python -m src.cracker hash --text password --hash 5f4dcc3b5aa765d61d8327deb882cf99 --algorithm md5

  Dictionary attack:
        python -m src.cracker dict --hash 5f4dcc3b5aa765d61d8327deb882cf99 --wordlist data/wordlists/common.txt --algorithm md5 --i-understand-legal-use

  Brute-force attack:
        python -m src.cracker brute --hash 900150983cd24fb0d6963f7d28e17f72 --algorithm md5 --max-length 3 --i-understand-legal-use --force

  Password check:
        python -m src.cracker check --text password123
        """,
    )

    subparsers = parser.add_subparsers(dest="mode", required=True)

    hash_parser = subparsers.add_parser("hash", help="Generate or verify hashes")
    hash_parser.add_argument("--text", required=True, help="Input text")
    hash_parser.add_argument("--hash", help="Target hash for verification")
    hash_parser.add_argument(
        "--algorithm",
        choices=["md5", "sha1", "sha256"],
        default="sha256",
        help="Hash algorithm (default: sha256)",
    )

    dict_parser = subparsers.add_parser("dict", help="Run dictionary attack")
    dict_parser.add_argument("--hash", required=True, help="Target hash")
    dict_parser.add_argument(
        "--wordlist",
        type=Path,
        required=True,
        help="Path to wordlist file",
    )
    dict_parser.add_argument(
        "--algorithm",
        choices=["md5", "sha1", "sha256"],
        default="sha256",
        help="Hash algorithm (default: sha256)",
    )
    dict_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable progress output",
    )
    dict_parser.add_argument(
        "--progress-interval",
        type=int,
        default=1000,
        help="Show progress every N attempts (default: 1000)",
    )
    dict_parser.add_argument(
        "--i-understand-legal-use",
        action="store_true",
        help="Acknowledge authorized use requirement",
    )

    brute_parser = subparsers.add_parser("brute", help="Run brute-force attack")
    brute_parser.add_argument("--hash", required=True, help="Target hash")
    brute_parser.add_argument(
        "--algorithm",
        choices=["md5", "sha1", "sha256"],
        default="sha256",
        help="Hash algorithm (default: sha256)",
    )
    brute_parser.add_argument(
        "--max-length",
        dest="max_length",
        type=int,
        default=4,
        help="Maximum password length (default: 4)",
    )
    brute_parser.add_argument(
        "--charset",
        default="abcdefghijklmnopqrstuvwxyz",
        help="Character set (default: lowercase a-z)",
    )
    brute_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable progress output",
    )
    brute_parser.add_argument(
        "--progress-interval",
        type=int,
        default=1000,
        help="Show progress every N attempts (default: 1000)",
    )
    brute_parser.add_argument(
        "--i-understand-legal-use",
        action="store_true",
        help="Acknowledge authorized use requirement",
    )
    brute_parser.add_argument(
        "--force",
        action="store_true",
        help="Force execution for large brute-force search spaces",
    )

    check_parser = subparsers.add_parser("check", help="Analyze password strength")
    check_parser.add_argument("--text", required=True, help="Password text")

    return parser


def main() -> None:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    try:
        if args.mode == "hash":
            success = handle_hash_mode(args)
        elif args.mode == "dict":
            if args.progress_interval < 1:
                parser.error("--progress-interval must be >= 1")
            if not args.i_understand_legal_use:
                parser.error(
                    "You must acknowledge authorized use to run attack modes. "
                    "Use --i-understand-legal-use"
                )
            success = handle_dict_mode(args)
        elif args.mode == "brute":
            if args.progress_interval < 1:
                parser.error("--progress-interval must be >= 1")
            if not args.i_understand_legal_use:
                parser.error(
                    "You must acknowledge authorized use to run attack modes. "
                    "Use --i-understand-legal-use"
                )
            success = handle_brute_mode(args)
        elif args.mode == "check":
            success = handle_check_mode(args)
        else:
            parser.error(f"Unknown mode: {args.mode}")

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()
