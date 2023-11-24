import unittest

from AppConfig.ConfigurationV2 import ConfigurationV2


class ConfigurationV2Test(unittest.TestCase):
    configurationV2Instance = None

    @classmethod
    def setUpClass(cls):
        cls.configurationV2Instance = ConfigurationV2()

    @classmethod
    def tearDownClass(cls):
        cls.configurationV2Instance = None

    def test_LoadingTheRightConfig(self):
        # Test if the value had been updated from the detault
        self.assertNotEqual(ConfigurationV2.defaultDummyPath, self.configurationV2Instance.CanEncrypteUnder)
        self.assertNotEqual(ConfigurationV2.defaultDummyPath, self.configurationV2Instance.SavedPasswordDirPath)

if __name__ == '__main__':
    unittest.main()