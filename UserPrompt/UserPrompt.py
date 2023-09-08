from AppConsts.Consts import Consts
from Authentication.AuthenticationService import AuthenticationService
from Authentication.MfaManagerService import MfaManagerService
from Authentication.RegistrationService import RegistrationService
from Model.LogInReturnStatus import LogInReturnStatus
from Model.Status import Status
from PasswordManager.MainPasswordManager import MainPasswordManager
from Service.EncryptionService import EncryptionService
from Service.PasswordService import PasswordService
from UserInput.BasePromptUserInputHandler import BasePromptUserInputHandler
from UserInput.PromptUserInputHandler import PromptUserInputHandler

import cmd
import sys


class UserPrompt(cmd.Cmd):
    # There is no specific resone why it is 7
    MaxMfaRetry = 7

    intro = BasePromptUserInputHandler.getInstructionMessgae()
    prompt = f'({Consts.APP_NAME}) '

    def __init__(self,
                 userPromptHandler:PromptUserInputHandler,
                 authenticationService:AuthenticationService,
                 mfaManagerService:MfaManagerService,
                 registrationService:RegistrationService,
                 mainPasswordManager:MainPasswordManager):
        super().__init__()
        self._userPromptHandler = userPromptHandler
        self._authenticationService = authenticationService
        self._mfaManagerService = mfaManagerService
        self._registrationService = registrationService
        self._mainPasswordManager = mainPasswordManager

    def __GetPassword(self, encrypt=False):
        if self._authenticationService.isAuthnticated():
            return self._authenticationService.getPassowrd()
        if encrypt:
            return self._userPromptHandler.getValidPassword()
        return self._userPromptHandler.getInputPassword()

    def __ValidateMfa(self):
        mfaValidationResult = None
        for remainigRetires in range(self.MaxMfaRetry - 1, -1, -1):
            mfaKey = self._userPromptHandler.getValidMfaInputLogIn()
            mfaValidationResult = self._mfaManagerService.validate(mfaKey)

            if mfaValidationResult.IsSucceded():
                break

            self._userPromptHandler.HandleMfaLoginResult(mfaValidationResult, remainigRetires)

            mfaValidationResult = None

        return mfaValidationResult if mfaValidationResult is not None \
                   else LogInReturnStatus(Status.RegistrationFailedToManyAttemps, "Registration Failed.")

    def do_login(self, arg):
        'Login to your account, requires password and Mfa(your should be already registered)'
        # Add later locking mechanisem
        password = self.__GetPassword()
        mfaKey = self._userPromptHandler.getValidMfaInputLogIn()

        loginResult = self._authenticationService.login(password, mfaKey)
        self._userPromptHandler.HandleLoginResult(loginResult)

    def do_register(self, arg):
        'Register your account so you can encrypte and decrepte Data'
        accountName = self._userPromptHandler.getAccountMfaName()
        self._mfaManagerService.CreateRegistrationQR(accountName)

        mfaValidationResult = self.__ValidateMfa()
        self._userPromptHandler.HandleregistrationResult(mfaValidationResult)
        if not mfaValidationResult.IsSucceded():
            return

        password = self.__GetPassword(True)
        registrationResult = self._registrationService.register(password)
        self._userPromptHandler.HandleregistrationResult(registrationResult)

    def do_addPassword(self, arg):
        'Add New Password'
        accountName = self._userPromptHandler.getWebSiteServiceName()
        password = self._userPromptHandler.getInputPassword()

        self._mainPasswordManager.addPassword(accountName, password)

        # Clean-up
        password = None

    def do_getPassword(self, arg):
        'Get Saved Password'
        accountName = self._userPromptHandler.getWebSiteServiceName()

        savedPass = self._mainPasswordManager.getPassword(accountName)

        # Clean-up
        password = None
        print(f'Password of {accountName} = {savedPass}.')


    def do_exit(self, arg):
        'close the window, and exit.'
        self._userPromptHandler.Exit()
        return True



def InitAll():
    promptUserInputHandler = PromptUserInputHandler()
    mfaManagerService = MfaManagerService()
    encryptionService = EncryptionService()
    passwordService = PasswordService()

    registrationService = RegistrationService(passwordService, encryptionService, mfaManagerService)
    authenticationService = AuthenticationService(mfaManagerService)
    mainPasswordManager = MainPasswordManager(authenticationService)

    userPrompt = UserPrompt(
        promptUserInputHandler,
        authenticationService,
        mfaManagerService,
        registrationService,
        mainPasswordManager
    )


    userPrompt.cmdloop()


if __name__ == '__main__':
    InitAll()
