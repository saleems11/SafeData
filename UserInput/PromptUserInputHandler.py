from Model.LogInReturnStatus import LogInReturnStatus
from Service.FileManagement import FileManagement
from UserInput.BasePromptUserInputHandler import BasePromptUserInputHandler
import re


class PromptUserInputHandler(BasePromptUserInputHandler):

    def __getValidFilePath(self, msg, errorMsg="This is invalid Path."):
        while True:
            filePath = self.getUserInput(msg)
            if FileManagement.DoesPathExist(filePath):
                break
            print(errorMsg)

        return filePath

    def getAllowEncDecUnderPath(self) -> str:
        msg = "Please Enter where you to be able to encrypt you'r file\n"\
              "(Please Note that Encryption/Decryption will be applied under you'r selected Path):"

        return self.__getValidFilePath(msg)

    def getSavedPasswordsFileLocation(self) -> str:
        msg = "Please Enter where you want to save you'r password\n"\
              "(Please Note that Encrypted and Decrypted files will stay in the same location):"

        return self.__getValidFilePath(msg)

    def getInputPassword(self) -> str:
        password = self.getUserInput("Please Enter the password:")
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

    def getValidEmail(self) -> str:
        email_format: str = r"(^[a-zA-Z0-9'_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        validEmail = self.getUserInput('Please Enter your Email:')

        while not re.match(email_format, validEmail, re.IGNORECASE):
            validEmail = self.getUserInput('Invalid EmailAddress, Please Enter your Email again:')

        return validEmail

    # def getEmail(self) -> str:
    #     email = self.getUserInput('Please Enter your Email:')
    #     return email


    def getWebSiteServiceName(self) -> str:
        WebSiteServiceName = self.getUserInput('Please Enter Website/Service Name:')
        return WebSiteServiceName

    def getFilePath(self, toMsg='') -> str:
        to = '' if len(toMsg) == 0 else f' to {toMsg}'
        filePath = self.getUserInput(f'Please Enter File path{to}:')
        return filePath

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