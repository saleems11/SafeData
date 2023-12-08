from AppConfig.Consts import Consts
from Authentication.Model.SavedMfaKeyModel import SavedMfaKeyModel
from Model.LogInReturnStatus import LogInReturnStatus
from Model.Status import Status
from Service.MfaService import MfaService


class MfaManagerService:
    MfaDecreptionSuccessCodeMessage = 'MfaDecreptionSuccessCodeMessage'

    def __init__(self):
        self._mfaManager = None
        self.loginSucceded = False

    def logIn(self, mfa, email, mfaKeyDecrebtedKey) -> LogInReturnStatus:
        mfaKey = MfaService.getMfaKeyFromMfaKeyDecrebtedKey(mfaKeyDecrebtedKey, email)
        if mfaKey == None:
            self.handleInvalidLogin(mfa)

        self._mfaManager = MfaService(key=mfaKey)

        if self._mfaManager.Validate(mfa):
            self.loginSucceded = True
            return LogInReturnStatus(Status.Succed, "User Succeded to LogIn")

        return self.handleInvalidLogin(mfa)

    def logOut(self):
        self.loginSucceded = False
        self._mfaManager = None

    def handleInvalidLogin(self, mfa):
        self.logOut()
        return LogInReturnStatus(Status.InvalidMfaAuth, f"Failed to Authnticate with 2FA, you'r input was {mfa}.")

    def validate(self, mfaToValidate) -> LogInReturnStatus:
        succeded = self._mfaManager.Validate(mfaToValidate)
        if not succeded:
            return LogInReturnStatus(Status.InvalidMfaAuth, f"Failed to validate Pin, you'r input was {mfaToValidate}.")
        return LogInReturnStatus(Status.Succed, "Mfa key is Valid.")

    def CreateRegistrationQR(self, accountName):
        self._mfaManager = MfaService()
        self._mfaManager.GenerateQrCode(accountName)


    def IsMfaActive(self):
        return self._mfaManager is not None and self.loginSucceded

    def createMfaKeyPlussValidationMessage(self, email):
        mfaKeyMessageStr = self.buildMfaKey(self._mfaManager.getKeyAndDeleteIt(), email)
        return mfaKeyMessageStr

    @staticmethod
    def buildMfaKey(key, email):
        return SavedMfaKeyModel(key, email).serializeJson()