import sys
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDir, QRegExp
import pymongo
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QWidget, QInputDialog, QAction, QMessageBox, QFileDialog
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor, QTextCursor
from pickle import loads, dumps
from TC_model import DocEditor, HTMLEditor
from TC_controller import *


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
        print(self.new_dirname())

    def create_file(self):
        print(self.new_filename())

    def copy_dir(self):
        new_dir = self.dir_copy()
        file = self.f_sys.find_one({'path': self.dir_chosen})['obj']
        obj = loads(file)
        signal = obj.copy(new_dir)
        print(signal)
        if signal:
            self.model = QFileSystemModel()
            self.model.setRootPath('E:')
            self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
            self.main_w.Dirs.setModel(self.model)
            self.main_w.Dirs.setRootIndex(self.model.index(self.model.rootPath()))
            self.main_w.show()
        e = Directory(signal, None)
        self.f_sys.insert_one({'path': signal, 'obj': dumps(e)})
        folder_recursion(signal, e, self.f_sys)

    def copy_file(self):
        new_dir = self.dir_copy()
        file = self.f_sys.find_one({'path': self.file_chosen})['obj']
        new_r = self.f_sys.find_one({'path': new_dir})['obj']
        obj = loads(file)
        new_root_dir = loads(new_r)
        signal = obj.copy(new_dir)
        if signal:
            self.model = QFileSystemModel()
            self.model.setRootPath('E:')
            self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
            self.main_w.Dirs.setModel(self.model)
            self.main_w.Dirs.setRootIndex(self.model.index(self.model.rootPath()))
            self.main_w.show()
        folder_recursion(new_dir, new_root_dir.root_dir, self.f_sys)


    def rename_dir(self):
        newname = self.new_dirname()
        file = self.f_sys.find_one({'path': self.dir_chosen})['obj']
        obj = loads(file)
        signal = obj.rename(newname)
        print(signal)
        if signal:
            self.model = QFileSystemModel()
            self.model.setRootPath('E:')
            self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
            self.main_w.Dirs.setModel(self.model)
            self.main_w.Dirs.setRootIndex(self.model.index(self.model.rootPath()))
            self.main_w.show()
        self.f_sys.insert_one({'path': signal, 'obj': dumps(obj)})
        folder_recursion(signal, obj.root_dir, self.f_sys)


    def rename_file(self):
        newname = self.new_filename()
        file = self.f_sys.find_one({'path': self.file_chosen})['obj']
        obj = loads(file)
        try:
            signal = obj.rename(newname)
        except PermissionError:
            self.msg = QMessageBox()
            self.msg.setText("Warning!")
            self.msg .setInformativeText("You can not rename thi file because it's editing")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
            return None
        if signal:
            self.model = QFileSystemModel()
            self.model.setRootPath('E:')
            self.model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot)
            self.main_w.Dirs.setModel(self.model)
            self.main_w.Dirs.setRootIndex(self.model.index(self.model.rootPath()))
            self.main_w.show()
        self.f_sys.insert_one({'path': signal, 'obj': dumps(obj)})


    def delete_dir(self):
        pass

    def delete_file(self):
        pass

    def open_editor(self, obj):
        obj.open()
        if isinstance(obj, DocEditor):
            self.exe = Editor(obj)
        elif isinstance(obj, HTMLEditor):
            self.ex = HTMLeditor(obj)

    def new_filename(self):
        text, ok = QInputDialog.getText(self, 'Filename', 'Enter file name:')
        if ok:
            return text

    def new_dirname(self):
        text, ok = QInputDialog.getText(self, 'Dirname', 'Enter directory name:')
        if ok:
            return text

    def dir_copy(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.DirectoryOnly)
        dlg.ShowDirsOnly = True
        dlg.setFilter(QDir.AllDirs)
        return dlg.getExistingDirectory()


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
            text = text + '    ' + str(i + 1) + '. ' + t[i]
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


class HTMLeditor:

    def __init__(self, editor_obj):
        self.window = loadUi('HTMLEditor.ui')
        self.editor = editor_obj
        self.ui()

    def ui(self):
        self.window.code.setPlainText(self.editor.text)
        self.window.save.clicked.connect(self.save)
        self.window.simpl.clicked.connect(self.simpl)
        self.window.show()

    def save(self):
        self.editor.save(self.window.code.toPlainText())
        self.window.label.setText('Saved!')

    def simpl(self):
        simplif = self.editor.simplify(self.window.code.toPlainText())
        self.window.code.setPlainText(simplif)
        self.window.label.setText('Simplified.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
