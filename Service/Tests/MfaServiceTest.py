import unittest

from Service.MfaService import MfaService


class MfaServiceTest(unittest.TestCase):

    def test_getMfaKeyFromMfaKeyDecrebtedKey_UsedEmailThatDoesNotExist_returnsNone(self):
        # Arrange
        email = 'test@test.com'
        otherEmail = 'otherEmailtest@test.com'
        someKey= 'somekey123_'*3
        mfaKey = f'{someKey}{email}'

        expected = None
        # Act
        mfaKey = MfaService.getMfaKeyFromMfaKeyDecrebtedKey(mfaKey, emailOrUserName=otherEmail)
        # Assert
        self.assertEqual(expected, mfaKey)

    def test_getMfaKeyFromMfaKeyDecrebtedKey_UsedUserNameThatDoesNotExist_returnsNone(self):
        # Arrange
        email = 'test@test.com'
        otherUserName = 'otherEmailtest'
        someKey= 'somekey123_'*3
        mfaKey = f'{someKey}{email}'

        expected = None
        # Act
        mfaKey = MfaService.getMfaKeyFromMfaKeyDecrebtedKey(mfaKey, emailOrUserName=otherUserName)
        # Assert
        self.assertEqual(expected, mfaKey)

    def test_getMfaKeyFromMfaKeyDecrebtedKey_UsedUserNameThatIsSubstring_returnsNone(self):
        # Arrange
        email = 'otherEmailtest@test.com'
        otherUserName = 'test'
        someKey= 'somekey123_'*3
        mfaKey = f'{someKey}{email}'

        expected = None
        # Act
        mfaKey = MfaService.getMfaKeyFromMfaKeyDecrebtedKey(mfaKey, emailOrUserName=otherUserName)
        # Assert
        self.assertEqual(expected, mfaKey)

    def test_getMfaKeyFromMfaKeyDecrebtedKey_UsedEmailThatExist_returnsKey(self):
        # Arrange
        email = 'test@test.com'
        someKey= 'somekey123_'*3
        mfaKey = f'{someKey}{email}'

        expected = someKey
        # Act
        mfaKey = MfaService.getMfaKeyFromMfaKeyDecrebtedKey(mfaKey, emailOrUserName=email)
        # Assert
        self.assertEqual(expected, mfaKey)

    def test_getMfaKeyFromMfaKeyDecrebtedKey_UsedUserNameThatExist_returnsKey(self):
        # Arrange
        userName = 'testtest'
        email = f'{userName}@test.com'
        someKey= 'somekey123_'*3
        mfaKey = f'{someKey}{email}'

        expected = someKey
        # Act
        mfaKey = MfaService.getMfaKeyFromMfaKeyDecrebtedKey(mfaKey, emailOrUserName=userName)
        # Assert
        self.assertEqual(expected, mfaKey)

if __name__ == '__main__':
    unittest.main()