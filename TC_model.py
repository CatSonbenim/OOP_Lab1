import os
import time
import shutil
from abc import ABC, abstractmethod
import pickle
from bs4 import BeautifulSoup

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
        return file.path

    def add_dir(self, dir):
        self.root_dir.append(dir)

    def send_update(self):
        for directory in self.root_dir:
            return directory.updater(self)

    def rename(self, new_name):
        os.rename(self.path, self.root_dir_path + new_name)
        self.name = new_name
        self.path = self.root_dir_path + new_name
        return self.send_update()

    def copy(self, new_folder):
        new = shutil.copytree(self.path, new_folder + '/' + self.name)
        return new

    def new_dir(self, name):
        os.mkdir(self.path + '/' + name)
        return self.path + '/' + name

    def new_file(self, name):
        open(self.path + '/' + name, 'tw', encoding='utf-8').close()
        return self.path + '/' + name

    def del_file(self, file):
        os.remove(file)
        return self.path

    def del_dir(self):
        for file in os.listdir(self.path):
            os.remove(self.path + '/' + file)
        os.rmdir(self.path)
        return self.root_dir_path


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
           return directory.updater(self)

    def rename(self, new_name):
        new_name = new_name + '.' + self.type
        os.rename(self.path, self.root_dir_path + '/' + new_name)
        self.path = self.root_dir_path + '/' + new_name
        self.name = new_name
        return self.send_update()

    def copy(self, new_folder):
        new = shutil.copy(self.path, new_folder)
        return new

    @abstractmethod
    def open(self):
        pass


class Other(File):

    def open(self):
        os.startfile(self.path)
        return None


class Document(File):

    def open(self):
        return DocEditor(self.path)


class HTML(File):
    def open(self):
        return HTMLEditor(self.path)


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
        text = text.replace('\n', ' ')
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
        text_list = []
        for string in text:
            if string != '':
                text_list.append(string)
        if len(text) > 10:
            top = text_list[:10:]
        else:
            top = text_list
        return top

    def clear_text(self, text):
        out = ''
        text = text.replace('\t', '')
        while '  ' in text:
            text = text.replace('  ', ' ')
        text = text.split('\n')
        for string in text:
            if string != ' ' and string != '':
                out = out + string + '\n'
        return out


class HTMLEditor(Editor):

    def open(self):
        self.file = open(self.file_path, 'r')
        self.text = self.file.read()

    def save(self, text):
        with open(self.file_path, 'w') as file:
            file.write(text)

    def close(self):
        self.file.close()

    def simplify(self, text, whitelist=tuple()):
        soup = BeautifulSoup(text, "html.parser")
        for tag in soup.findAll(True):
            for attr in [attr for attr in tag.attrs if attr not in whitelist]:
                del tag[attr]
        return soup.prettify().__str__()


if __name__ == '__main__':
    d = Directory('C:\\Users\\BULALA\\Downloads\\Telegram Desktop', None)
    numb = pickle.dumps(d)
    print(numb)
    el = pickle.loads(numb)
    print(el.__dict__)