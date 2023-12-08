from Model.IAmUnique import IAmUnique
from Model.ISerilizable import ISerilizable


class SavedPasswordData(ISerilizable, IAmUnique):

    def __init__(self, serviceName, password, email, website=None, metaData={}):
        self.serviceName = serviceName
        self.email = email
        self.password = password
        self.website = website
        self.metaData = metaData

    def setEmail(self, email):
        self.email = email

    def getUniqueId(self):
        return self.email + self.serviceName

    def __str__(self):
        return f'Email = {self.email}\n' \
               f'Service Name = {self.serviceName}\n' \
               f'Password = {self.password}\n' \
               f'websiteUrl = {self.website}\n' \
               f'more Info = {self.metaData}.'