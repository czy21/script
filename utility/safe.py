import base64

import bcrypt


def decrypt(value: str, mode: str = "base64"):
    if mode == "base64":
        return base64.b64decode(value).rstrip().decode("utf-8")
    return value


def htpasswd(value: str):
    return bcrypt.hashpw(value.encode(), bcrypt.gensalt(rounds=12)).decode()