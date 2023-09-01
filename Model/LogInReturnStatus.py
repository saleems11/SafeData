from Model.IInputResult import IInputResult
from Model.Status import Status

class LogInReturnStatus(IInputResult):
    def __init__(self, status:Status, message):
        self.status = status
        self.message = message

    def IsSucceded(self):
        return self.status == Status.Succed

    def IsFailed(self):
        return self.status != Status.Succed