import os

from AppConsts.Consts import Consts
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
    registartionFolderPath = os.path.join(Consts.SavedPasswordDirPath, UserRegistrationFolderForMfa)
    registartionFilePath = os.path.join(registartionFolderPath, registartionFileNameAndType)

    def __init__(self,
                 passwordService:PasswordService,
                 encryptionService:EncryptionService,
                 mfaManagerService:MfaManagerService):
        self._passwordService = passwordService
        self._encryptionService = encryptionService
        self._mfaManagerService = mfaManagerService
        self.__CreateRegitrationSaveLocationIfNotExist()

    def register(self, password):
        try:
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