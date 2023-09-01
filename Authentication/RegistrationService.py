import os

from Authentication.MfaManagerService import MfaManagerService
from Model.LogInReturnStatus import LogInReturnStatus
from Model.Status import Status
from Service.AccessService import AccessService
from Service.EncryptionService import EncryptionService
from Service.FileEncryptionService import FileEncryptionService
from Service.PasswordService import PasswordService


class RegistrationService:

    UserRegistrationFileNameForMfa = 'secureMfa'
    UserRegistrationFolderForMfa = 'MfaRegistration'

    registartionFileNameAndType = f'{UserRegistrationFileNameForMfa}{FileEncryptionService.encreptionFileType}'
    registartionFolderPath = os.path.join(AccessService.CanEncrypteUnder, UserRegistrationFolderForMfa)
    registartionFilePath = os.path.join(registartionFolderPath, registartionFileNameAndType)

    def __init__(self,
                 passwordService:PasswordService,
                 encryptionService:EncryptionService,
                 mfaManagerService:MfaManagerService):
        self._passwordService = passwordService
        self._encryptionService = encryptionService
        self._mfaManagerService = mfaManagerService

    def register(self, password):
        try:
            self.__CreateRegitrationSaveLocationIfNotExist()
            self.SaveRegistrationData(password)
            return LogInReturnStatus(Status.Succed, 'Registartion Succeded.')

        except Exception as ex:
            os.remove(self.registartionFilePath)
            print(ex)
            return LogInReturnStatus(Status.ExceptionOccured, 'Registartion Failed.')

    def SaveRegistrationData(self, password):
        with open(self.registartionFilePath, "wb") as secMfaF:
            mfaKeyWithValidationMessageBytes = self._mfaManagerService.createMfaKeyPlussValidationMessageInBytes()

            key = self._passwordService.HashifyPassword(password)
            securedMfaKey = self._encryptionService.encrypt(mfaKeyWithValidationMessageBytes, key)

            secMfaF.write(securedMfaKey)

    def __CreateRegitrationSaveLocationIfNotExist(self):
        if not os.path.exists(self.registartionFolderPath):
            os.mkdir(self.registartionFolderPath)