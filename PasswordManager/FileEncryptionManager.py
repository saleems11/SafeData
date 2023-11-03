import gc

from Authentication.AuthenticationService import AuthenticationService
from Service.FileEncryptionService import FileEncryptionService

class FileEncryptionManager:

    def __init__(self, authenticationService:AuthenticationService, fileEncryptionService:FileEncryptionService):
        self._authenticationService = authenticationService
        self._fileEncryptionService = fileEncryptionService

    def encryptFile(self, filePath):
        key = self._authenticationService.getPassowrdKey()
        self._fileEncryptionService.encrypted_file(filePath, key)

        # Clean-up
        key = None
        collected = gc.collect()

    def decryptFile(self, filePath):
        key = self._authenticationService.getPassowrdKey()
        self._fileEncryptionService.create_decrypted_file(filePath, key)

        # Clean-up
        key = None
        collected = gc.collect()

    def read_encrypted_file(self, filePath) -> str:
        key = self._authenticationService.getPassowrdKey()
        dec = self._fileEncryptionService.decryptFileContent(filePath, key)
        return dec