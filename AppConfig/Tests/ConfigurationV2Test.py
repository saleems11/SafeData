import unittest

from AppConfig.Configuration import ConfigurationV2

class ConfigurationV2Test(unittest.TestCase):
    configurationV2Instance = None

    @classmethod
    def setUpClass(cls):
        cls.configurationV2Instance = ConfigurationV2()

    @classmethod
    def tearDownClass(cls):
        cls.configurationV2Instance = None

    def test_LoadingTheRightConfig(self):
        self.assertEqual('', self.configurationV2Instance.CanEncrypteUnder)
        self.assertEqual('', self.configurationV2Instance.SavedPasswordDirPath)

if __name__ == '__main__':
    unittest.main()