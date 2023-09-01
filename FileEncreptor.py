# import os
# from time import sleep
#
# from Service.MfaService import MfaService
# from Model.Status import Status
#
#
#
#
#
#
#
#
# #Protection
#
#
# # const
#
# encoding = 'utf-8'
# UserRegistrationFolderForMfa = 'MfaRegistration'
# UserRegistrationFileNameForMfa = 'secureMfa'
# MfaDecreptionSuccessCodeMessage = 'MfaDecreptionSuccessCodeMessage'
#
# # globals
# mfaManager = None
# gpassword = None
#
#
#
#
#
#
#
#
#
#
#
#
#
# # GUI Handles
#
#
# def getFilePathAndKeyToDecrept(cur_dir):
#     while True:
#         file_path = input("Enter file path to Decrypt(including .file_type):")
#         if not file_path.endswith(encreptionFileType):
#             print(f"Please select an encrypted file, ends with {encreptionFileType}")
#             continue
#
#         file_path = file_path if len(cur_dir) == 0 else os.path.join(cur_dir, file_path)
#         if os.path.exists(file_path) and os.path.isfile(file_path):
#             break
#         else:
#             print("Invalid Path\nTry again")
#             return
#
#     # get the key from user
#     password = getPassword()
#     # Hash the key to convert it to 256
#     hash_object = hashlib.sha256(password.encode())
#     key = hash_object.hexdigest()[:32]
#     key = key.encode()
#     return file_path, key
#
# def DecryptFile_2_Handler(cur_dir):
#     (file_path, key) = getFilePathAndKeyToDecrept(cur_dir)
#     decrypt_file(file_path, key)
#
# def DecryptPreviewFile_6_Handler(cur_dir):
#     (file_path, key) = getFilePathAndKeyToDecrept(cur_dir)
#
#     try:
#         decreptedContent = decryptFileContent(file_path, key,True)
#         print(f'File Content: \n{decreptedContent}')
#     except UnicodeDecodeError:
#         print("Failed to decrept the data.")
#     except Exception:
#         print("An Error Icured in DecryptPreviewFile_6_Handler.")
#     decreptedContent = None
#
# def allFileInDir_4_Handler(cur_dir):
#     if cur_dir == '':
#         print("\n\nPlease Select first the current path !!\n\n")
#         return False
#
#     files_in_dir = os.listdir(cur_dir)
#     if not os.path.isdir(cur_dir):
#         print("Please Select Valid Path")
#         return False
#
#     print("--------- Files in Dir -----------")
#
#     for file in files_in_dir:
#         if os.path.isdir(file):
#             continue
#         if file.endswith(acceptedToEncrypteFileType):
#             print(file)
#         if file.endswith(encreptionFileType):
#             print(file, "           === Encrepted Files")
#
#     print("----------------------------------")
#     return True
#
#
#
# def validateDecrebtionOfMfaSucceded(mfaKeyDecrebtedKey):
#     return str.endswith(mfaKeyDecrebtedKey, MfaDecreptionSuccessCodeMessage)
#
#
#
#
# def userPrompt():
#     cur_dir = ''
#     while True:
#         print("-----------------\nThe current Dir: ", cur_dir, "\n-----------------\n")
#         user_input = input(f"File And Password Manager: V1.3.0\nHello This System can encrypt {acceptedToEncrypteFileType} Files\nPlease Select:\n1-Encrypt All files in dir\n2-Decrypt file\n"
#                            "3-set CUR_DIR\n4-get file in dir\n5-LogIn and SetMfa\n6-PreviewFile\n7-Exit\n8-Create Session\n")
#         if not user_input.isnumeric():
#             continue
#
#         input_int = int(user_input)
#         if input_int == 1:
#             succeded = allFileInDir_4_Handler(cur_dir)
#             if not succeded:
#                 continue
#             encrept = input("Are you sure you want to encrypt thos files(Y=1/N=3)")
#             if int(encrept) == 1:
#                 EncryptALL_1_Handler(cur_dir)
#             else:
#                 print("Will continue without Encrepting")
#         elif input_int == 2:
#             DecryptFile_2_Handler(cur_dir)
#         elif input_int == 3:
#             while True:
#                 cur_dir = input("Enter the CUR_DIR path:")
#                 if os.path.isdir(cur_dir): break
#                 print("Invalid Directory path")
#         elif input_int == 4:
#             allFileInDir_4_Handler(cur_dir)
#         elif input_int == 5:
#             LogInAndSetMfa_5_Handler()
#         elif input_int == 6:
#             DecryptPreviewFile_6_Handler(cur_dir)
#         elif input_int == 7:
#             break
#         elif input_int == 8:
#             SessionManager().createUserSession()
#         sleep(1.85)
#
#
#
# if __name__ == '__main__':
#     userPrompt()
#     # My Main PAssword is the my roboform Password