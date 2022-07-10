import docx_file_parsing
import drop_OLX
import os
import sys
import MainWindow
import attributes
from PyQt5 import QtCore, QtGui, QtWidgets

class EmittingStream(QtCore.QObject):
    signal = QtCore.pyqtSignal(str)
    
    def __init__(self):
        super().__init__()

    def write(self, text):
        self.signal.emit(text)

class MainWindow_shell(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setObjectName("OpenEDX_converter")
        self.set_bindings()

    def set_bindings(self):
        self.dir_browse.clicked.connect(self.browse_dir)
        self.file_browse.clicked.connect(self.browse_file)
        self.convert.clicked.connect(self.start_convert)
        stream = EmittingStream()
        stream.signal.connect(self.add_to_TextBrowser)
        sys.stdout = stream
        sys.stderr = stream
        val = QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Z0-9_]{0,255}"))                 
        self.lineEdit_library.setValidator(val)
        self.lineEdit_org.setValidator(val)

    def __del__(self):
        sys.stdout = sys.__stdout__

    def add_to_TextBrowser(self, text):
        #self.textBrowser.append(text) It works strangely
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def browse_dir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        if directory != "":
            self.lineEdit_dir.setText(directory)

    def browse_file(self):
        file, filter = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл", "", "(*.docx)")
        if file != "":
            self.lineEdit_file.setText(file)

    def start_convert(self):
        library_library = self.lineEdit_library.text()
        library_display_name = self.lineEdit_display_name.text()
        library_org = self.lineEdit_org.text()
        library_use_latex_compiler = self.checkBox_use_latex_compiler.isChecked()
        library_show_correctness = self.comboBox_show_correctness.currentText()
        library_showanswer = self.comboBox_showanswer.currentText()
        library_rerandomize = self.comboBox_rerandomize.currentText()
        library_show_reset_button = self.checkBox_show_reset_button.isChecked()
        library_max_attempts = self.spinBox_max_attempts.value()

        questions_display_name = self.lineEdit_display_name_q.text()
        questions_show_correctness = self.comboBox_show_correctness_q.currentText()
        questions_showanswer = self.comboBox_showanswer_q.currentText()
        questions_rerandomize = self.comboBox_rerandomize_q.currentText()
        questions_max_attempts = self.spinBox_max_attempts_q.value()
        questions_weight = self.doubleSpinBox_weight_q.value()

        file = self.lineEdit_file.text()
        dir = self.lineEdit_dir.text()

        l_attr = attributes.library_attributes()
        q_attr = attributes.problem_attributes()

        if library_library != "":
            l_attr.library = library_library
        if library_display_name != "":
            l_attr.display_name = library_display_name
        if library_org != "":
            l_attr.org = library_org
        if library_use_latex_compiler:
            l_attr.use_latex_compiler = "True"
        else:
            l_attr.use_latex_compiler = "False"
        if library_show_correctness == "Всегда":
            l_attr.show_correctness = "always"
        elif library_show_correctness == "Никогда":
            l_attr.show_correctness = "never"
        if library_showanswer == "После завершения":
            l_attr.showanswer = "finished"
        if library_rerandomize == "Никогда":
            l_attr.rerandomize = "never"
        elif library_rerandomize == "Для каждого студента":
            l_attr.rerandomize = "per_student"
        if library_show_reset_button:
            l_attr.show_reset_button = "True"
        else:
            l_attr.show_reset_button = "False"
        if library_max_attempts == 0:
            l_attr.max_attempts = "null"
        else:
            l_attr.max_attempts = str(library_max_attempts)

        if questions_display_name != "":
            q_attr.display_name = questions_display_name
        if questions_show_correctness == "Всегда":
            q_attr.show_correctness = "always"
        elif questions_show_correctness == "Никогда":
            q_attr.show_correctness = "never"
        if questions_showanswer == "Никогда":
            q_attr.showanswer = "never"
        if questions_rerandomize == "Никогда":
            q_attr.rerandomize = "never"
        elif questions_rerandomize == "Для каждого студента":
            q_attr.rerandomize = "per_student"
        if questions_max_attempts == 0:
            q_attr.max_attempts = "null"
        else:
            q_attr.max_attempts = str(questions_max_attempts)
        q_attr.weight =  str(questions_weight)

        if os.path.exists(file) and os.path.exists(dir) and os.path.isfile(file) and os.path.isdir(dir):
            if file[-5 : ] == ".docx":
                lib, problems, problems_names = docx_file_parsing.parse_file(file, l_attr, q_attr)
                drop_OLX.drop_files(dir, lib, problems, problems_names)
            else:
                print("This is not docx file.")
        else:
            print("Path to file or directory incorrect.")

app = QtWidgets.QApplication(sys.argv)
window = MainWindow_shell()
window.show()
app.exec_()


#while True:
#    test_path = input('Enter the full name of the source file (with extension and path): ')
#    if os.path.exists(test_path):
#        if os.path.isfile(test_path):
#            if test_path[-5 : ] == ".docx":
#                lib, problems = sourсe_file_parsing.parse_file(test_path)
#                #C:\Users\User\Desktop\Сем 6\Практика\Исходники\Auto-Graded Practice Quiz.docx
#                #C:\Users\User\Desktop\Сем 6\Практика\test\ВсеТипы.docx
#                break
#            else:
#                print("This is not docx file.")
#        else:
#            print("This is not file.")
#    else:
#        print("Path incorrect.")
#while lib != "":
#    directory_path = input('Enter the path to the directory where the resulting files will be placed: ')
#
#    if os.path.exists(directory_path):
#        if os.path.isdir(directory_path):
#            drop_OLX.drop_files(directory_path, lib, problems)
#            #C:\Users\User\Desktop\Сем 6\Практика\test
#            break
#        else:
#            print("This is not directory.")
#    else:
#        print("Path incorrect.")