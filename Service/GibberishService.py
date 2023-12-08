import string
import secrets

from AppConfig.Consts import Consts

# The same as adding Salt
class GibberishService:

    @staticmethod
    def addGibberishToData(data:str) -> str:
        return GibberishService.__GenerateGibberishData(data)

    @staticmethod
    def removeGibberishFromData(dataWithGebb:str) -> str:
        return GibberishService.__ParseGibberishData(dataWithGebb)

    @staticmethod
    def GenerateGibberish():
        alphabet = string.ascii_letters + string.digits
        gibberish = ''.join(secrets.choice(alphabet) for _ in range(Consts.Gibberish_Len))
        return gibberish

    @staticmethod
    def __ParseGibberishData(dataWithGebb):
        return dataWithGebb[Consts.Gibberish_Len: -1 * Consts.Gibberish_Len]

    @staticmethod
    def __GenerateGibberishData(data):
        return GibberishService.GenerateGibberish()+data+GibberishService.GenerateGibberish()