from AppConfig.Consts import Consts
from Model.InputStatus import InputStatus
from Model.UserInputResult import UserInputResult
from UserInput.IUserInputHandler import IUserInputHandler


class BasePromptUserInputHandler(IUserInputHandler):
    BREAK_INPUT = "CNT+C"
    EventHandlers = None

    def __init__(self):
        pass

    @staticmethod
    def getInstructionMessgae():
        return f"Wellcome to {Consts.APP_NAME}," \
               f"To Exist Please Enter anywhere {BasePromptUserInputHandler.BREAK_INPUT}\n" \
               f"You can manage your secret txt file here (they may contain your password).\n" \
               f"Use help/? to help you with the command, formate help [cmd].\n" \
               f"Use setUpEnv cmd to setup you env first."

    def getUserInput(self, message) -> str:
        userInput = input(message)
        userInputResult = self._handleInput(userInput)
        return userInputResult.input


    def _handleInput(self, input) -> UserInputResult:
        for eventHanlder in BasePromptUserInputHandler.getEventHandlers():
            status = eventHanlder(input)
            if status != InputStatus.VALID:
                self.Exit()
        return UserInputResult(input, InputStatus.VALID)

    def Exit(self):
        pass

    @staticmethod
    def _checkBreakInput(input) -> InputStatus:
        if str.endswith(input, BasePromptUserInputHandler.BREAK_INPUT):
            # return InputStatus.BREAK
            exit()
        return InputStatus.VALID

    @staticmethod
    def getEventHandlers() -> []:
        if BasePromptUserInputHandler.EventHandlers is not None:
            return BasePromptUserInputHandler.EventHandlers

        BasePromptUserInputHandler.EventHandlers = [
            BasePromptUserInputHandler._checkBreakInput
        ]
        return BasePromptUserInputHandler.EventHandlers
