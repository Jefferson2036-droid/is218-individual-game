"""Password hashing (scrypt, from Python's standard library) and login tokens (JWT)."""

import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

import jwt

SCRYPT_N = 2 ** 14
SCRYPT_R = 8
SCRYPT_P = 1
ALGORITHM = "HS256"


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _scrypt(password: str, salt: bytes, n: int, r: int, p: int) -> bytes:
    return hashlib.scrypt(password.encode("utf-8"), salt=salt, n=n, r=r, p=p, dklen=32)


def hash_password(password: str) -> str:
    """Returns "scrypt$N$r$p$salt$hash". Never store the password itself."""
    salt = secrets.token_bytes(16)
    digest = _scrypt(password, salt, SCRYPT_N, SCRYPT_R, SCRYPT_P)
    return "scrypt$%d$%d$%d$%s$%s" % (SCRYPT_N, SCRYPT_R, SCRYPT_P, _b64(salt), _b64(digest))


def verify_password(password: str, stored: str) -> bool:
    try:
        scheme, n, r, p, salt, digest = stored.split("$")
        if scheme != "scrypt":
            return False
        expected = base64.b64decode(digest)
        actual = _scrypt(password, base64.b64decode(salt), int(n), int(r), int(p))
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(actual, expected)


def create_token(user_id: int, secret: str, minutes: int) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    return jwt.encode({"sub": str(user_id), "exp": expires}, secret, algorithm=ALGORITHM)


def read_token(token: str, secret: str):
    """The user id in a valid, unexpired token, otherwise None."""
    try:
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError, TypeError):
        return None
