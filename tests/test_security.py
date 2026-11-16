from app.security import create_token, hash_password, read_token, verify_password

SECRET = "test-secret-key-that-is-long-enough-for-hs256-0123456789"


def test_password_round_trip():
    stored = hash_password("correct horse battery")
    assert stored.startswith("scrypt$")
    assert "correct horse battery" not in stored
    assert verify_password("correct horse battery", stored)
    assert not verify_password("wrong password", stored)


def test_same_password_hashes_differently_each_time():
    assert hash_password("same-password") != hash_password("same-password")


def test_garbage_hashes_never_verify():
    for stored in ("", "plain-text", "scrypt$1$2", "bcrypt$a$b$c$d$e", "scrypt$x$8$1$AAAA$AAAA"):
        assert not verify_password("anything", stored)


def test_token_round_trip():
    token = create_token(42, SECRET, minutes=5)
    assert read_token(token, SECRET) == 42


def test_bad_tokens_are_rejected():
    token = create_token(42, SECRET, minutes=5)
    assert read_token(token, "another-secret-key-that-is-also-long-enough-987654321") is None
    assert read_token(token + "x", SECRET) is None
    assert read_token("not-a-token", SECRET) is None
    assert read_token(create_token(42, SECRET, minutes=-1), SECRET) is None   # expired
