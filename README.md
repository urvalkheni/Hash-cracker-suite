# Hash Cracker Suite
Command-line password security lab for hashing workflows, controlled cracking demonstrations, and fast strength estimation.

## 🚀 Overview
Hash Cracker Suite is a modular Python CLI that demonstrates core password security workflows end to end:

- create and verify hashes
- attempt recovery using dictionary and brute-force strategies
- evaluate password quality with a rule-based strength score

Why it exists:

- to make password security concepts practical and testable from the terminal
- to show how weak credentials are exposed by basic attack techniques
- to pair offensive testing concepts with defensive password quality checks

Real-world relevance:

- cybersecurity training and awareness labs
- secure software education for developers
- repeatable local experiments for understanding hash-based credential risk

## 🔥 Features
- Multi-algorithm hash generation and verification: `md5`, `sha1`, `sha256`.
- Hash input validation with strict hexadecimal and algorithm-specific length checks.
- Dictionary attack mode with:
	- wordlist validation
	- UTF-8 line processing
	- non-UTF-8 line skipping with warning output
	- optional progress output (`--verbose`, `--progress-interval`)
- Brute-force mode with:
	- configurable charset and max length
	- full combinatorial candidate generation (length `1..N`)
	- optional progress output (`--verbose`, `--progress-interval`)
	- search-space estimate and explicit `--force` requirement for large runs
- Safety gate for attack modes requiring explicit legal-use acknowledgment:
	- `--i-understand-legal-use`
- Password strength analyzer with:
	- rule-based score (`0..5`)
	- checks for length, mixed case, digits, special characters
	- common-pattern penalty (`password`, `123456`, `qwerty`, `admin`)
	- estimated entropy in bits
- Warning output when using insecure legacy hashes (`md5`, `sha1`).
- Test suite with `pytest` and automated CI on GitHub Actions.

## 🛠 Tech Stack
- Language: Python 3.10+
- CLI: Python `argparse`
- Cryptography primitives: Python standard-library `hashlib`
- Candidate generation: Python standard-library `itertools`
- Packaging: `setuptools`, PEP 517/518 (`pyproject.toml`)
- Testing: `pytest`
- CI: GitHub Actions

## 📂 Project Structure
```text
Hash-cracker-suite/
├── .github/
│   └── workflows/
│       └── ci.yml                  # CI pipeline: install deps, install package, run pytest
├── data/
│   └── wordlists/
│       └── common.txt              # Sample dictionary words for attack demonstrations
├── src/
│   ├── __init__.py                 # Package metadata
│   ├── cracker.py                  # Main CLI entrypoint and argument parsing
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── hash_mode.py            # Hash mode output + validation + verify flow
│   │   ├── dict_mode.py            # Dictionary mode orchestration and reporting
│   │   ├── brute_mode.py           # Brute-force mode orchestration + safety checks
│   │   └── check_mode.py           # Password strength mode output
│   └── core/
│       ├── __init__.py
│       ├── hash_utils.py           # Hash generation/verification + format validation
│       ├── dictionary_attack.py    # Wordlist-driven hash cracking engine
│       ├── brute_force.py          # Exhaustive candidate generation and matching
│       └── password_strength.py    # Rule-based strength scoring + entropy estimate
├── tests/
│   ├── conftest.py                 # Test import-path setup
│   ├── test_cli.py                 # End-to-end CLI behavior tests
│   ├── test_hash_utils.py          # Hash module unit tests
│   ├── test_dictionary_attack.py   # Dictionary attack tests
│   ├── test_brute_force.py         # Brute-force tests
│   └── test_password_strength.py   # Password analysis tests
├── pyproject.toml                  # Project metadata, script entrypoint, build config
├── requirements.txt                # Runtime dependencies (standard library only)
├── requirements-dev.txt            # Dev dependencies (pytest)
└── README.md
```

## ⚙️ Setup & Installation

### 1) Clone
```bash
git clone https://github.com/urvalkheni/Hash-cracker-suite.git
cd Hash-cracker-suite
```

### 2) Install (recommended)
```bash
python -m pip install --upgrade pip
pip install -e .
```

### 3) Run CLI
```bash
hash-cracker --help
```

If script entrypoints are unavailable in your shell, run via module:

```bash
python -m src.cracker --help
```

## ▶️ Usage

### Hash generation and verification
```bash
hash-cracker hash --text password --algorithm md5
hash-cracker hash --text password --hash 5f4dcc3b5aa765d61d8327deb882cf99 --algorithm md5
```

### Dictionary attack
```bash
hash-cracker dict \
	--hash 5f4dcc3b5aa765d61d8327deb882cf99 \
	--wordlist data/wordlists/common.txt \
	--algorithm md5 \
	--i-understand-legal-use
```

Verbose progress example:

```bash
hash-cracker dict \
	--hash 5f4dcc3b5aa765d61d8327deb882cf99 \
	--wordlist data/wordlists/common.txt \
	--algorithm md5 \
	--i-understand-legal-use \
	--verbose \
	--progress-interval 500
```

### Brute-force attack
```bash
hash-cracker brute \
	--hash 900150983cd24fb0d6963f7d28e17f72 \
	--algorithm md5 \
	--max-length 3 \
	--i-understand-legal-use \
	--force
```

Custom charset example:

```bash
hash-cracker brute \
	--hash 187ef4436122d1cc2f40dc2b92f0eba0 \
	--algorithm md5 \
	--max-length 3 \
	--charset abc123 \
	--i-understand-legal-use \
	--force
```

### Password strength check
```bash
hash-cracker check --text password123
hash-cracker check --text Aq7!zP9@Lm#2
```

## 🧪 Development & Testing
```bash
pip install -r requirements-dev.txt
pytest
```

CI runs test automation from [.github/workflows/ci.yml](.github/workflows/ci.yml).

## ⚠️ Responsible Use
This project is intended for education and authorized security testing only.

Use attack modes only on systems and data you own or are explicitly permitted to assess.
