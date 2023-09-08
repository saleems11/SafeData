import gc

from AppConsts.Consts import Consts
from Authentication.AuthenticationService import AuthenticationService
from Service.FileEncryptionService import FileEncryptionService
from Service.FileManagement import FileManagement


class MainPasswordManager:

    def __init__(self, authenticationService:AuthenticationService, defaultDir=Consts.SavedPasswordDirPath):
        self._authenticationService = authenticationService
        self._defaultDir = defaultDir
        self.initSavedPasswordDir()

    def addPassword(self, serviceName, password):
        'Throw exception'
        fileFullPath = ''

        try:
            fileFullPath = FileManagement.createFilePath(serviceName, self._defaultDir)
            FileManagement.WriteInFile(fileFullPath, password)

            key = self._authenticationService.getPassowrdKey()
            FileEncryptionService.create_encrypted_file(fileFullPath, key)
        except Exception:
            FileManagement.deleteFile(fileFullPath)
            raise

        # Clean-up
        password = None
        key = None
        collected = gc.collect()

    def getPassword(self, serviceName):
        'Throw exception'
        fileFullPath = FileManagement.createFilePath(serviceName, self._defaultDir, FileManagement.Encreption)
        if not FileManagement.isFileExist(fileFullPath):
            raise Exception(f'No matching passwrod for this service found :{serviceName}.')

        key = self._authenticationService.getPassowrdKey()
        decFilePath = FileEncryptionService.create_decrypted_file(fileFullPath, key)
        decPassword = FileManagement.readFile(decFilePath)

        # Clean-up
        password = None
        key = None
        collected = gc.collect()

        return decPassword

    def initSavedPasswordDir(self):
        FileManagement.CreateDir(self._defaultDir)