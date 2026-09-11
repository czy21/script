import base64
import bcrypt
import hashlib


def decrypt(value: str, mode: str = "base64"):
    if mode == "base64":
        return base64.b64decode(value).rstrip().decode("utf-8")
    return value


def htpasswd(value: str):
    return bcrypt.hashpw(value.encode(), bcrypt.gensalt(rounds=12)).decode()


def md5_encrypt(text: str) -> str:
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()
