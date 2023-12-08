import unittest

from Authentication.MfaManagerService import MfaManagerService
from Service.MfaService import MfaService


class MfaServiceTest(unittest.TestCase):

    def test_getMfaKeyFromMfaKeyDecrebtedKey_UsedEmailThatDoesNotExist_returnsNone(self):
        # Arrange
        email = 'test@test.com'
        otherEmail = 'otherEmailtest@test.com'
        someKey= 'somekey123_'*3
        mfaKey = MfaManagerService.buildMfaKey(someKey, email)

        expected = None
        # Act
        mfaKey = MfaService.getMfaKeyFromMfaKeyDecrebtedKey(mfaKey, email=otherEmail)
        # Assert
        self.assertEqual(expected, mfaKey)

    def test_getMfaKeyFromMfaKeyDecrebtedKey_UsedUserNameThatDoesNotExist_returnsNone(self):
        # Arrange
        email = 'test@test.com'
        otherUserName = 'otherEmailtest'
        someKey= 'somekey123_'*3
        mfaKey = MfaManagerService.buildMfaKey(someKey, email)

        expected = None
        # Act
        mfaKey = MfaService.getMfaKeyFromMfaKeyDecrebtedKey(mfaKey, email=otherUserName)
        # Assert
        self.assertEqual(expected, mfaKey)

    def test_getMfaKeyFromMfaKeyDecrebtedKey_UsedUserNameThatIsSubstring_returnsNone(self):
        # Arrange
        email = 'otherEmailtest@test.com'
        otherUserName = 'test'
        someKey= 'somekey123_'*3
        mfaKey = MfaManagerService.buildMfaKey(someKey, email)

        expected = None
        # Act
        mfaKey = MfaService.getMfaKeyFromMfaKeyDecrebtedKey(mfaKey, email=otherUserName)
        # Assert
        self.assertEqual(expected, mfaKey)

    def test_getMfaKeyFromMfaKeyDecrebtedKey_UsedEmailThatExist_returnsKey(self):
        # Arrange
        email = 'test@test.com'
        someKey= 'somekey123_'*3
        mfaKey = MfaManagerService.buildMfaKey(someKey, email)

        expected = someKey
        # Act
        mfaKey = MfaService.getMfaKeyFromMfaKeyDecrebtedKey(mfaKey, email=email)
        # Assert
        self.assertEqual(expected, mfaKey)

    # This test is decativated as the login via username is disabled for now.
    # def test_getMfaKeyFromMfaKeyDecrebtedKey_UsedUserNameThatExist_returnsKey(self):
    #     # Arrange
    #     userName = 'testtest'
    #     email = f'{userName}@test.com'
    #     someKey= 'somekey123_'*3
    #     mfaKey = MfaManagerService.buildMfaKey(someKey, email)
    #
    #     expected = someKey
    #     # Act
    #     mfaKey = MfaService.getMfaKeyFromMfaKeyDecrebtedKey(mfaKey, email=userName)
    #     # Assert
    #     self.assertEqual(expected, mfaKey)

if __name__ == '__main__':
    unittest.main()