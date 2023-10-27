from datetime import datetime

import pyotp
import qrcode
from PIL import Image
import io

from AppConsts.Consts import Consts


class MfaService:
    MfaDecreptionSuccessCodeMessage = 'MfaDecreptionSuccessCodeMessage'

    def __init__(self, key=None):
        self.key = MfaService.GenerateKey(key)
        self._TOTP = pyotp.TOTP(self.key)

    def getKeyAndDeleteIt(self):
        tempKey = self.key
        self.key = None
        return tempKey

    @staticmethod
    def GenerateKey(key=None):
        key = pyotp.random_base32() if key == None else key
        return key

    def GenerateQrCode(self, AccountName):
        uri = self.GenerateUserBaseUri(AccountName)
        self.ShowQR(uri)

    def GenerateUserBaseUri(self, AccountName):
        uri = self._TOTP.provisioning_uri(name=AccountName, issuer_name=f'{Consts.APP_NAME} ')
        return uri

    @staticmethod
    def ShowQR(uriData):
        img = qrcode.make(uriData)
        buf = io.BytesIO()
        img.save(buf)

        buf.seek(0)
        im = Image.open(buf)
        im.show()

    def Validate(self, Pin):
        print(f'Mfa correct value: {self._TOTP.now()} and you entered {Pin}.')
        return self._TOTP.verify(Pin, datetime.now(), 1)

    @staticmethod
    def getMfaKeyFromMfaKeyDecrebtedKey(mfaKeyDecrebtedKey):
        return mfaKeyDecrebtedKey[:-(len(MfaService.MfaDecreptionSuccessCodeMessage))]