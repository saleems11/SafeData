import os

from Service.AccessService import AccessService
from Service.FileEncryptionService import FileEncryptionService
from Service.FileManagement import FileManagement
from Service.PasswordService import PasswordService


class DirectoryEncryptionService:

    def __init__(self, accessService:AccessService):
        self._accessService = accessService


    def encrypt_dir(self, password, cur_dir, default_dir):
        dir_path = self._accessService.getValidDirPath(cur_dir, default_dir)
        files_in_dir = os.listdir(dir_path)

        # Hash the key to convert it to 256
        key = PasswordService.HashifyPassword(password)

        for file in files_in_dir:
            if os.path.isdir(file): continue

            if file.endswith(FileManagement.Encryption):
                FileEncryptionService.encrypted_file(dir_path + '\\' + file, key)

        print("File Encrypted Successfully")
        # Clean-up
        password = None