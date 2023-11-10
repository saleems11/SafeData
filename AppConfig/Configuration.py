
# I wanted to set up some parameters using env variable, but it looks like
# that it doesn't save the env variable value after the proccess finish.
# need to do iy using json file, but for now set up env variable isn't very important.
import json
import os

from AppConfig.Consts import Consts
from AppConfig.IConfiguration import IConfiguration
from Service.FileManagement import FileManagement


class Configuration:

    def __init__(self):
        self.CanEncrypteUnder = f'Path'
        self.SavedPasswordDirPath = f'Path'
        self.__updateConsts()


    def __updateConsts(self):
        self.CanEncrypteUnder = self.GetValueOrDefault(
            Consts._Can_Encrypte_Under,
            self.CanEncrypteUnder)

        self.SavedPasswordDirPath = self.GetValueOrDefault(
            Consts._Saved_Password_Dir_Path,
            self.SavedPasswordDirPath)

        FileManagement.DoesPathExist(self.CanEncrypteUnder, True)
        FileManagement.DoesPathExist(self.SavedPasswordDirPath, True)


    def GetValueOrDefault(self, configName, defaultVal):
        configVal = os.getenv(configName)
        return defaultVal if configVal is None else configVal

    def setUpConsts(self, canEncrypteUnder, savedPasswordDirPath):
        os.environ[Consts._Can_Encrypte_Under] = canEncrypteUnder
        os.environ[Consts._Saved_Password_Dir_Path] = savedPasswordDirPath

        self.__updateConsts()


    def IsConstsAreSetUpSuccesfuly(self):
        try:
            self.__updateConsts()
        except Exception:
            # Failed to setup the consts
            return False
        return True

    def IsInDebugMode(self):
        boolStr = self.GetValueOrDefault(Consts._DebugMode, "False")
        return bool(boolStr)


    def printConfigurations(self):
        data = f'Parameters:\n' \
               f'CanEncrypteUnder = {self.CanEncrypteUnder}\n' \
               f'Saved Password Dir Path = {self.SavedPasswordDirPath}.\n' \
               f'-------------------------------------------------------'
        print(data)

class ConfigurationV2(IConfiguration):

    def __init__(self):
        self.CanEncrypteUnder = 'Path'
        self.SavedPasswordDirPath = 'Path'
        configData = self.__GetConfigData()
        self.__UpdateConfigData(configData)


    def GetValueOrDefault(self, configName, defaultVal):
        pass

    def setUpConsts(self, canEncrypteUnder, savedPasswordDirPath):
        self.__GetConfigData()

    def IsConstsAreSetUpSuccesfuly(self):
        pass

    def IsInDebugMode(self):
        pass

    def printConfigurations(self):
        pass

    def __GetConfigData(self) -> {}:
        ConfigFilePath = os.path.join('.\\', Consts.Confgi_File_Name)

        with open(ConfigFilePath) as f:
            valuesDict = json.load(f)
            return valuesDict

    def __UpdateConfigData(self, dataDict:{}):
        self.CanEncrypteUnder = dataDict[Consts._Can_Encrypte_Under]
        self.SavedPasswordDirPath = dataDict[Consts._Saved_Password_Dir_Path]