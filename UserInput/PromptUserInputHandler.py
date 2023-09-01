from Model.LogInReturnStatus import LogInReturnStatus
from UserInput.BasePromptUserInputHandler import BasePromptUserInputHandler


class PromptUserInputHandler(BasePromptUserInputHandler):

    def getInputPassword(self) -> str:
        password = self.getUserInput("Please Enter your password:")
        return password

    def getValidPassword(self) -> str:
        while True:
            password = self.getUserInput("Please Enter the password (Must be longer than 4 charcters):")
            if len(password) <= 4:
                print("Please Select a longer password.")
                continue

            rePassword = self.getUserInput("Please Re-Enter the password To validate the process:")
            if password != rePassword:
                print("The Process of Encreption Failed, Because the password didn't match.")
                continue
            else:
                break
        print(f'The Passwords matched, you Entered: {password}, Password Length: {len(password)}.')
        return password

    def getValidMfaInputLogIn(self) -> str:
        mfaKey = self.getUserInput("Please Enter your Mfa Key(It will be required only Once):")
        return mfaKey

    def getAccountMfaName(self) -> str:
        accountName = None
        while accountName is None or len(accountName) == 0:
            if accountName is not None:
                print("Invalid Account Name, Please try Again:")
            accountName = self.getUserInput('Please Enter Account Name:')
        return accountName

    def HandleLoginResult(self, loginResult:LogInReturnStatus):
        print(f"{loginResult.message}, status:{loginResult.status}")

    def HandleMfaLoginResult(self, mfaResult:LogInReturnStatus, remainingRetries:int = -1):
        shouldPrintRemainingReties = remainingRetries != -1
        remainingRetriesMsg = f'remaining retries:{remainingRetries}, ' if shouldPrintRemainingReties else ''
        print(f"{mfaResult.message}, {remainingRetriesMsg}status:{mfaResult.status}")

    def HandleregistrationResult(self, registrationResult:LogInReturnStatus):
        print(f"{registrationResult.message}, status:{registrationResult.status}")

    def Exit(self, textOnly=False):
        print("GoodBye, see you later")
        if not textOnly:
            exit(0)