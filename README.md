# 🔑 Hash Cracker Suite

A comprehensive password security and hash cracking toolkit designed to demonstrate real-world attack techniques such as dictionary attacks, brute-force attacks, and rainbow table lookups.

## 📌 Overview

This project helps understand how weak passwords are exploited and how modern systems defend against such attacks.

## 🚀 Features (Planned)

- 🔓 Crack MD5, SHA-1, SHA-256 hashes
- 📚 Dictionary attack using wordlists
- 💪 Brute-force password generation
- 🌈 Rainbow table simulation (precomputed hashes)
- 🔐 Password strength checker
- ⚡ CLI-based fast execution

## 🛠 Tech Stack

- **Language:** Python 3.8+
- **Libraries:** hashlib, itertools, argparse (standard library)

## 📂 Project Structure

```
hash-cracker-suite/
├── src/
│   ├── core/              # Core attack modules (Phase 2)
│   └── cracker.py         # Main CLI entry point
├── data/
│   ├── wordlists/         # Wordlist data files
│   └── rainbow_tables/    # Precomputed hash tables
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/urvalkheni/Hash-cracker-suite.git
cd Hash-cracker-suite

# No external dependencies required (using Python standard library)
# Optional: Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## 🚀 Quick Start

```bash
# Show help
python src/cracker.py --help

# Dictionary attack (coming in Phase 2)
python src/cracker.py --mode dict --hash <hash> --wordlist data/wordlists/sample.txt

# Brute force (coming in Phase 2)
python src/cracker.py --mode brute --hash <hash> --length 4

# Rainbow table (coming in Phase 2)
python src/cracker.py --mode rainbow --hash <hash>
```

## 📊 Development Phases

### Phase 1 ✅ (Current)
- [x] Project structure
- [x] CLI argument parsing
- [x] Base setup

### Phase 2 (Next)
- [ ] Hash utility functions
- [ ] Dictionary attack implementation
- [ ] Brute-force implementation
- [ ] Rainbow table simulation

### Phase 3+
- [ ] Performance optimizations
- [ ] Additional hash algorithms
- [ ] GUI dashboard
- [ ] GPU acceleration

## ⚠️ Disclaimer

This tool is for **educational and ethical use only**.

Do NOT use it on systems without proper authorization.

## 🤝 Contributing

Contributions welcome! Focus areas:
- Implement core attack modules
- Add new hash algorithm support
- Performance optimizations
- Documentation

## 📝 License

See LICENSE file for details.
