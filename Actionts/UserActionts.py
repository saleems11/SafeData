# from Authentication.AuthenticationService import AuthenticationService
# from Authentication.MfaManagerService import MfaManagerService
# from Authentication.RegistrationService import RegistrationService
# from Model.LogInReturnStatus import LogInReturnStatus
# from Model.Status import Status
# from UserInput.PromptUserInputHandler import PromptUserInputHandler
#
#
# class UserActionts:
#
#     def __init__(self,
#                  userPromptHandler:PromptUserInputHandler,
#                  authenticationService:AuthenticationService,
#                  mfaManagerService:MfaManagerService,
#                  registrationService:RegistrationService):
#         self._userPromptHandler = userPromptHandler
#         self._authenticationService = authenticationService
#         self._mfaManagerService = mfaManagerService
#         self._registrationService = registrationService
#
#     def __GetPassword(self, encrypt=False):
#         if self._authenticationService.isAuthnticated():
#             return self._authenticationService.getPassowrd()
#         if encrypt:
#             return self._userPromptHandler.getValidPassword()
#         return self._userPromptHandler.getInputPassword()
#
#     def __ValidateMfa(self):
#         mfaValidationResult = None
#         for remainigRetires in range(self.MaxMfaRetry - 1, -1, -1):
#             mfaKey = self._userPromptHandler.getValidMfaInputLogIn()
#             mfaValidationResult = self._mfaManagerService.validate(mfaKey)
#
#             if mfaValidationResult.IsSucceded():
#                 break
#
#             self._userPromptHandler.HandleMfaLoginResult(mfaValidationResult, remainigRetires)
#
#             mfaValidationResult = None
#
#         return mfaValidationResult if mfaValidationResult is not None \
#                    else LogInReturnStatus(Status.RegistrationFailedToManyAttemps, "Registration Failed.")
#
#     def login(self, arg):
#         'Login to your account, requires password and Mfa(your should be already registered)'
#         # Add later locking mechanisem
#         password = self.__GetPassword()
#         mfaKey = self._userPromptHandler.getValidMfaInputLogIn()
#
#         loginResult = self._authenticationService.login(password, mfaKey)
#         self._userPromptHandler.HandleLoginResult(loginResult)
#
#     def register(self):
#         'Register your account so you can encrypte and decrepte Data'
#         accountName = self._userPromptHandler.getAccountMfaName()
#         self._mfaManagerService.CreateRegistrationQR(accountName)
#
#         mfaValidationResult = self.__ValidateMfa()
#         self._userPromptHandler.HandleregistrationResult(mfaValidationResult)
#         if not mfaValidationResult.IsSucceded():
#             return
#
#         password = self.__GetPassword(True)
#         registrationResult = self._registrationService.register(password)
#         self._userPromptHandler.HandleregistrationResult(registrationResult)

# Need some work