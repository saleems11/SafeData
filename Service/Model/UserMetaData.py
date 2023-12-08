from Model.IAmUnique import IAmUnique
from Model.ISerilizable import ISerilizable


class UserMetaData(ISerilizable, IAmUnique):

    def __init__(self, userEmail, servicesNamesList, lastLoginAt, accountCreatedAt):
        self.userEmail = userEmail
        self.servicesNamesList = servicesNamesList
        self.lastLoginAt = lastLoginAt
        self.accountCreatedAt = accountCreatedAt

    def getUniqueId(self):
        return self.userEmail

    def addService(self, serviceName):
        self.servicesNamesList.append(serviceName)