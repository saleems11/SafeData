import os

from AppConsts.Consts import Consts


class AccessService:

    def __init__(self):
        pass

    @staticmethod
    def validateCanAccessPath(dir_path):
        if Consts.CanEncrypteUnder in dir_path:
            return True
        else:
            print(f'Invalid Path\nTry again (Path Must be under: {Consts.CanEncrypteUnder})')
            return False

    @staticmethod
    def getValidDirPath(cur_dir, default_dir):
        dir_path = None
        while True:
            # dir_path = input(f'Enter Dir path to Encrypt (Path Must be under: {AccessService.CanEncrypteUnder}) :')
            dir_path = default_dir if len(cur_dir) == 0 else default_dir + '\\' + cur_dir

            if not AccessService.validateCanAccessPath(dir_path):
                continue

            if os.path.isdir(dir_path):
                break
            else:
                print("Invalid Path\nTry again")
                continue
        return dir_path