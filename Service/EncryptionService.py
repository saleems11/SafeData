from Crypto import Random
from Crypto.Cipher import AES

from AppConfig.Consts import Consts
from Service.GibberishService import GibberishService


class EncryptionService:
    # AES modes:
    # https://onboardbase.com/blog/aes-encryption-decryption/
    def __init__(self):
        pass

    @staticmethod
    def encrypt(message:str, key, key_size=256):
        # add Gibberish Part
        gibberishData = GibberishService.addGibberishToData(message)
        gibberishDataInBytes = bytes(gibberishData, Consts.encoding)

        # Encrypt Part
        gibberishDataInBytes = EncryptionService.pad(gibberishDataInBytes)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(gibberishDataInBytes)

    @staticmethod
    def encyptV2(message:str, key):
        # encryption based on the Key size
        # add Gibberish Part
        # will not be used, but it is here in case needed
        # code based on(not by the best practices, it was intended to be used for testing):
        # https://asecuritysite.com/encryption/aes_gcm#:~:text=AES%20GCM%20(Galois%20Counter%20Mode,it%20does%20not%20require%20padding.
        gibberishData = GibberishService.addGibberishToData(message)
        gibberishDataInBytes = bytes(gibberishData, Consts.encoding)

        # add IV
        encobj = AES.new(key, AES.MODE_GCM)
        ciphertext, authTag = encobj.encrypt_and_digest(gibberishDataInBytes)
        return (ciphertext, authTag, encobj.nonce)

    @staticmethod
    def decrypt(ciphertext, key):
        # Decryption Part
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])

        # Clean up part
        textWithoutBytes = plaintext.rstrip(b"\0")
        decodedTextStr = textWithoutBytes.decode(Consts.encoding)
        cleanplaintextDec = GibberishService.removeGibberishFromData(decodedTextStr)

        return cleanplaintextDec

    @staticmethod
    def decryptV2(ciphertext, key):
        (ciphertext, authTag, nonce) = ciphertext
        encobj = AES.new(key, AES.MODE_GCM, nonce)
        decryptedData = (encobj.decrypt_and_verify(ciphertext, authTag))

        # Clean up part
        textWithoutBytes = decryptedData.rstrip(b"\0")
        decodedTextStr = textWithoutBytes.decode(Consts.encoding)
        cleanplaintextDec = GibberishService.removeGibberishFromData(decodedTextStr)

        return cleanplaintextDec

    @staticmethod
    def pad(s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)