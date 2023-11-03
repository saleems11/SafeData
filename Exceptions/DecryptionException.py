class DecryptionException(Exception):
    def __init__(self, ex, message):
        super().__init__(message)
        self.innerEx = ex