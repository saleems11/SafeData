import os

from AppConsts.Consts import Consts


class AccessService:

    def __init__(self):
        pass

    @staticmethod
    def validateCanAccessPath(dir_path):
        canAccess = Consts.CanEncrypteUnder in dir_path
        return canAccess

    @staticmethod
    def tryAccessPath(dir_path):
        if not AccessService.validateCanAccessPath(dir_path):
            raise Exception('CAN NOT ACCESS THIS PATH.')

    @staticmethod
    def getValidDirPath(cur_dir, default_dir):
        dir_path = None
        while True:
            dir_path = default_dir if len(cur_dir) == 0 else default_dir + '\\' + cur_dir

            if not AccessService.validateCanAccessPath(dir_path):
                continue

            if os.path.isdir(dir_path):
                break
            else:
                print("Invalid Path\nTry again")
                continue
        return dir_path