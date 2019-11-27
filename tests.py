import win32api
import os
from bs4 import BeautifulSoup
import pymongo

drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\\\000')[:-1]
print(drives)


def rec_going(dir, i=1):
    files = os.listdir(dir + '\\')
    for file in files:
        if file[0] == '$':
            pass
        elif os.path.isfile(dir + '\\' + file):
            print('-'*i + dir + '\\' + file)
        else:
            print('-'*i + dir + '\\' + file)
            dir_name = dir + '\\' + file
            try:
                if os.listdir(dir_name) != []:
                    rec_going(dir_name, i+1)
                else:
                    pass
            except PermissionError:
                print('Access is denied')

for drive in drives:
    print(drive)
    rec_going(drive)


def remove_attrs(soup, whitelist=tuple()):
    for tag in soup.findAll(True):
        for attr in [attr for attr in tag.attrs if attr not in whitelist]:
            del tag[attr]
    return soup



list.sort(key=len)

