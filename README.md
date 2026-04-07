# 🔑 Hash Cracker Suite
> 🔐 A modular password security lab demonstrating hashing, cracking techniques, and strength analysis.

## Overview
Hash Cracker Suite is a beginner-friendly, command-line educational lab for understanding password security.

It demonstrates both offensive and defensive concepts:
- how hashes are generated and verified
- how weak passwords are cracked with dictionary and brute-force methods
- how password strength can be analyzed before use

## Features
- Hash generation and verification (MD5, SHA-1, SHA-256)
- Dictionary attack using a wordlist
- Brute-force attack using configurable charset and max length
- Password strength analysis with simple scoring and explanation

## Learning Purpose
This project is an educational password security lab.

It is designed to help learners:
- understand how hashing works
- see why weak passwords are risky
- compare attack techniques and defensive checks
- practice secure password thinking in a safe environment

## Project Structure
```text
hash-cracker-suite/
├── src/
│   ├── cracker.py
│   ├── cli/
│   │   ├── hash_mode.py
│   │   ├── dict_mode.py
│   │   ├── brute_mode.py
│   │   └── check_mode.py
│   └── core/
│       ├── hash_utils.py
│       ├── dictionary_attack.py
│       ├── brute_force.py
│       └── password_strength.py
├── data/
│   └── wordlists/
│       └── common.txt
├── tests/
│   ├── test_cli.py
│   ├── test_hash_utils.py
│   ├── test_dictionary_attack.py
│   ├── test_brute_force.py
│   └── test_password_strength.py
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── README.md
```

## CI Status
CI workflow is configured in `.github/workflows/ci.yml`.

## Installation
```bash
git clone https://github.com/urvalkheni/Hash-cracker-suite.git
cd Hash-cracker-suite

pip install -e .
hash-cracker --help
```

## Development Setup
```bash
git clone https://github.com/urvalkheni/Hash-cracker-suite.git
cd Hash-cracker-suite

pip install -r requirements-dev.txt
pytest
```

## Usage Examples

All examples below use the installed CLI entrypoint `hash-cracker`.

### 1) Hash generation and verification (`--mode hash`)
```bash
# Generate MD5 hash
hash-cracker hash --text password --algorithm md5

# Verify text against hash
hash-cracker hash --text password --hash 5f4dcc3b5aa765d61d8327deb882cf99 --algorithm md5
```

### 2) Dictionary attack (`--mode dict`)
```bash
hash-cracker dict --hash 5f4dcc3b5aa765d61d8327deb882cf99 --wordlist data/wordlists/common.txt --algorithm md5 --i-understand-legal-use

# Verbose progress every 500 attempts
hash-cracker dict --hash 5f4dcc3b5aa765d61d8327deb882cf99 --wordlist data/wordlists/common.txt --algorithm md5 --i-understand-legal-use --verbose --progress-interval 500
```

Use your own wordlist or place one in `data/wordlists/`.

### 3) Brute-force attack (`--mode brute`)
```bash
# Uses default charset (lowercase a-z) and max length 3
hash-cracker brute --hash 900150983cd24fb0d6963f7d28e17f72 --algorithm md5 --max-length 3 --i-understand-legal-use --force

# Custom charset example
hash-cracker brute --hash 187ef4436122d1cc2f40dc2b92f0eba0 --algorithm md5 --max-length 3 --charset abc123 --i-understand-legal-use --force

# Verbose progress every 100 attempts
hash-cracker brute --hash 900150983cd24fb0d6963f7d28e17f72 --algorithm md5 --max-length 3 --i-understand-legal-use --force --verbose --progress-interval 100
```

### 4) Password strength analysis (`--mode check`)
```bash
hash-cracker check --text password123
hash-cracker check --text Aq7!zP9@Lm#2
```

Note: This password strength checker is a simplified educational estimator, not a full real-world password audit tool.

## Demo
```bash
# Crack MD5 hash using dictionary
hash-cracker dict --hash 5f4dcc3b5aa765d61d8327deb882cf99 --wordlist data/wordlists/common.txt --algorithm md5 --i-understand-legal-use
```

## Safety Disclaimer
This project is for educational and authorized security testing only.

Do not run these techniques against systems, accounts, or data you do not own or have explicit permission to test.
