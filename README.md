# Hash Cracker Suite
Educational Python CLI for hashing, authorized password-cracking demonstrations, and rule-based password strength checks.

## 🚀 Overview
Hash Cracker Suite is a command-line project built to help learners understand how password-related security workflows behave in practice.

It includes four main workflows:
- Generate a hash from text.
- Verify whether text matches a target hash.
- Attempt hash recovery with a dictionary wordlist.
- Attempt hash recovery with brute-force combinations.
- Check password strength using a simple scoring model.

Why this project exists:
- To turn common security concepts into hands-on terminal exercises.
- To show how weak passwords can be discovered with basic attack techniques.
- To pair offensive concepts (cracking demos) with defensive thinking (password quality checks).

Where it is useful in real life:
- Cybersecurity education and classroom labs.
- Developer awareness training.
- Local experiments for understanding hash-based credential risk.

## Features
Only implemented features are listed below.

- Multi-algorithm hashing and verification.
Supports `md5`, `sha1`, and `sha256` for generating and verifying hashes.

- Hash format validation.
Validates that target hashes are hexadecimal and match the exact length for the chosen algorithm.

- Dictionary attack mode.
Reads a wordlist file, hashes each candidate, and compares against the target hash.

- Wordlist validation and robust file handling.
Checks file existence/type, counts valid words, skips non-UTF-8 lines, and reports skipped lines as warnings.

- Brute-force mode with configurable search space.
Generates all combinations from length `1` to `max-length` using a custom `charset`.

- Safety controls for expensive brute-force runs.
Estimates total combinations and requires `--force` for large search spaces.

- Progress reporting in attack modes.
Optional `--verbose` + `--progress-interval` output for dictionary and brute-force runs.

- Legal-use acknowledgement gate.
Requires `--i-understand-legal-use` before running attack modes.

- Password strength analyzer.
Returns score (`0..5`), strength label (`Weak`/`Medium`/`Strong`), character-type checks, a common-pattern penalty, and estimated entropy bits.

- Clear warnings for weak legacy hash algorithms.
Shows warnings when `md5` or `sha1` are selected.

- Automated tests and CI.
Pytest-based tests for core modules and CLI behavior, executed in GitHub Actions CI.

## 🛠 Tech Stack
- Language: Python (project requires `>=3.10`)
- CLI framework: standard library `argparse`
- Hashing: standard library `hashlib`
- Brute-force generation: standard library `itertools`
- Utilities: `pathlib`, `math`, `typing`
- Packaging/build: `setuptools` via `pyproject.toml`
- Testing: `pytest`
- CI: GitHub Actions

## 📂 Project Structure
```text
Hash-cracker-suite/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   └── wordlists/
│       └── common.txt
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
├── tests/
│   ├── test_cli.py
│   ├── test_hash_utils.py
│   ├── test_dictionary_attack.py
│   ├── test_brute_force.py
│   └── test_password_strength.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

Folder guide for beginners:
- `.github/workflows/`: CI pipeline that installs dependencies and runs tests on push/PR.
- `data/wordlists/`: Sample wordlist used for dictionary attack demos.
- `src/cracker.py`: Main CLI entrypoint and argument parser.
- `src/cli/`: Mode-specific command handlers that print user-facing results.
- `src/core/`: Core cracking/hash/strength logic used by the CLI.
- `tests/`: Unit and integration-style CLI tests using pytest.
- `pyproject.toml`: Project metadata, package config, and `hash-cracker` command entrypoint.

## ⚙️ Setup & Installation

### Quick Start (copy-paste)
```bash
git clone https://github.com/urvalkheni/Hash-cracker-suite.git
cd Hash-cracker-suite
python -m pip install --upgrade pip
pip install -e .
hash-cracker --help
```

What each step does:
1. `git clone ...`: Downloads the project to your machine.
2. `cd Hash-cracker-suite`: Moves into the project folder.
3. `python -m pip install --upgrade pip`: Updates pip to a recent version.
4. `pip install -e .`: Installs this project in editable mode and creates the `hash-cracker` command.
5. `hash-cracker --help`: Shows available modes and flags.

If your shell does not expose script entrypoints, run via module:
```bash
python -m src.cracker --help
```

For development/testing setup:
```bash
pip install -r requirements-dev.txt
pytest
```

## 🧪 Usage Examples

### 1) Generate a hash
```bash
hash-cracker hash --text password --algorithm md5
```
Creates an MD5 hash for the input text.

### 2) Verify text against a target hash
```bash
hash-cracker hash --text password --hash 5f4dcc3b5aa765d61d8327deb882cf99 --algorithm md5
```
Generates a hash from `--text`, compares it with `--hash`, and reports match/no-match.

### 3) Dictionary attack (authorized use only)
```bash
hash-cracker dict --hash 5f4dcc3b5aa765d61d8327deb882cf99 --wordlist data/wordlists/common.txt --algorithm md5 --i-understand-legal-use
```
Tries each word in the wordlist until a match is found or the list ends.

### 4) Brute-force attack (authorized use only)
```bash
hash-cracker brute --hash 900150983cd24fb0d6963f7d28e17f72 --algorithm md5 --max-length 3 --i-understand-legal-use --force
```
Tests every combination (length `1..3`) from the default lowercase charset.

### 5) Password strength check
```bash
hash-cracker check --text Aq7!zP9@Lm#2
```
Returns score, strength label, entropy estimate, and rule-based reasoning.

## 📊 Example Output

Example: hash verification
```text
============================================================
Hash Cracker Suite - Hash Utility
============================================================

[!] WARNING: MD5/SHA1 are cryptographically broken and should not be used in real systems.
[+] Text: password
[+] Algorithm: MD5
[+] Generated Hash: 5f4dcc3b5aa765d61d8327deb882cf99

[*] Verification:
[*] Target Hash: 5f4dcc3b5aa765d61d8327deb882cf99
[*] Generated Hash: 5f4dcc3b5aa765d61d8327deb882cf99
[+] MATCH FOUND! Password is: password
```

Example: password strength check
```text
============================================================
Hash Cracker Suite - Password Strength Analyzer
============================================================

Password: password123
Strength: Weak
Score: 2/5
Entropy (estimated): 71.45 bits
Reason: missing mixed case, no special characters, common pattern
Note: This is an educational estimate only.
```

## 🧠 How It Works
Simple flow used across modes:

1. Input
User chooses a mode (`hash`, `dict`, `brute`, `check`) and provides command arguments.

2. Validation
The CLI validates required flags, hash format/length, and legal-use acknowledgement for attack modes.

3. Processing
- `hash`: generate hash and optionally verify.
- `dict`: iterate wordlist and compare candidate hashes.
- `brute`: generate charset combinations and compare hashes.
- `check`: apply scoring rules and estimate entropy.

4. Output
Mode handler prints result summary, attempts (for attack modes), and success/failure status.

## 🔐 Limitations / Notes
- This is an educational CLI, not a production password auditing platform.
- Supported algorithms are only `md5`, `sha1`, and `sha256`.
- Attack modes require the correct algorithm and a valid hash format.
- Dictionary mode depends on wordlist quality and encoding (non-UTF-8 lines are skipped).
- Brute-force becomes expensive quickly; large search spaces require explicit `--force`.
- Password strength scoring is rule-based and simplified; it is not a full security assessment.
- No GPU acceleration, distributed cracking, or advanced hash schemes (for example `bcrypt`/`argon2`) are implemented.

## 🎯 Learning Outcomes
This project demonstrates practical skills in:
- Python CLI application design with `argparse`.
- Hashing and hash verification workflows.
- Dictionary and brute-force cracking mechanics.
- Input validation and safe-by-default CLI controls.
- Modular architecture (`cli` handlers vs `core` logic).
- Automated testing with pytest and CI pipeline setup.

## 🚀 Future Improvements
- Add modern password hash support (for example `bcrypt` or `argon2`) for defensive learning use-cases.
- Add optional benchmark mode to measure attempts/second.
- Add exportable result logs (JSON/CSV) for lab reporting.

## ⚠️ Disclaimer
Use this project only for education and authorized security testing.

Do not run dictionary or brute-force modes against systems, credentials, or data unless you have explicit permission.
