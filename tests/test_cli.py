import subprocess
import sys
from pathlib import Path
from subprocess import CompletedProcess

ROOT = Path(__file__).resolve().parent.parent


def run_cli(*args: str) -> CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "src.cracker", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_hash_generate_success():
    result = run_cli("hash", "--text", "password", "--algorithm", "md5")
    assert result.returncode == 0
    assert "5f4dcc3b5aa765d61d8327deb882cf99" in result.stdout
    assert "cryptographically broken" in result.stdout


def test_cli_dict_invalid_hash_rejected():
    result = run_cli(
        "dict",
        "--hash",
        "bad_hash",
        "--wordlist",
        "data/wordlists/common.txt",
        "--algorithm",
        "md5",
        "--i-understand-legal-use",
    )
    assert result.returncode == 1
    assert "Invalid hash" in result.stdout


def test_cli_brute_success_small_space():
    result = run_cli(
        "brute",
        "--hash",
        "900150983cd24fb0d6963f7d28e17f72",
        "--algorithm",
        "md5",
        "--max-length",
        "3",
        "--i-understand-legal-use",
        "--force",
    )
    assert result.returncode == 0
    assert "MATCH FOUND" in result.stdout


def test_cli_check_success():
    result = run_cli("check", "--text", "password123")
    assert result.returncode == 0
    assert "Strength:" in result.stdout
    assert "educational estimate only" in result.stdout


def test_cli_rejects_unknown_mode():
    result = run_cli("rainbow", "--hash", "abcd")
    assert result.returncode != 0
    assert "invalid choice" in result.stderr.lower()


def test_cli_progress_interval_validation():
    result = run_cli(
        "brute",
        "--hash",
        "900150983cd24fb0d6963f7d28e17f72",
        "--algorithm",
        "md5",
        "--max-length",
        "3",
        "--progress-interval",
        "0",
        "--i-understand-legal-use",
        "--force",
    )
    assert result.returncode != 0
    assert "progress-interval" in result.stderr.lower()


def test_cli_requires_legal_ack_for_dict():
    result = run_cli(
        "dict",
        "--hash",
        "5f4dcc3b5aa765d61d8327deb882cf99",
        "--wordlist",
        "data/wordlists/common.txt",
        "--algorithm",
        "md5",
    )
    assert result.returncode != 0
    assert "acknowledge authorized use" in result.stderr.lower()


def test_cli_requires_legal_ack_for_brute():
    result = run_cli(
        "brute",
        "--hash",
        "900150983cd24fb0d6963f7d28e17f72",
        "--algorithm",
        "md5",
        "--max-length",
        "3",
    )
    assert result.returncode != 0
    assert "acknowledge authorized use" in result.stderr.lower()


def test_cli_requires_force_for_large_bruteforce():
    result = run_cli(
        "brute",
        "--hash",
        "5f4dcc3b5aa765d61d8327deb882cf99",
        "--algorithm",
        "md5",
        "--max-length",
        "4",
        "--charset",
        "abcdefghijklmnopqrstuvwxyz",
        "--i-understand-legal-use",
    )
    assert result.returncode != 0
    assert "use --force to continue" in result.stdout.lower()
