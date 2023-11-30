import json
import os
from pathlib import Path

from AppConfig.Consts import Consts
from AppConfig.IConfiguration import IConfiguration

# Json File Based Implementation

class ConfigurationV2(IConfiguration):
    defaultDummyPath = 'Path'

    def __init__(self):
        self.CanEncrypteUnder = self.defaultDummyPath
        self.SavedPasswordDirPath = self.defaultDummyPath
        self.DataDict = {}
        configData = self.__GetConfigData()
        self.__UpdateConfigData(configData)


    def GetValueOrDefault(self, configName, defaultVal):
        return self.DataDict.get(configName, defaultVal)

    def setUpConsts(self, canEncrypteUnder, savedPasswordDirPath):
        self.DataDict[Consts._Can_Encrypte_Under] = canEncrypteUnder
        self.DataDict[Consts._Saved_Password_Dir_Path] = savedPasswordDirPath

        ConfigFilePath = self.__GetConfigFilePath()

        import json
        with open(ConfigFilePath, 'w', encoding='utf-8') as f:
            json.dump(self.DataDict, f, ensure_ascii=False, indent=4)

        self.__GetConfigData()

    def IsConstsAreSetUpSuccesfuly(self):
        return True

    def IsInDebugMode(self):
        boolStr = self.GetValueOrDefault(Consts._DebugMode, "False")
        return bool(boolStr)

    def __GetConfigData(self) -> {}:
        ConfigFilePath = self.__GetConfigFilePath()

        with open(ConfigFilePath) as f:
            valuesDict = json.load(f)
            return valuesDict

    def __UpdateConfigData(self, dataDict:{}):
        self.CanEncrypteUnder = dataDict[Consts._Can_Encrypte_Under]
        self.SavedPasswordDirPath = dataDict[Consts._Saved_Password_Dir_Path]
        self.DataDict = dataDict

    def __GetConfigFilePath(self):
        ConfigRelaticFilePath = os.path.join('./', Consts.Confgi_File_Name)
        ConfigFilePath = Path(__file__).parent / ConfigRelaticFilePath
        return ConfigFilePath
