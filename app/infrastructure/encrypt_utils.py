import bcrypt


def encrypt_str(to_encrypt: str):
    return bcrypt.hashpw(to_encrypt.encode("utf-8"), bcrypt.gensalt())


def check_encrypted_str(original: str, encrypted: str):
    return bcrypt.checkpw(original.encode("utf-8"), encrypted)
