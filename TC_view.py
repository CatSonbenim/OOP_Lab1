import sys
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDir, QRegExp
import pymongo
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QAction
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor, QTextCursor
from pickle import loads


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.main_w = loadUi('MainWindow.ui')
        self.dir_chosen = None
        self.file_chosen = None
        mongo = pymongo.MongoClient()
        tc = mongo.FileSys
        self.f_sys = tc.file_sys
        self.initUI()


    def initUI(self):
        self.model = QFileSystemModel()
        self.model.setRootPath('E:')
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
            self.file_chosen = self.file_chosen.replace('/', '\\')
            print(self.file_chosen)
            file = self.f_sys.find_one({'path': self.file_chosen})
            file_obj = loads(file['obj'])
            editor = file_obj.open()
            if editor:
                self.open_editor(editor)
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

    def open_editor(self, obj):
        obj.open()
        self.exe = Editor(obj)



class Editor:

    def __init__(self, editor_obj):
        self.window = loadUi('DocEditor.ui')
        self.editor = editor_obj
        self.ui()

    def ui(self):
        self.window.text_bar.setPlainText(self.editor.text)
        self.window.clean.clicked.connect(self.clean)
        self.window.top.clicked.connect(self.top)
        self.window.save.clicked.connect(self.save)
        self.window.latin.clicked.connect(self.highlight)
        self.window.show()

    def clean(self):
        t = self.editor.clear_text(self.window.text_bar.toPlainText())
        self.window.text_bar.setPlainText(t)

    def top(self):
        text = ''
        t = self.editor.max10(self.window.text_bar.toPlainText())
        for i in range(len(t)):
            text = text + '    ' + str(i+1) + '. ' + t[i]
        self.window.label.setText(text)

    def save(self):
        self.editor.save(self.window.text_bar.toPlainText())
        self.window.label.setText('Saved!')

    def highlight(self):
        cursor = self.window.text_bar.textCursor()
        format = QTextCharFormat()
        format.setBackground(QBrush(QColor("blue")))
        pattern = "[a-zA-Z]+"
        regex = QRegExp(pattern)
        pos = 0
        index = regex.indexIn(self.window.text_bar.toPlainText(), pos)
        while index != -1:
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.EndOfWord, 1)
            cursor.mergeCharFormat(format)
            pos = index + regex.matchedLength()
            index = regex.indexIn(self.window.text_bar.toPlainText(), pos)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())