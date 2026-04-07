# 🔑 Hash Cracker Suite

A comprehensive password security and hash cracking toolkit designed to demonstrate real-world attack techniques such as dictionary attacks, brute-force attacks, and rainbow table lookups.

This project helps understand how weak passwords are exploited and how modern systems defend against such attacks.

---

## 📌 Overview

Passwords are rarely stored in plaintext. Instead, systems store **hashes** — one-way cryptographic representations of passwords.

However, weak passwords and poor hashing practices make systems vulnerable.

This toolkit simulates how attackers:

* Crack hashes using wordlists
* Perform brute-force attacks
* Use rainbow tables for fast lookup

---

## 🚀 Features

* 🔓 Crack MD5, SHA-1, SHA-256 hashes
* 📚 Dictionary attack using wordlists (e.g., rockyou.txt)
* 💪 Brute-force password generation
* 🌈 Rainbow table simulation (precomputed hashes)
* 🔐 Password strength checker
* ⚡ CLI-based fast execution

---

## 🛠 Tech Stack

* **Language:** Python
* **Libraries:** hashlib, itertools, argparse

---

## 📂 Project Structure

hash-cracker-suite/
│── core/
│   ├── hash_utils.py
│   ├── dictionary_attack.py
│   ├── brute_force.py
│   ├── rainbow_table.py
│
│── data/
│   ├── wordlists/
│   │   ├── sample.txt
│   │   ├── rockyou.txt (optional)
│   │
│   ├── rainbow_tables/
│       ├── md5_table.json
│
│── tools/
│   ├── password_strength.py
│
│── cracker.py
│── README.md

---

## 🔍 Core Modules

### 1. Dictionary Attack

Attempts to match a given hash with words from a predefined list.

```bash id="g2y6nr"
python cracker.py --mode dict --hash <hash> --wordlist data/wordlists/sample.txt
```

✔ Fast
✔ Effective against weak passwords

---

### 2. Brute Force Attack

Generates all possible combinations within a character set.

```bash id="e7l4dn"
python cracker.py --mode brute --hash <hash> --length 4
```

✔ Works even without wordlists
❌ Slow for long passwords

---

### 3. Rainbow Table Lookup

Uses precomputed hashes for instant lookup.

```bash id="g0zj7n"
python cracker.py --mode rainbow --hash <hash>
```

✔ Extremely fast
❌ Requires storage

---

### 4. Password Strength Checker

Evaluates password strength based on:

* Length
* Complexity
* Entropy estimation

```bash id="5a2q8m"
python tools/password_strength.py
```

---

## 🔐 Supported Hash Types

* MD5
* SHA-1
* SHA-256

Example hash:

```id="kz1q6p"
5f4dcc3b5aa765d61d8327deb882cf99
```

Cracked password:

```id="1pjc5x"
password
```

---

## 🧪 Usage

### Basic Command

```bash id="r3f9wt"
python cracker.py --mode dict --hash <hash> --wordlist <path>
```

### Full Example

```bash id="r2n8va"
python cracker.py --mode dict --hash 5f4dcc3b5aa765d61d8327deb882cf99 --wordlist data/wordlists/sample.txt
```

---

## ⚙️ How It Works

1. Convert input word → hash
2. Compare generated hash with target
3. If match found → password cracked

---

## 📊 Sample Output

```id="vl7q9x"
[+] Target Hash: 5f4dcc3b5aa765d61d8327deb882cf99
[+] Mode: Dictionary Attack
[+] Match Found: password
```

---

## 🔐 Security Insights

This project demonstrates why:

* ❌ Weak passwords are dangerous
* ❌ Fast hashing (MD5) is insecure
* ❌ Lack of salting enables rainbow attacks

---

## 🛡️ Prevention Techniques

* ✅ Use strong passwords
* ✅ Apply salting
* ✅ Use slow hashing algorithms (bcrypt, scrypt, Argon2)
* ✅ Implement rate limiting

---

## ⚠️ Disclaimer

This tool is for **educational and ethical use only**.

Do NOT use it on systems without proper authorization.

---

## 🎯 Learning Outcomes

After using this toolkit, you will:

* Understand how hashes work
* Learn multiple cracking techniques
* Analyze password strength
* Understand real-world attack scenarios

---

## 🚀 Future Improvements

* GPU acceleration (hashcat-style)
* Support for bcrypt / Argon2
* GUI dashboard
* Distributed cracking

---

## 🤝 Contributing

Contributions are welcome!

* Add new attack modules
* Improve performance
* Expand hash support

---

## ⭐ Acknowledgment

Inspired by real-world password cracking tools and security research.
