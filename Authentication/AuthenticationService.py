from Authentication.MfaManagerService import MfaManagerService
from Authentication.RegistrationService import RegistrationService
from Model.LogInReturnStatus import LogInReturnStatus
from Model.PasswordLogInReturnStatus import PasswordLogInReturnStatus
from Model.Status import Status
from Service.FileEncryptionService import FileEncryptionService
from Service.PasswordService import PasswordService


class AuthenticationService:

    def __init__(self, mfaManagerService:MfaManagerService):
        self._mfaManagerService = mfaManagerService
        self.mfaManager = None
        self.gpassword = None

    def isAuthnticated(self) -> bool:
        return self._mfaManagerService.IsMfaActive() and self.getPassowrd() is not None

    def login(self, password, mfa) -> LogInReturnStatus:
        passwordKey = PasswordService.HashifyPassword(password)
        logInReult = self.__tryLogin(passwordKey)
        passwordKey = None

        if not logInReult.IsSucceded():
            return LogInReturnStatus(logInReult.status, logInReult.message)

        mfaKeyDecrebtedKey = logInReult.MfaKey
        mfaLoginResult = self._mfaManagerService.logIn(mfa, mfaKeyDecrebtedKey)
        mfaKeyDecrebtedKey = None

        if mfaLoginResult.IsSucceded():
            self.__setPassword(password)
        return mfaLoginResult


    def __tryLogin(self, passwordKey) -> PasswordLogInReturnStatus:
        try:
            mfaKeyDecrebtedKey = FileEncryptionService.decryptFileContent(
                RegistrationService.registartionFilePath,
                passwordKey,
                True
            )
            return PasswordLogInReturnStatus(Status.Succed, f"User password is correct", mfaKeyDecrebtedKey)
        except UnicodeDecodeError as ex:
            return PasswordLogInReturnStatus(Status.InvalidPassword, f"User Failed To Login.", ex)


    def getPassowrd(self):
        pass

    def __setPassword(self, password):
        self.gpassword = password