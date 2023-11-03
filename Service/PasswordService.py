import hashlib

class PasswordService:

    def __init__(self):
        pass

    @staticmethod
    def HashifyPassword(password, keySizeInBytes=32) -> bytes:
        if isinstance(password, bytes):
            #  already hashified
            return password
        hash_object = hashlib.sha256(password.encode())
        key = hash_object.hexdigest()[:keySizeInBytes]
        return key.encode()
