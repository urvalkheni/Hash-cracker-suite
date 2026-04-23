import sys
from argparse import Namespace
from pathlib import Path

import pytest
import src.cracker as cracker
from src.cli import brute_mode, check_mode, dict_mode, hash_mode
from src.core.brute_force import BruteForceError, run_brute_force
from src.core.dictionary_attack import (
    DictionaryAttackError,
    run_dictionary_attack,
    validate_wordlist,
)
from src.core.hash_utils import get_algorithm_info, validate_hash_input, verify_hash
from src.core.password_strength import analyze_password_strength


def _write_wordlist(path: Path, lines: list[str]) -> None:
    path.write_bytes(b"\n".join(line.encode("utf-8") for line in lines) + b"\n")


def _run_main(monkeypatch: pytest.MonkeyPatch, *args: str) -> int:
    monkeypatch.setattr(sys, "argv", ["hash-cracker", *args])
    with pytest.raises(SystemExit) as excinfo:
        cracker.main()
    return excinfo.value.code


def test_create_parser_supports_all_modes() -> None:
    parser = cracker.create_parser()

    hash_args = parser.parse_args(["hash", "--text", "pw", "--algorithm", "md5"])
    assert hash_args.mode == "hash"
    assert hash_args.algorithm == "md5"

    dict_args = parser.parse_args(
        [
            "dict",
            "--hash",
            "5f4dcc3b5aa765d61d8327deb882cf99",
            "--wordlist",
            "data/wordlists/common.txt",
            "--i-understand-legal-use",
        ]
    )
    assert dict_args.mode == "dict"
    assert dict_args.progress_interval == 1000

    brute_args = parser.parse_args(
        [
            "brute",
            "--hash",
            "0cc175b9c0f1b6a831c399e269772661",
            "--i-understand-legal-use",
        ]
    )
    assert brute_args.mode == "brute"
    assert brute_args.max_length == 4

    check_args = parser.parse_args(["check", "--text", "password123"])
    assert check_args.mode == "check"


def test_main_hash_and_check_modes_exit_zero(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    assert _run_main(monkeypatch, "hash", "--text", "password", "--algorithm", "md5") == 0
    hash_output = capsys.readouterr().out
    assert "Generated Hash" in hash_output
    assert "cryptographically broken" in hash_output

    assert _run_main(monkeypatch, "check", "--text", "Aq7!zP9@Lm#2") == 0
    check_output = capsys.readouterr().out
    assert "Password Strength Analyzer" in check_output
    assert "Strength: Strong" in check_output


def test_main_dict_and_brute_modes_cover_success_and_parser_errors(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    wordlist = tmp_path / "words.txt"
    _write_wordlist(wordlist, ["not-it", "password", "admin"])

    assert (
        _run_main(
            monkeypatch,
            "dict",
            "--hash",
            "5f4dcc3b5aa765d61d8327deb882cf99",
            "--wordlist",
            str(wordlist),
            "--algorithm",
            "md5",
            "--i-understand-legal-use",
        )
        == 0
    )
    dict_output = capsys.readouterr().out
    assert "MATCH FOUND" in dict_output

    assert (
        _run_main(
            monkeypatch,
            "brute",
            "--hash",
            "0cc175b9c0f1b6a831c399e269772661",
            "--algorithm",
            "md5",
            "--max-length",
            "1",
            "--charset",
            "abc",
            "--verbose",
            "--progress-interval",
            "1",
            "--i-understand-legal-use",
            "--force",
        )
        == 0
    )
    brute_output = capsys.readouterr().out
    assert "Trying combinations" in brute_output
    assert "MATCH FOUND" in brute_output

    assert (
        _run_main(
            monkeypatch,
            "dict",
            "--hash",
            "5f4dcc3b5aa765d61d8327deb882cf99",
            "--wordlist",
            str(wordlist),
            "--progress-interval",
            "0",
            "--i-understand-legal-use",
        )
        == 2
    )
    err = capsys.readouterr().err
    assert "progress-interval" in err

    assert (
        _run_main(
            monkeypatch,
            "brute",
            "--hash",
            "5f4dcc3b5aa765d61d8327deb882cf99",
            "--max-length",
            "4",
            "--charset",
            "abcdefghijklmnopqrstuvwxyz",
        )
        == 2
    )
    err = capsys.readouterr().err
    assert "acknowledge authorized use" in err

    assert (
        _run_main(
            monkeypatch,
            "hash",
            "--text",
            "password",
            "--hash",
            "0" * 32,
            "--algorithm",
            "md5",
        )
        == 1
    )
    mismatch_output = capsys.readouterr().out
    assert "No match" in mismatch_output


def test_main_handles_keyboard_interrupt(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def _interrupt(_args: Namespace) -> bool:
        raise KeyboardInterrupt

    monkeypatch.setattr(cracker, "handle_hash_mode", _interrupt)
    assert _run_main(monkeypatch, "hash", "--text", "password") == 1
    assert "Operation cancelled by user" in capsys.readouterr().out


def test_hash_mode_handles_expected_and_unexpected_failures(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    missing_text_args = Namespace(text="", hash=None, algorithm="sha256")
    assert hash_mode.handle_hash_mode(missing_text_args) is False
    assert "--text is required" in capsys.readouterr().out

    invalid_hash_args = Namespace(text="password", hash="bad", algorithm="md5")
    assert hash_mode.handle_hash_mode(invalid_hash_args) is False
    assert "Invalid hash" in capsys.readouterr().out

    verify_args = Namespace(
        text="password",
        hash="00000000000000000000000000000000",
        algorithm="md5",
    )
    assert hash_mode.handle_hash_mode(verify_args) is False
    assert "No match" in capsys.readouterr().out

    match_args = Namespace(
        text="password",
        hash="5f4dcc3b5aa765d61d8327deb882cf99",
        algorithm="md5",
    )
    assert hash_mode.handle_hash_mode(match_args) is True
    assert "MATCH FOUND" in capsys.readouterr().out

    def _explode(_text: str, _algorithm: str) -> str:
        raise RuntimeError("boom")

    monkeypatch.setattr(hash_mode, "generate_hash", _explode)
    unexpected_args = Namespace(text="password", hash=None, algorithm="sha256")
    assert hash_mode.handle_hash_mode(unexpected_args) is False
    assert "Unexpected error: boom" in capsys.readouterr().out


def test_dict_mode_covers_validation_and_error_paths(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    wordlist = tmp_path / "words.txt"
    _write_wordlist(wordlist, ["password"])

    missing_hash_args = Namespace(
        hash="",
        wordlist=wordlist,
        algorithm="md5",
        verbose=False,
        progress_interval=1,
    )
    assert dict_mode.handle_dict_mode(missing_hash_args) is False
    assert "--hash is required" in capsys.readouterr().out

    missing_wordlist_args = Namespace(
        hash="5f4dcc3b5aa765d61d8327deb882cf99",
        wordlist=None,
        algorithm="md5",
        verbose=False,
        progress_interval=1,
    )
    assert dict_mode.handle_dict_mode(missing_wordlist_args) is False
    assert "--wordlist is required" in capsys.readouterr().out

    invalid_hash_args = Namespace(
        hash="bad",
        wordlist=wordlist,
        algorithm="md5",
        verbose=False,
        progress_interval=1,
    )
    assert dict_mode.handle_dict_mode(invalid_hash_args) is False
    assert "Invalid hash" in capsys.readouterr().out

    invalid_wordlist_args = Namespace(
        hash="5f4dcc3b5aa765d61d8327deb882cf99",
        wordlist=wordlist,
        algorithm="md5",
        verbose=False,
        progress_interval=1,
    )
    monkeypatch.setattr(dict_mode, "validate_wordlist", lambda _path: (False, "bad list"))
    assert dict_mode.handle_dict_mode(invalid_wordlist_args) is False
    assert "bad list" in capsys.readouterr().out

    monkeypatch.setattr(dict_mode, "validate_wordlist", lambda _path: (True, "Valid wordlist"))
    monkeypatch.setattr(dict_mode, "run_dictionary_attack", lambda **_kwargs: (False, None, 3))
    assert dict_mode.handle_dict_mode(invalid_wordlist_args) is False
    no_match_output = capsys.readouterr().out
    assert "No match found" in no_match_output

    monkeypatch.setattr(
        dict_mode,
        "run_dictionary_attack",
        lambda **_kwargs: (_ for _ in ()).throw(DictionaryAttackError("broken attack")),
    )
    assert dict_mode.handle_dict_mode(invalid_wordlist_args) is False
    assert "broken attack" in capsys.readouterr().out

    monkeypatch.setattr(
        dict_mode,
        "run_dictionary_attack",
        lambda **_kwargs: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    assert dict_mode.handle_dict_mode(invalid_wordlist_args) is False
    assert "Unexpected error: boom" in capsys.readouterr().out


def test_brute_mode_covers_validation_and_error_paths(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    base_args = Namespace(
        hash="5f4dcc3b5aa765d61d8327deb882cf99",
        algorithm="md5",
        max_length=2,
        charset="ab",
        verbose=False,
        progress_interval=1,
        force=True,
    )

    missing_hash_args = Namespace(**{**vars(base_args), "hash": ""})
    assert brute_mode.handle_brute_mode(missing_hash_args) is False
    assert "--hash is required" in capsys.readouterr().out

    short_length_args = Namespace(**{**vars(base_args), "max_length": 0})
    assert brute_mode.handle_brute_mode(short_length_args) is False
    assert "--max-length must be >= 1" in capsys.readouterr().out

    empty_charset_args = Namespace(**{**vars(base_args), "charset": ""})
    assert brute_mode.handle_brute_mode(empty_charset_args) is False
    assert "--charset must not be empty" in capsys.readouterr().out

    invalid_hash_args = Namespace(**{**vars(base_args), "hash": "bad"})
    assert brute_mode.handle_brute_mode(invalid_hash_args) is False
    assert "Invalid hash" in capsys.readouterr().out

    force_required_args = Namespace(
        **{
            **vars(base_args),
            "charset": "abcdefghijklmnopqrstuvwxyz",
            "max_length": 4,
            "force": False,
        }
    )
    assert brute_mode.handle_brute_mode(force_required_args) is False
    assert "Use --force to continue" in capsys.readouterr().out

    monkeypatch.setattr(brute_mode, "run_brute_force", lambda **_kwargs: (False, None, 6))
    assert brute_mode.handle_brute_mode(base_args) is False
    no_match_output = capsys.readouterr().out
    assert "No match found" in no_match_output

    monkeypatch.setattr(
        brute_mode,
        "run_brute_force",
        lambda **_kwargs: (_ for _ in ()).throw(BruteForceError("broken brute")),
    )
    assert brute_mode.handle_brute_mode(base_args) is False
    assert "broken brute" in capsys.readouterr().out

    monkeypatch.setattr(
        brute_mode,
        "run_brute_force",
        lambda **_kwargs: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    assert brute_mode.handle_brute_mode(base_args) is False
    assert "Unexpected error: boom" in capsys.readouterr().out


def test_check_mode_covers_error_paths(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    assert check_mode.handle_check_mode(Namespace(text="")) is False
    assert "--text is required" in capsys.readouterr().out

    monkeypatch.setattr(
        check_mode,
        "analyze_password_strength",
        lambda _password: (_ for _ in ()).throw(ValueError("invalid password")),
    )
    assert check_mode.handle_check_mode(Namespace(text="pw")) is False
    assert "invalid password" in capsys.readouterr().out

    monkeypatch.setattr(
        check_mode,
        "analyze_password_strength",
        lambda _password: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    assert check_mode.handle_check_mode(Namespace(text="pw")) is False
    assert "Unexpected error: boom" in capsys.readouterr().out


def test_core_edge_cases_cover_remaining_branches(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(ValueError):
        validate_hash_input("", "md5")

    assert validate_hash_input(" 5F4DCC3B5AA765D61D8327DEB882CF99 ", "md5") == (
        "5f4dcc3b5aa765d61d8327deb882cf99"
    )

    with pytest.raises(TypeError):
        hash_mode.generate_hash(123)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        verify_hash(123, "5f4dcc3b5aa765d61d8327deb882cf99", "md5")  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        verify_hash("password", 123, "md5")  # type: ignore[arg-type]

    info = get_algorithm_info()
    assert set(info) == {"md5", "sha1", "sha256"}

    with pytest.raises(BruteForceError):
        run_brute_force("", algorithm="md5")

    with pytest.raises(BruteForceError):
        run_brute_force("5f4dcc3b5aa765d61d8327deb882cf99", algorithm="md5", progress_interval=0)

    found, password, attempts = run_brute_force(
        "0cc175b9c0f1b6a831c399e269772661",
        algorithm="md5",
        charset="abc",
        max_length=1,
        show_progress=True,
        progress_interval=1,
    )
    assert (found, password, attempts) == (True, "a", 1)
    assert "Attempts: 1" in capsys.readouterr().out

    with pytest.raises(BruteForceError, match="Unsupported algorithm"):
        run_brute_force(
            "5f4dcc3b5aa765d61d8327deb882cf99", algorithm="md2", charset="ab", max_length=1
        )

    def _raise_bruteforce_error(_target_hash: str, _algorithm: str) -> str:
        raise BruteForceError("passthrough")

    monkeypatch.setattr("src.core.brute_force.validate_hash_input", _raise_bruteforce_error)
    with pytest.raises(BruteForceError, match="passthrough"):
        run_brute_force(
            "5f4dcc3b5aa765d61d8327deb882cf99", algorithm="md5", charset="ab", max_length=1
        )

    monkeypatch.setattr(
        "src.core.brute_force.generate_hash",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    with pytest.raises(BruteForceError, match="Error during brute-force attack: boom"):
        run_brute_force(
            "5f4dcc3b5aa765d61d8327deb882cf99", algorithm="md5", charset="ab", max_length=1
        )

    wordlist = tmp_path / "mixed.txt"
    wordlist.write_bytes(b"skip-me-\xff\n\npassword\n")
    found, password, attempts = run_dictionary_attack(
        "5f4dcc3b5aa765d61d8327deb882cf99",
        wordlist,
        algorithm="md5",
        show_progress=True,
        progress_interval=1,
    )
    assert (found, password, attempts) == (True, "password", 1)
    dict_output = capsys.readouterr().out
    assert "Skipped 1 non-UTF-8 lines" in dict_output

    with pytest.raises(DictionaryAttackError):
        run_dictionary_attack("", wordlist, algorithm="md5")

    with pytest.raises(DictionaryAttackError):
        run_dictionary_attack(
            "5f4dcc3b5aa765d61d8327deb882cf99", wordlist, algorithm="md5", progress_interval=0
        )

    monkeypatch.setattr(
        "src.core.dictionary_attack.validate_hash_input",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(DictionaryAttackError("passthrough")),
    )
    with pytest.raises(DictionaryAttackError, match="passthrough"):
        run_dictionary_attack("5f4dcc3b5aa765d61d8327deb882cf99", wordlist, algorithm="md5")

    from src.core.hash_utils import UnsupportedAlgorithmError

    monkeypatch.setattr(
        "src.core.dictionary_attack.generate_hash",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(UnsupportedAlgorithmError("bad algorithm")),
    )
    with pytest.raises(DictionaryAttackError, match="Invalid algorithm"):
        run_dictionary_attack("5f4dcc3b5aa765d61d8327deb882cf99", wordlist, algorithm="md5")

    monkeypatch.setattr(
        "src.core.dictionary_attack.validate_hash_input",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    with pytest.raises(DictionaryAttackError, match="Error during dictionary attack: boom"):
        run_dictionary_attack("5f4dcc3b5aa765d61d8327deb882cf99", wordlist, algorithm="md5")

    directory = tmp_path / "folder"
    directory.mkdir()
    assert validate_wordlist(directory) == (False, f"Not a file: {directory}")

    assert validate_wordlist(tmp_path / "missing.txt")[0] is False

    noisy_wordlist = tmp_path / "noisy.txt"
    noisy_wordlist.write_bytes(b"alpha\n\xff\nbeta\n")
    is_valid, message = validate_wordlist(noisy_wordlist)
    assert is_valid is True
    assert "1 lines skipped" in message

    monkeypatch.setattr(
        Path, "open", lambda self, *_args, **_kwargs: (_ for _ in ()).throw(OSError("denied"))
    )
    assert validate_wordlist(noisy_wordlist) == (False, "Error reading file: denied")

    result = analyze_password_strength("abc")
    assert result["strength"] == "Weak"
    assert "too short" in result["reason"]
    assert "no digits" in result["reason"]
