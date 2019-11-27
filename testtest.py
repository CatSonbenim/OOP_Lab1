import sys
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDir, QFile

from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QAction
from PyQt5.QtGui import QIcon


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.main_w = loadUi('MainWindow.ui')
        self.dir_chosen = None
        self.file_chosen = None
        self.initUI()


    def initUI(self):
        self.model = QFileSystemModel()
        self.model.setRootPath('home')
        self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
        self.main_w.Dirs.setModel(self.model)
        self.main_w.Dirs.doubleClicked.connect(self.choose_dir)
        self.main_w.Files.doubleClicked.connect(self.choose_file)
        self.main_w.Dirs.setAnimated(False)
        self.main_w.Dirs.setIndentation(20)
        self.main_w.Dirs.setSortingEnabled(True)
        self.main_w.Dirs.setRootIndex(self.model.index(self.model.rootPath()))
        self.main_w.Dirs.keyPressEvent = self.keyPressEvent_dir
        self.main_w.Files.keyPressEvent = self.keyPressEvent_file
        self.main_w.create_dir.clicked.connect(self.create_dir)
        self.main_w.create_file.clicked.connect(self.create_file)
        self.main_w.copy_dir.clicked.connect(self.copy_dir)
        self.main_w.copy_file.clicked.connect(self.copy_file)
        self.main_w.rename_dir.clicked.connect(self.rename_dir)
        self.main_w.rename_file.clicked.connect(self.rename_file)
        self.main_w.delete_dir.clicked.connect(self.delete_dir)
        self.main_w.delete_file.clicked.connect(self.delete_file)
        self.main_w.show()

    def keyPressEvent_dir(self, e):
        if e.key() == 16777220:
            path = self.dir_chosen
            self.files = QFileSystemModel()
            self.files.setRootPath(path)
            self.files.setFilter(QDir.Files)
            self.main_w.Files.setModel(self.files)
            self.main_w.Files.setRootIndex(self.files.index(path))
            print(path)

    def keyPressEvent_file(self, e):
        if e.key() == 16777220:
            print('Opened file %s' % self.file_chosen)

    def choose_dir(self, signal):
        self.dir_chosen = self.main_w.Dirs.model().filePath(signal)
        print(self.dir_chosen)

    def choose_file(self, signal):
        self.file_chosen = self.main_w.Files.model().filePath(signal)
        print(self.file_chosen)

    def create_dir(self):
        pass

    def create_file(self):
        pass

    def copy_dir(self):
        pass

    def copy_file(self):
        pass

    def rename_dir(self):
        pass

    def rename_file(self):
        pass

    def delete_dir(self):
        pass

    def delete_file(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
