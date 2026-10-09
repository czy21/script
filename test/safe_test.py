from util import safe as safe_util

base64_encrypt = safe_util.encrypt("abc", mode="base64")
print(f'base64_encrypt: {base64_encrypt}')
base64_decrypt = safe_util.decrypt(base64_encrypt, "base64")
print(f'base64_decrypt: {base64_decrypt}')

md5_encrypt = safe_util.encrypt("def", "md5")
print(f'md5_encrypt: {md5_encrypt}')

htpasswd = safe_util.htpasswd("hello")
print(f'htpasswd: {htpasswd}')