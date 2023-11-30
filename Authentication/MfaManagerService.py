from AppConfig.Consts import Consts
from Model.LogInReturnStatus import LogInReturnStatus
from Model.Status import Status
from Service.MfaService import MfaService


class MfaManagerService:
    MfaDecreptionSuccessCodeMessage = 'MfaDecreptionSuccessCodeMessage'

    def __init__(self):
        self._mfaManager = None
        self.loginSucceded = False

    def logIn(self, mfa, emailOrUserName, mfaKeyDecrebtedKey) -> LogInReturnStatus:
        mfaKey = MfaService.getMfaKeyFromMfaKeyDecrebtedKey(mfaKeyDecrebtedKey, emailOrUserName)
        if mfaKey == None:
            self.handleInvalidLogin()

        self._mfaManager = MfaService(key=mfaKey)

        if self._mfaManager.Validate(mfa):
            self.loginSucceded = True
            return LogInReturnStatus(Status.Succed, "User Succeded to LogIn")

        return self.handleInvalidLogin()

    def handleInvalidLogin(self):
        self.loginSucceded = False
        self._mfaManager = None
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
        mfaKeyMessageStr = f'{self._mfaManager.getKeyAndDeleteIt()}{Consts.EMAIL_PART_IN_MFA_REG}{email}'
        return mfaKeyMessageStr