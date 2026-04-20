from pathlib import Path

import pytest
from src.core.dictionary_attack import (
    DictionaryAttackError,
    run_dictionary_attack,
    validate_wordlist,
)


def _write_wordlist(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_dictionary_attack_found_md5(tmp_path: Path):
    wordlist = tmp_path / "words.txt"
    _write_wordlist(wordlist, ["notpassword", "password", "admin"])

    found, password, attempts = run_dictionary_attack(
        target_hash="5f4dcc3b5aa765d61d8327deb882cf99",
        wordlist_path=wordlist,
        algorithm="md5",
    )

    assert found is True
    assert password == "password"
    assert attempts == 2


def test_dictionary_attack_not_found(tmp_path: Path):
    wordlist = tmp_path / "words.txt"
    _write_wordlist(wordlist, ["one", "two", "three"])

    found, password, attempts = run_dictionary_attack(
        target_hash="5f4dcc3b5aa765d61d8327deb882cf99",
        wordlist_path=wordlist,
        algorithm="md5",
    )

    assert found is False
    assert password is None
    assert attempts == 3


def test_dictionary_attack_missing_file_raises():
    with pytest.raises(DictionaryAttackError):
        run_dictionary_attack(
            target_hash="5f4dcc3b5aa765d61d8327deb882cf99",
            wordlist_path=Path("missing.txt"),
            algorithm="md5",
        )


def test_dictionary_attack_rejects_invalid_hash(tmp_path: Path):
    wordlist = tmp_path / "words.txt"
    _write_wordlist(wordlist, ["password"])

    with pytest.raises(DictionaryAttackError):
        run_dictionary_attack(
            target_hash="not_hex_hash",
            wordlist_path=wordlist,
            algorithm="md5",
        )


def test_validate_wordlist_empty(tmp_path: Path):
    wordlist = tmp_path / "empty.txt"
    wordlist.write_text("", encoding="utf-8")
    is_valid, message = validate_wordlist(wordlist)
    assert is_valid is False
    assert "empty" in message.lower()


def test_validate_wordlist_valid(tmp_path: Path):
    wordlist = tmp_path / "words.txt"
    _write_wordlist(wordlist, ["a", "b", "c"])
    is_valid, message = validate_wordlist(wordlist)
    assert is_valid is True
    assert "3 words" in message
