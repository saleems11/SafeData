from Exceptions.DecryptionException import DecryptionException
from Service.AccessService import AccessService
from Service.EncryptionService import EncryptionService
import os

from Service.FileManagement import FileManagement


class FileEncryptionService:

    def __init__(self, accessService: AccessService):
        self._accessService = accessService

    def create_encrypted_file(self, encFilePath, data, key:bytes):
        # need to add path validation
        enc = EncryptionService.encrypt(data, key)
        FileManagement.WriteInFile(encFilePath, enc, inBytes=True)

    def encrypted_file(self, filePath:str, key:bytes, delete=True) -> str:
        self.fileValidation(filePath)
        FileManagement.ValidAbleToEncrypt(filePath)

        plaintext = FileManagement.readFile(filePath, asbytes=False)
        enc = EncryptionService.encrypt(plaintext, key)

        encFilePath = FileManagement.ChangeFileType(filePath, FileManagement.Encryption)
        FileManagement.WriteInFile(encFilePath, enc, inBytes=True)

        if delete:
            os.remove(filePath)

        # Clean-up
        plaintext = None

        return encFilePath


    def create_decrypted_file(self, filePath, key:bytes, delete=True) -> str:
        dec = self.decryptFileContent(filePath, key)
        decFilePath = FileManagement.ChangeFileType(filePath, FileManagement.Txt)

        try:
            FileManagement.WriteInFile(decFilePath, dec)
        except FileExistsError as ex:
            os.remove(decFilePath)
            raise ex

        if delete:
            os.remove(filePath)

        # Clean-up
        dec = None

        return decFilePath


    def fileValidation(self, filePath):
        FileManagement.DoesPathExist(filePath, True)
        self._accessService.tryAccessPath(filePath)


    def decryptFileContent(self, filePath, key:bytes):
        self.fileValidation(filePath)
        FileManagement.ValidAbleToDecrypt(filePath)

        try:
            with open(filePath, 'rb') as fo:
                ciphertext = fo.read()
                dec = EncryptionService.decrypt(ciphertext, key)
                return dec
        except Exception as ex:
            raise DecryptionException(ex, ex)