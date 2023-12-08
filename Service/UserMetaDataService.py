from AppConfig.Consts import Consts
from AppConfig.IConfiguration import IConfiguration
from PasswordManager.FileEncryptionManager import FileEncryptionManager
from Service.FileManagement import FileManagement
from Service.Model.UserMetaData import UserMetaData

import os

class UserMetaDataService:

    def __init__(self,
                 fileEncryptionManager:FileEncryptionManager,
                 configuration:IConfiguration):
        self._fileEncryptionManager = fileEncryptionManager
        self._configuration = configuration

    def ReadUserMetaData(self, userMetaData:UserMetaData) -> UserMetaData:
        filePath = self.GetFilePath(userMetaData)
        FileManagement.DoesPathExist(filePath, raiseException=True)
        fileContent = self._fileEncryptionManager.read_encrypted_file(filePath)
        return UserMetaData.deserilizeJson(fileContent)

    def WriteUserMetaData(self, userMetaData:UserMetaData):
        # write assumes that the enc file doesn't exist
        filePath = self.GetFilePath(userMetaData)
        FileManagement.WriteInFileWithErrorHandling(filePath, userMetaData.serializeJson(), newFile=False, overiteFile=True)
        self._fileEncryptionManager.encryptFile(filePath)

    def UpdateUserMetaData(self, userMetaData:UserMetaData):
        # change fileName then create new file then delte it
        pass

    def CreateUserMetaDataFolder(self):
        dirPath = self.GetMetaDataDirPath()
        FileManagement.CreateDir(dirPath)

    def GetFilePath(self, userMetaData:UserMetaData) -> str:
        dirPath = self.GetMetaDataDirPath()
        filePath = FileManagement.createFilePath(userMetaData.getUniqueId(), dirPath)
        return filePath

    def GetMetaDataDirPath(self) -> str:
        folderName = Consts.UserMetaDataFolderName
        savedPasswordsDirPath = self._configuration.GetValueOrDefault(Consts._Saved_Password_Dir_Path)
        return os.path.join(savedPasswordsDirPath, folderName)