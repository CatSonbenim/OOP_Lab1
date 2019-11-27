import win32api
import os
import pymongo
from TC_model import *

def creating_file_model():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\\\000')[:-1]
    print(drives)


def folder_recursion(dir):
    files = os.listdir(dir + '\\')
    for file in files:
        if file[0] == '$':
            pass
        elif os.path.isfile(dir + '\\' + file):
            type = file[file.rfind('.')+1::]
            types = {}


creating_file_model()