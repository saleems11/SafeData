from datetime import datetime

import pyotp
import qrcode
from PIL import Image
import io

from AppConfig.Consts import Consts
from Authentication.Model.SavedMfaKeyModel import SavedMfaKeyModel


class MfaService:
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
        # Pin is the mfa key
        # datetime.now() - uses the local time of the machine, it must be the same timezone with the Mfa app.
        # 1 - is used to handle cases where the diff bettwen the Mfa server/client is bigger than 30 sec.
        return self._TOTP.verify(Pin, datetime.now(), 1)

    @staticmethod
    def getMfaKeyFromMfaKeyDecrebtedKey(mfaKeyDecrebtedKey, email) -> str:
        """ Part of this function feature is to allow only user name, but as the data is not yet saved in db, it will
        be hard to access a file based on a username, as it will require searching in the entire folder."""
        if not email in mfaKeyDecrebtedKey:
            return None

        savedMfaKeyModel = SavedMfaKeyModel.deserilizeJson(mfaKeyDecrebtedKey)
        savedEmail = savedMfaKeyModel.email

        # isUserName = email.find('@') < 0
        # if isUserName:
        #     savedUserName = savedEmail.split('@')[0]
        #     if savedUserName != email:
        #         return None
        # elif savedEmail != email:
        #     return None

        if savedEmail != email:
            return None

        return savedMfaKeyModel.key