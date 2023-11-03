from AppConfig.Consts import Consts
from Exceptions.DecryptionException import DecryptionException
from Service.AccessService import AccessService
from Service.EncryptionService import EncryptionService
import os

from Service.FileManagement import FileManagement


class FileEncryptionService:

    def __init__(self, accessService: AccessService):
        self._accessService = accessService


    def create_encrypted_file(self, filePath, key, delete=True) -> str:
        self.fileValidation(filePath)

        plaintext = FileManagement.readFile(filePath)
        enc = EncryptionService.encrypt(plaintext, key)

        encFilePath = FileManagement.ChangeFileType(filePath, FileManagement.Encreption)
        FileManagement.WriteInFile(encFilePath, enc, inBytes=True)

        if delete:
            os.remove(filePath)

        # Clean-up
        plaintext = None

        return encFilePath


    def read_encrypted_file(self, filePath, key) -> str:
        self.fileValidation(filePath)

        dec = self.decryptFileContent(filePath, key, True)
        return dec


    def create_decrypted_file(self, filePath, key, delete=True) -> str:
        self.fileValidation(filePath)

        dec = self.decryptFileContent(filePath, key, True)
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


    def decryptFileContent(self, filePath, key, decode = False):
        self._accessService.tryAccessPath(filePath)

        try:
            with open(filePath, 'rb') as fo:
                ciphertext = fo.read()
                dec = EncryptionService.decrypt(ciphertext, key)
                if decode:
                    dec = dec.decode(Consts.encoding)
                return dec
        except Exception as ex:
            raise DecryptionException(ex, ex)