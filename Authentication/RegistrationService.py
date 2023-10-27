import os

from AppConfig.Configuration import Configuration
from AppConfig.Consts import Consts
from Authentication.MfaManagerService import MfaManagerService
from Model.LogInReturnStatus import LogInReturnStatus
from Model.Status import Status
from Service.EncryptionService import EncryptionService
from Service.FileManagement import FileManagement
from Service.PasswordService import PasswordService


class RegistrationService:

    UserRegistrationFileNameForMfa = 'secureMfa'
    UserRegistrationFolderForMfa = 'MfaRegistration'

    registartionFileNameAndType = f'{UserRegistrationFileNameForMfa}{FileManagement.Encreption}'

    def __init__(self,
                 passwordService:PasswordService,
                 encryptionService:EncryptionService,
                 mfaManagerService:MfaManagerService,
                 configuration:Configuration):
        self._passwordService = passwordService
        self._encryptionService = encryptionService
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
        with open(self.registartionFilePath, "wb") as secMfaF:
            mfaKeyWithValidationMessageBytes = self._mfaManagerService.createMfaKeyPlussValidationMessageInBytes()

            key = self._passwordService.HashifyPassword(password)
            securedMfaKey = self._encryptionService.encrypt(mfaKeyWithValidationMessageBytes, key)

            secMfaF.write(securedMfaKey)

    def __CreateRegitrationSaveLocationIfNotExist(self):
        FileManagement.CreateDir(self.registartionFolderPath)