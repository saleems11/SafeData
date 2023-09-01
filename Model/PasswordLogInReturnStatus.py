from Model.LogInReturnStatus import LogInReturnStatus
from Model.Status import Status


class PasswordLogInReturnStatus(LogInReturnStatus):

    def __init__(self, status:Status, message, mfaKey):
        super().__init__(status, message)
        self.MfaKey = mfaKey