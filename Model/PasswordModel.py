import json


class PasswordModel:

    def __init__(self, name, password, url='', describtion=''):
        self.name = name
        self.password = password
        self.url = url
        self.describtion = describtion

    def toJson(self):
        return json.dumps(self)

    @staticmethod
    def loadJson(string:str):
        dict = json.loads(string)
        return PasswordModel(
            dict['name'],
            dict['password'],
            dict.get('url', ''),
            dict.get('describtion', '')
        )
