import os


class FileManagement:
    Txt = 'txt'
    Encreption = 'enc'

    @staticmethod
    def CreateDir(dirPath):
        if not FileManagement.isFileExist(dirPath):
            os.mkdir(dirPath)

    @staticmethod
    def GetAllFilesInDir(dirPath):
        if not os.path.isdir(dirPath):
            raise Exception('Path is not a Directory.')

        files_in_dir = os.listdir(dirPath)
        files = [path for path in files_in_dir if not os.path.isdir(path)]
        return files

    @staticmethod
    def AppendToFile(filePath, data):
        with open(filePath, 'a') as file:
            file.write(data)


    @staticmethod
    def WriteInFile(filePath, data, inBytes=False,newFile=True):
        if newFile and FileManagement.isFileExist(filePath):
            raise Exception(f'File already exist in this Path:{filePath}.')

        if not newFile:
            FileManagement.AppendToFile(filePath, data)

        writeMode = 'wb' if inBytes else 'w'
        with open(filePath, writeMode) as file:
            file.write(data)

    @staticmethod
    def createFilePath(fileName, dirPath, fileType=Txt):
        fileWithType = f'{fileName}.{fileType}'
        fullFilePath = os.path.join(dirPath, fileWithType)
        return fullFilePath

    @staticmethod
    def isFileExist(filePath):
        return os.path.exists(filePath)

    @staticmethod
    def readFile(filePath):
        if not FileManagement.isFileExist(filePath):
            raise Exception(f'File does not exist in this Path:{filePath}.')

        plaintext = ''
        with open(filePath, 'rb') as fo:
            plaintext = fo.read()

        return plaintext

    @staticmethod
    def removeFileTypeFromFilePath(filePath):
        return os.path.splitext(filePath)[0]

    @staticmethod
    def ChangeFileType(filePath, newFileType):
        filePathWithoutType = FileManagement.removeFileTypeFromFilePath(filePath)
        newFilePath = f'{filePathWithoutType}.{newFileType}'
        return newFilePath

    @staticmethod
    def deleteFile(filePath):
        if not FileManagement.isFileExist(filePath):
            raise Exception(f'File does not exist in this Path:{filePath}.')
        os.remove(filePath)