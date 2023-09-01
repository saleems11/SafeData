from enum import Enum

class Status(Enum):
    Succed = 1
    InvalidPassword = 2
    ExceptionOccured = 3
    InvalidMfaAuth = 4
    RegistrationFailedToManyAttemps = 5