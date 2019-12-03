import os
import pymongo
from TC_model import *
from TC_view import *
from pickle import dumps


def creating_file_model(f_sys):
    e = Directory('E:', None)
    f_sys.insert_one({'path': 'E:', 'obj': dumps(e)})
    print('Dir created: E:\nobj:', e)
    folder_recursion('E:', e, f_sys)


def folder_recursion(dir, rootdir_obj, f_sys):
    files = os.listdir(dir + '/')
    for file in files:
        if file[0] == '$':
            pass
        elif os.path.isfile(dir + '/' + file):
            type = file[file.rfind('.')+1::]
            if type == 'txt':
                f = Document(dir + '/' + file, rootdir_obj, 'txt')
            elif type == 'html':
                f = HTML(dir + '/' + file, rootdir_obj, 'html')
            else:
                f = Other(dir + '/' + file, rootdir_obj, type)

            f_sys.insert_one({'path': dir + '/' + file, 'obj': dumps(f), 'type': type})

        elif os.path.isdir(dir + '/' + file):
            try:
                current_dir = Directory(dir + '/' + file, rootdir_obj)
                f_sys.insert_one({'path': dir + '/' + file, 'obj': dumps(current_dir), 'type': 'dir'})
                print('Dir created:', dir + '/' + file, '\nobj:', current_dir)
                folder_recursion(dir + '/' + file, current_dir, f_sys)
            except PermissionError:
                print('Access is denied:', dir + '/' + file)


def file_system():
    mongo = pymongo.MongoClient()
    mongo.drop_database('FileSys')
    tc = mongo.FileSys
    f_sys = tc.file_sys
    creating_file_model(f_sys)


if __name__ == '__main__':
    file_system()