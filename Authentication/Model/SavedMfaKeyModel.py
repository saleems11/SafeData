import pickle

from AppConfig.Consts import Consts


class SavedMfaKeyModel:
    def __init__(self, key, email):
        self.key = key
        self.email = email

    def serializeJson(self)->str:
        return str(pickle.dumps(self), encoding=Consts.encoding_byte_array)

    @staticmethod
    def deserilizeJson(str):
        try:
            return pickle.loads(bytes(str, encoding=Consts.encoding_byte_array))
        except:
            return None