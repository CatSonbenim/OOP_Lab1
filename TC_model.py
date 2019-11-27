import os
import time
import shutil
from abc import ABC, abstractmethod
from PIL import Image
import pickle


class Directory:

    def __init__(self, path, rd):
        self.path = path
        self.size = os.path.getsize(path)
        change_date = time.ctime(os.path.getctime(path)).split(' ')
        day = change_date[2]
        month = {'Jan': '1', 'Feb': '2', 'Mar': '3', 'Apr': '4', 'May': '5', 'Jun': '6', 'Jul': '7', 'Aug': '8',
                 'Sep': '9', 'Oct': '10', 'Nov': '11', 'Dec': '12'}[change_date[1]]
        year = change_date[-1]
        self.change_date = day + '.' + month + '.' + year
        path = os.path.split(path)
        self.name = path[1]
        self.root_dir_path = path[0]
        self.root_dir = [rd]
        self.files = []

    def updater(self, file):
        #придумать тут функцию которая будет динамически обновлять панель отображения
        pass

    def add_dir(self, dir):
        self.root_dir.append(dir)

    def send_update(self):
        for directory in self.root_dir:
            directory.updater()

    def rename(self, new_name):
        os.rename(self.name, new_name)
        self.name = new_name

    def copy(self, new_folder):
        shutil.copy(self.path, new_folder.path)
        self.add_dir(new_folder)
        self.send_update()

    def create_file(self, filepath):
        pass

    def create_dir(self, filepath):
        pass


class File(ABC):

    def __init__(self, path, rd, file_type):
        self.path = path
        self.size = os.path.getsize(path)
        change_date = time.ctime(os.path.getctime(path)).split(' ')
        day = change_date[2]
        month = {'Jan': '1', 'Feb': '2', 'Mar': '3', 'Apr': '4', 'May': '5', 'Jun': '6', 'Jul': '7', 'Aug': '8',
                 'Sep': '9', 'Oct': '10', 'Nov': '11', 'Dec': '12'}[change_date[1]]
        year = change_date[-1]
        self.change_date = day + '.' + month + '.' + year
        path = os.path.split(path)
        self.name = path[1]
        self.root_dir_path = path[0]
        self.root_dir = [rd]
        self.type = file_type

    def add_dir(self, dir):
        self.root_dir.append(dir)

    def send_update(self):
        for directory in self.root_dir:
            directory.updater()

    def delete(self):
        os.remove(self.path)
        self.send_update()

    def rename(self, new_name):
        new_name = new_name + self.type
        os.rename(self.name, new_name)
        self.name = new_name

    def copy(self, new_folder):
        shutil.copy(self.path, new_folder.path)
        self.add_dir(new_folder)
        self.send_update()

    @abstractmethod
    def open(self):
        pass


class Photo(File):

    def open(self):
        file = Image.open(self.path)
        file.load()
        file.show()


class Music(File):

    def open(self):
        os.startfile(self.path)


class Video(File):

    def open(self):
        os.startfile(self.path)


class Document(File):

    def open(self):
        return DocEditor(self.path)


class Editor(ABC):

    def __init__(self, path):
        self.file_path = path
        self.file = None
        self.text = ''

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def save(self, text):
        pass

    @abstractmethod
    def close(self):
        pass


class DocEditor(Editor):

    def open(self):
        self.file = open(self.file_path, 'r')
        self.text = self.file.read()

    def save(self, text):
        with open(self.file_path, 'w') as file:
            file.write(text)

    def close(self):
        self.file.close()

    def max10(self, text):
        text = str(text)
        text = text.replace('\n', '')
        text = text.replace('\t', '')
        text = text.replace('.', '')
        text = text.replace('!', '')
        text = text.replace('?', '')
        text = text.replace('\"', '')
        text = text.replace(',', '')
        while '  ' in text:
            text = text.replace('  ', ' ')
        text = text.split(' ')
        text.sort(key=len, reverse=True)
        if len(text) > 10:
            top = text[:10:]
        else:
            top = text
        return top

    def clear_text(self, text):
        out = ''
        text = str(text)
        text = text.replace('\t', '')
        while '  ' in text:
            text = text.replace('  ', ' ')
        text = text.split('\n')
        for string in text:
            if string != ' ':
                out = out + string + '\n'
        return out


if __name__ == '__main__':
    d = Directory('C:\\Users\\BULALA\\Downloads\\Telegram Desktop', None)
    numb = pickle.dumps(d)
    print(numb)
    el = pickle.loads(numb)
    print(el.__dict__)