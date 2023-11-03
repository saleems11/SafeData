class InvalidFileTypeException(Exception):
    def __init__(self, expectedFileType, actualFileType, message):
        super().__init__(message)
        self._expectedFileType = expectedFileType
        self._actualFileType = actualFileType

    def __str__(self):
        return f'{super().__str__()}, expectedFileType={self._expectedFileType}, actualFileType={self._actualFileType}'