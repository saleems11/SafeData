
# I wanted to set up some parameters using env variable, but it looks like
# that it doesn't save the env variable value after the proccess finish.
# need to do iy using json file, but for now set up env variable isn't very important.
import os

from AppConfig.Consts import Consts
from AppConfig.IConfiguration import IConfiguration
from Service.FileManagement import FileManagement


class Configuration(IConfiguration):

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