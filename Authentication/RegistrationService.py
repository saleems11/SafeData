import os

from AppConfig.Configuration import Configuration
from AppConfig.Consts import Consts
from Authentication.MfaManagerService import MfaManagerService
from Model.LogInReturnStatus import LogInReturnStatus
from Model.Status import Status
from Service.EncryptionService import EncryptionService
from Service.FileEncryptionService import FileEncryptionService
from Service.FileManagement import FileManagement
from Service.PasswordService import PasswordService


class RegistrationService:

    UserRegistrationFileNameForMfa = 'secureMfa'
    UserRegistrationFolderForMfa = 'MfaRegistration'

    registartionFileNameAndType = f'{UserRegistrationFileNameForMfa}.{FileManagement.Encryption}'

    def __init__(self,
                 passwordService:PasswordService,
                 fileEncryptionService:FileEncryptionService,
                 mfaManagerService:MfaManagerService,
                 configuration:Configuration):
        self._passwordService = passwordService
        self._fileEncryptionService = fileEncryptionService
        self._mfaManagerService = mfaManagerService

        self.registartionFolderPath = os.path.join(configuration.SavedPasswordDirPath, RegistrationService.UserRegistrationFolderForMfa)
        self.registartionFilePath = os.path.join(self.registartionFolderPath, RegistrationService.registartionFileNameAndType)

    def register(self, password):
        try:
            self.__CreateRegitrationSaveLocationIfNotExist()

            self.SaveRegistrationData(password)
            return LogInReturnStatus(Status.Succed, 'Registartion Succeded.')

        except Exception as ex:
            print(ex)
            return LogInReturnStatus(Status.ExceptionOccured, 'Registartion Failed.')

    def SaveRegistrationData(self, password):
        mfaKeyWithValidationMessage = self._mfaManagerService.createMfaKeyPlussValidationMessage()
        key = self._passwordService.HashifyPassword(password)
        self._fileEncryptionService.create_encrypted_file(self.registartionFilePath, mfaKeyWithValidationMessage, key)


    def __CreateRegitrationSaveLocationIfNotExist(self):
        FileManagement.CreateDir(self.registartionFolderPath)