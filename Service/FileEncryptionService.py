from Service.AccessService import AccessService
from Service.EncryptionService import EncryptionService
import os

from Service.FileManagement import FileManagement


class FileEncryptionService:

    def __init__(self):
        pass

    @staticmethod
    def create_encrypted_file(filePath, key, delete=True) -> str:
        AccessService.tryAccessPath(filePath)

        plaintext = FileManagement.readFile(filePath)
        enc = EncryptionService.encrypt(plaintext, key)

        encFilePath = FileManagement.ChangeFileType(filePath, FileManagement.Encreption)
        FileManagement.WriteInFile(encFilePath, enc, inBytes=True)

        if delete:
            os.remove(filePath)

        # Clean-up
        plaintext = None

        return encFilePath

    @staticmethod
    def create_decrypted_file(filePath, key, delete=True) -> str:
        AccessService.tryAccessPath(filePath)

        dec = FileEncryptionService.decryptFileContent(filePath, key)

        decFilePath = FileManagement.ChangeFileType(filePath, FileManagement.Txt)
        FileManagement.WriteInFile(decFilePath, dec)

        if delete:
            os.remove(filePath)

        # Clean-up
        dec = None

        return decFilePath

    @staticmethod
    def decryptFileContent(filePath, key, decode = False):
        AccessService.tryAccessPath(filePath)

        with open(filePath, 'rb') as fo:
            ciphertext = fo.read()
            dec = EncryptionService.decrypt(ciphertext, key)
            if decode:
                dec = dec.decode()
            return dec