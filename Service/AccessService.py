import os

from AppConfig.Configuration import Configuration


class AccessService:

    def __init__(self, configuration: Configuration):
        self._configuration = configuration

    def validateCanAccessPath(self, dir_path):
        canAccess = self._configuration.CanEncrypteUnder in dir_path
        return canAccess

    def tryAccessPath(self, path):
        if not self.validateCanAccessPath(path):
            raise Exception(f'CAN NOT ACCESS THIS PATH, path={path}.')

    def getValidDirPath(self, cur_dir, default_dir):
        dir_path = None
        while True:
            dir_path = default_dir if len(cur_dir) == 0 else default_dir + '\\' + cur_dir

            if not self.validateCanAccessPath(dir_path):
                continue

            if os.path.isdir(dir_path):
                break
            else:
                print("Invalid Path\nTry again")
                continue
        return dir_path