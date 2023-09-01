from Service.AccessService import AccessService
from Service.EncryptionService import EncryptionService
import os

class FileEncryptionService:
    encreptionFileType = ".enc"
    acceptedToEncrypteFileType = '.txt'

    def __init__(self):
        pass

    @staticmethod
    def encrypt_file(filePath, key):
        if not AccessService.validateCanAccessPath(filePath):
            raise Exception('CAN NOT ACCESS THIS PATH.')

        with open(filePath, 'rb') as fo:
            plaintext = fo.read()
        enc = EncryptionService.encrypt(plaintext, key)
        with open(filePath[:-4] + FileEncryptionService.encreptionFileType, 'wb') as fo:
            fo.write(enc)
        os.remove(filePath)

    @staticmethod
    def decrypt_file(filePath, key):
        if not AccessService.validateCanAccessPath(filePath):
            raise Exception('CAN NOT ACCESS THIS PATH.')

        dec = FileEncryptionService.decryptFileContent(filePath, key)
        with open(filePath[:-4] + FileEncryptionService.acceptedToEncrypteFileType, 'wb') as fo:
            fo.write(dec)
        os.remove(filePath)
        # user message
        print("File Decrypted Successfully")

    @staticmethod
    def decryptFileContent(filePath, key, decode = False):
        if not AccessService.validateCanAccessPath(filePath):
            raise Exception('CAN NOT ACCESS THIS PATH.')

        with open(filePath, 'rb') as fo:
            ciphertext = fo.read()
            dec = EncryptionService.decrypt(ciphertext, key)
            if decode:
                dec = dec.decode()
            return dec