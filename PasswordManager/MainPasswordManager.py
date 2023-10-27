import gc

from AppConfig.Configuration import Configuration
from Authentication.AuthenticationService import AuthenticationService
from Service.FileEncryptionService import FileEncryptionService
from Service.FileManagement import FileManagement


class MainPasswordManager:

    def __init__(self,
                 authenticationService:AuthenticationService,
                 fileEncryptionService:FileEncryptionService,
                 configuration:Configuration):
        self._authenticationService = authenticationService
        self._fileEncryptionService = fileEncryptionService
        self._defaultDir = configuration.SavedPasswordDirPath
        self.initSavedPasswordDir()

    def addPassword(self, serviceName, password):
        'Throw exception'
        fileFullPath = ''

        try:
            fileFullPath = FileManagement.createFilePath(serviceName, self._defaultDir)
            FileManagement.WriteInFile(fileFullPath, password)

            key = self._authenticationService.getPassowrdKey()
            self._fileEncryptionService.create_encrypted_file(fileFullPath, key)
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
        if not FileManagement.DoesPathExist(fileFullPath):
            raise Exception(f'No matching passwrod for this service found :{serviceName}.')

        key = self._authenticationService.getPassowrdKey()
        decPassword = self._fileEncryptionService.read_encrypted_file(fileFullPath, key)

        # Clean-up
        key = None
        collected = gc.collect()

        return decPassword

    def initSavedPasswordDir(self):
        FileManagement.CreateDir(self._defaultDir)