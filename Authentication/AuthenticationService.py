from Authentication.MfaManagerService import MfaManagerService
from Authentication.RegistrationService import RegistrationService
from Exceptions.AuthenticationException import AuthenticationException
from Exceptions.DecryptionException import DecryptionException
from Model.LogInReturnStatus import LogInReturnStatus
from Model.PasswordLogInReturnStatus import PasswordLogInReturnStatus
from Model.Status import Status
from Service.FileEncryptionService import FileEncryptionService
from Service.PasswordService import PasswordService


class AuthenticationService:

    def __init__(self,
                 mfaManagerService:MfaManagerService,
                 registrationService:RegistrationService,
                 fileEncryptionService:FileEncryptionService):
        self._mfaManagerService = mfaManagerService
        self._registrationService = registrationService
        self._fileEncryptionService = fileEncryptionService
        self.mfaManager = None
        self.gpassword = None
        self.gpasswordKey = None

    def isAuthnticated(self) -> bool:
        return self._mfaManagerService.IsMfaActive() and self.gpasswordKey is not None

    def login(self, password, mfa) -> LogInReturnStatus:
        passwordKey = PasswordService.HashifyPassword(password)
        logInReult = self.__tryLogin(passwordKey)

        if not logInReult.IsSucceded():
            return LogInReturnStatus(logInReult.status, logInReult.message)

        mfaKeyDecrebtedKey = logInReult.MfaKey
        mfaLoginResult = self._mfaManagerService.logIn(mfa, mfaKeyDecrebtedKey)

        if mfaLoginResult.IsSucceded():
            hashedMfaKey = PasswordService.HashifyPassword(mfaKeyDecrebtedKey)
            self.gpasswordKey = hashedMfaKey

        mfaKeyDecrebtedKey = None
        password = None

        return mfaLoginResult


    def __tryLogin(self, passwordKey) -> PasswordLogInReturnStatus:
        try:
            mfaKeyDecrebtedKey = self._fileEncryptionService.decryptFileContent(
                self._registrationService.registartionFilePath,
                passwordKey,
                True
            )
            return PasswordLogInReturnStatus(Status.Succed, f"User password is correct", mfaKeyDecrebtedKey)
        except DecryptionException as ex:
            if isinstance(ex.innerEx, UnicodeDecodeError):
                return PasswordLogInReturnStatus(Status.InvalidPassword, f"User Failed To Login", ex)


    def getPassowrdKey(self):
        if not self.isAuthnticated():
            raise AuthenticationException('Not Authenticated')
        return self.gpasswordKey

    def __setPassword(self, password):
        self.gpassword = password