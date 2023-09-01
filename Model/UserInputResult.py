from Model.IInputResult import IInputResult
from Model.InputStatus import InputStatus


class UserInputResult(IInputResult):

    def __init__(self, input, status:InputStatus):
        self.input = input
        self.status = status

    def IsSucceded(self):
        self.status == InputStatus.VALID

    def IsFailed(self):
        self.status == InputStatus.BREAK

    def IsExit(self):
        self.status == InputStatus.BREAK