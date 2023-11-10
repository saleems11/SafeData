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
        pass