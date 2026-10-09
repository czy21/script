import base64
import hashlib

import bcrypt


def encrypt(value: str, mode: str = "base64") -> str:
    value_bytes = value.encode("utf-8")
    if mode == "base64":
        return base64.b64encode(value_bytes).decode("ascii")
    if mode == "md5":
        return hashlib.md5(value_bytes).hexdigest()
    return value


def decrypt(value: str, mode: str = "base64") -> str:
    if mode == "base64":
        return base64.b64decode(value, validate=True).decode("utf-8")
    return value


def htpasswd(value: str) -> str:
    return bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("ascii")
