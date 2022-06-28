import bcrypt

if __name__ == '__main__':
    hashed = bcrypt.hashpw(b"hhhhh", bcrypt.gensalt(rounds=12))
    print(hashed)
