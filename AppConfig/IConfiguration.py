class IConfiguration:

    def __init__(self):
        pass

    def GetValueOrDefault(self, configName, defaultVal):
        pass

    def setUpConsts(self, canEncrypteUnder, savedPasswordDirPath):
        pass

    def IsConstsAreSetUpSuccesfuly(self):
        pass

    def IsInDebugMode(self):
        pass

    def printConfigurations(self):
        data = f'Parameters:\n' \
               f'CanEncrypteUnder = {self.CanEncrypteUnder}\n' \
               f'Saved Password Dir Path = {self.SavedPasswordDirPath}.\n' \
               f'-------------------------------------------------------'
        print(data)