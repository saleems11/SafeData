class PathAccessException(Exception):
    def __init__(self, pathToAccess, validPathToAccess, message):
        super().__init__(message)
        self._pathToAccess = pathToAccess
        self._validPathToAccess = validPathToAccess

    def __str__(self):
        return f'{super().__str__()}, pathToAccess={self._pathToAccess}, validPathToAccess={self._validPathToAccess}'