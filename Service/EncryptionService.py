from Crypto import Random
from Crypto.Cipher import AES

class EncryptionService:

    def __init__(self):
        pass

    @staticmethod
    def encrypt(message, key, key_size=256):
        message = EncryptionService.pad(message)
        iv = Random.new().read(AES.block_size)
        # print('iv: ', iv)
        # print('key', key)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    @staticmethod
    def decrypt(ciphertext, key):
        iv = ciphertext[:AES.block_size]
        # print('iv: ', iv)
        # print('key', key)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    @staticmethod
    def pad(s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)