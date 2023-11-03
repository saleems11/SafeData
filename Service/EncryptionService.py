from Crypto import Random
from Crypto.Cipher import AES

from AppConfig.Consts import Consts
from Service.GibberishService import GibberishService


class EncryptionService:

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
    def pad(s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)