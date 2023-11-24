import gc

from AppConfig.IConfiguration import IConfiguration
from PasswordManager.FileEncryptionManager import FileEncryptionManager
from Service.FileManagement import FileManagement


class MainPasswordManager:

    def __init__(self,
                 fileEncryptionManager:FileEncryptionManager,
                 configuration:IConfiguration):
        self._fileEncryptionManager = fileEncryptionManager
        self._defaultDir = configuration.SavedPasswordDirPath
        self.initSavedPasswordDir()

    def addPassword(self, serviceName, password):
        'Throw exception'
        fileFullPath = ''

        try:
            fileFullPath = FileManagement.createFilePath(serviceName, self._defaultDir)
            FileManagement.WriteInFile(fileFullPath, password)
        except FileExistsError as ex:
            raise
        except Exception:
            FileManagement.deleteFile(fileFullPath)
            raise

        # encrypt the File
        try:
            self._fileEncryptionManager.encryptFile(fileFullPath)
        except Exception:
            FileManagement.deleteFile(fileFullPath)
            raise

        # Clean-up
        password = None
        key = None
        collected = gc.collect()

    def getPassword(self, serviceName):
        'Throw exception'
        fileFullPath = FileManagement.createFilePath(serviceName, self._defaultDir, FileManagement.Encryption)
        if not FileManagement.DoesPathExist(fileFullPath):
            raise Exception(f'No matching passwrod for this service found :{serviceName}.')

        decPassword = self._fileEncryptionManager.read_encrypted_file(fileFullPath)

        # Clean-up
        key = None
        collected = gc.collect()

        return decPassword

    def initSavedPasswordDir(self):
        FileManagement.CreateDir(self._defaultDir)