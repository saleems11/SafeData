from AppConfig.ConfigurationV2 import ConfigurationV2
from AppConfig.Consts import Consts
from AppConfig.IConfiguration import IConfiguration
from Authentication.AuthenticationService import AuthenticationService
from Authentication.MfaManagerService import MfaManagerService
from Authentication.RegistrationService import RegistrationService
from Exceptions.AuthenticationException import AuthenticationException
from Exceptions.DecryptionException import DecryptionException
from Exceptions.InvalidFileTypeException import InvalidFileTypeException
from Exceptions.PathAccessException import PathAccessException
from Model.LogInReturnStatus import LogInReturnStatus
from Model.Status import Status
from PasswordManager.FileEncryptionManager import FileEncryptionManager
from PasswordManager.MainPasswordManager import MainPasswordManager
from Service.AccessService import AccessService
from Service.FileEncryptionService import FileEncryptionService
from Service.PasswordService import PasswordService
from UserInput.BasePromptUserInputHandler import BasePromptUserInputHandler
from UserInput.PromptUserInputHandler import PromptUserInputHandler

import cmd


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
                 mainPasswordManager:MainPasswordManager,
                 fileEncryptionManager:FileEncryptionManager,
                 configuration:IConfiguration):
        super().__init__()
        self._userPromptHandler = userPromptHandler
        self._authenticationService = authenticationService
        self._mfaManagerService = mfaManagerService
        self._registrationService = registrationService
        self._mainPasswordManager = mainPasswordManager
        self._fileEncryptionManager = fileEncryptionManager
        self._configuration = configuration

        self.__setUpEnv(False, True)


    def __GetPassword(self):
        if self._authenticationService.isAuthnticated():
            return self._authenticationService.getPassowrdKey()
        return self._userPromptHandler.getInputPassword()

    def __GetRegistrationPassword(self):
        return self._userPromptHandler.getValidPassword()

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

    def __setUpEnv(self, forceUpdate=False, initIsCalling=False):
        if forceUpdate or not self._configuration.IsConstsAreSetUpSuccesfuly():
            allowEncDecUnderPath = self._userPromptHandler.getAllowEncDecUnderPath()
            savedPasswordsFileLocation = self._userPromptHandler.getSavedPasswordsFileLocation()
            self._configuration.setUpConsts(allowEncDecUnderPath, savedPasswordsFileLocation)

        if initIsCalling and self._configuration.IsInDebugMode():
            self._configuration.printConfigurations()

    def do_setUpEnv(self, arg):
        'Set Up is required to use the application.'
        try:
            self.__setUpEnv(True)
            self._configuration.printConfigurations()
        except Exception as ex:
            handeled = self.__handleMainExcptions(ex)
            if not handeled: raise


    def do_login(self, arg):
        'Login to your account, requires password and Mfa(your should be already registered).'
        # Add later locking mechanisem
        try:
            emailOrUserName = self._userPromptHandler.getEmailOrUserName()
            password = self.__GetPassword()
            mfaKey = self._userPromptHandler.getValidMfaInputLogIn()
            loginResult = self._authenticationService.login(emailOrUserName, password, mfaKey)
            self._userPromptHandler.HandleLoginResult(loginResult)
        except Exception as ex:
            handeled = self.__handleMainExcptions(ex)
            if not handeled: raise

    def do_logout(self, arg):
        'Logout from your account.'
        try:
            loginResult = self._authenticationService.logout()
            print('Logout Succeded.')
        except Exception as ex:
            handeled = self.__handleMainExcptions(ex)
            if not handeled: raise

    def do_register(self, arg):
        'Register your account so you can encrypte and decrepte Data'
        try:
            accountName = self._userPromptHandler.getAccountMfaName()
            email = self._userPromptHandler.getValidEmail()
            self._mfaManagerService.CreateRegistrationQR(accountName)

            mfaValidationResult = self.__ValidateMfa()
            self._userPromptHandler.HandleregistrationResult(mfaValidationResult)
            if not mfaValidationResult.IsSucceded():
                return

            password = self.__GetRegistrationPassword()
            registrationResult = self._registrationService.register(email, password)
            self._userPromptHandler.HandleregistrationResult(registrationResult)
        except Exception as ex:
            handeled = self.__handleMainExcptions(ex)
            if not handeled: raise

    def do_addPassword(self, arg):
        'Add New Password, it will be saved in a file where you had set the SavedPasswordDirPath'
        try:
            accountName = self._userPromptHandler.getWebSiteServiceName()
            password = self._userPromptHandler.getInputPassword()

            self._mainPasswordManager.addPassword(accountName, password)
            # Clean-up
            password = None
        except Exception as ex:
            handeled = self.__handleMainExcptions(ex, 'while adding new password')
            if not handeled: raise

    def do_getPassword(self, arg):
        'Get Saved Password'
        try:
            accountName = self._userPromptHandler.getWebSiteServiceName()

            savedPass = self._mainPasswordManager.getPassword(accountName)
            print(f'Password of {accountName} = {savedPass}.')
        except Exception as ex:
            handeled = self.__handleMainExcptions(ex, "while trying to get password.")
            if not handeled: raise

    def do_encFile(self, arg):
        'Enter a valid file path (.txt file only will be able to encrypt) and it will encrypted.'
        try:
            filePath = self._userPromptHandler.getFilePath('encrypt')

            self._fileEncryptionManager.encryptFile(filePath)
            print(f'File {filePath}, had been encrypted Succesfuly.')
        except Exception as ex:
            handeled = self.__handleMainExcptions(ex)
            if not handeled: raise

    def do_decFile(self, arg):
        'Enter a valid file path (.txt file only will be able to decrypt) and it will decrypted.'
        try:
            filePath = self._userPromptHandler.getFilePath('decrypt')
            self._fileEncryptionManager.decryptFile(filePath)
            print(f'File {filePath}, had been decrypted Succesfuly.')
        except Exception as ex:
            handeled = self.__handleMainExcptions(ex)
            if not handeled: raise

    def do_exit(self, arg):
        'close the window, and exit.'
        self._userPromptHandler.Exit()
        return True

    def __handleMainExcptions(self, ex, customMessage=""):
        if isinstance(ex, AuthenticationException):
            print(f'{ex} - Need to authenticate first.{customMessage}')
            return True
        if isinstance(ex, DecryptionException):
            print(f'Unable to Decrypte the data.{customMessage}')
            return True
        if isinstance(ex, FileNotFoundError):
            print(f'{ex} - Please enter a valid Path.{customMessage}')
            return True
        if isinstance(ex, FileExistsError):
            print(f'The prev step Failed, please try again.{customMessage}')
            return True
        if isinstance(ex, InvalidFileTypeException):
            print(f'{ex}.{customMessage}')
            return True
        if isinstance(ex, PathAccessException):
            print(f'{ex}.{customMessage}')
            return True



def InitAll():
    configuration = ConfigurationV2()
    promptUserInputHandler = PromptUserInputHandler()
    mfaManagerService = MfaManagerService()
    # encryptionService = EncryptionService()
    passwordService = PasswordService()

    accessService = AccessService(configuration)

    fileEncryptionService = FileEncryptionService(accessService)
    registrationService = RegistrationService(passwordService, fileEncryptionService, mfaManagerService, configuration)

    authenticationService = AuthenticationService(mfaManagerService, registrationService, fileEncryptionService)
    fileEncryptionManager = FileEncryptionManager(authenticationService, fileEncryptionService)
    mainPasswordManager = MainPasswordManager(fileEncryptionManager, configuration)

    userPrompt = UserPrompt(
        promptUserInputHandler,
        authenticationService,
        mfaManagerService,
        registrationService,
        mainPasswordManager,
        fileEncryptionManager,
        configuration
    )

    userPrompt.cmdloop()


if __name__ == '__main__':
    InitAll()
