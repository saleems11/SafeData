import os
import pathlib

from Exceptions.InvalidFileTypeException import InvalidFileTypeException


class FileManagement:
    Txt = 'txt'
    Encryption = 'enc'

    @staticmethod
    def CreateDir(dirPath):
        if not FileManagement.DoesPathExist(dirPath):
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
        if newFile and FileManagement.DoesPathExist(filePath):
            raise FileExistsError(f'File already exist in this Path:{filePath}.')

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
    def DoesPathExist(path, raiseException=False):
        doesExist = os.path.exists(path)
        if raiseException and not doesExist:
            raise FileNotFoundError(f'Path does not exist, path:{path}.')
        return doesExist

    @staticmethod
    def readFile(filePath, asbytes=True):
        FileManagement.DoesPathExist(filePath, True)

        plaintext = ''
        readType = 'rb' if asbytes else 'r'
        with open(filePath, readType) as fo:
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
        if not FileManagement.DoesPathExist(filePath):
            raise Exception(f'File does not exist in this Path:{filePath}.')
        os.remove(filePath)

    @staticmethod
    def getFileType(filePath):
        return pathlib.Path(filePath).suffix[1:]

    @staticmethod
    def ValidAbleToDecrypt(filePath):
        fileType = FileManagement.getFileType(filePath)
        if FileManagement.getFileType(filePath) == FileManagement.Encryption:
            return
        raise InvalidFileTypeException(FileManagement.Encryption, fileType, "Invalid File type")

    @staticmethod
    def ValidAbleToEncrypt(filePath):
        fileType = FileManagement.getFileType(filePath)
        if FileManagement.getFileType(filePath) == FileManagement.Txt:
            return
        raise InvalidFileTypeException(FileManagement.Txt, fileType, "Invalid File type")

