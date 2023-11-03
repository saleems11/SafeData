import unittest

from Service.GibberishService import GibberishService


class GibberishServiceTest(unittest.TestCase):

    def test_AddAndRemoveGibberish(self):
        expected = 'Data That should not be changed and nothing should be missing.'
        generatedGibberish = GibberishService.addGibberishToData(expected)
        actual = GibberishService.removeGibberishFromData(generatedGibberish)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()