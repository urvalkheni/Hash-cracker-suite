"""Password strength check mode handler."""

from src.core.password_strength import analyze_password_strength


def handle_check_mode(args) -> bool:
    """Handle password strength analysis."""
    print("\n" + "=" * 60)
    print("Hash Cracker Suite - Password Strength Analyzer")
    print("=" * 60 + "\n")

    if not args.text:
        print("[!] Error: --text is required for check mode")
        return False

    try:
        result = analyze_password_strength(args.text)
        print(f"Password: {result['password']}")
        print(f"Strength: {result['strength']}")
        print(f"Score: {result['score']}/5")
        print(f"Entropy (estimated): {result['entropy_bits']} bits")
        print(f"Reason: {result['reason']}")
        print("Note: This is an educational estimate only.")
        return True
    except ValueError as e:
        print(f"[-] Error: {e}")
        return False
    except Exception as e:
        print(f"[-] Unexpected error: {e}")
        return False
