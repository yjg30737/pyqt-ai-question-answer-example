from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QGuiApplication, QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QFormLayout, QLineEdit, QGroupBox, QVBoxLayout, QTextEdit, QWidget, \
    QApplication, QTextBrowser, QFrame, QLabel, QPushButton

from src.huggingFaceModelWidget import HuggingFaceModelWidget
from src.script import getAnswer

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support
# qt version should be above 5.14
QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

QApplication.setFont(QFont('Arial', 12))

QApplication.setWindowIcon(QIcon('hf-logo.svg'))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__current_model_prefix = 'Selected Model:'

    def __initUi(self):
        self.setWindowTitle('PyQt Using Question-Answering model example')
        self.__huggingFaceModelWidget = HuggingFaceModelWidget(['deepset/roberta-base-squad2', 'deepset/tinyroberta-squad2'])
        self.__huggingFaceModelWidget.onModelSelected.connect(self.__onModelSelected)

        self.__questionLineEdit = QLineEdit()
        self.__questionLineEdit.textChanged.connect(self.__textChanged)
        self.__contextLineEdit = QLineEdit()
        self.__contextLineEdit.textChanged.connect(self.__textChanged)

        self.__answerBrowser = QTextBrowser()

        lay = QFormLayout()
        lay.addRow('Question', self.__questionLineEdit)
        lay.addRow('Context', self.__contextLineEdit)

        topGrpBox = QGroupBox()
        topGrpBox.setTitle('Question')
        topGrpBox.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(self.__answerBrowser)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)

        bottomGrpBox = QGroupBox()
        bottomGrpBox.setTitle('Answer')
        bottomGrpBox.setLayout(lay)

        self.__currentModelLbl = QLabel()
        self.__currentModelLbl.setText(f'{self.__current_model_prefix} {self.__huggingFaceModelWidget.getCurrentModelName()}')

        self.__submitBtn = QPushButton('Submit')
        self.__submitBtn.clicked.connect(self.__submit)
        self.__submitBtn.setEnabled(False)

        lay = QVBoxLayout()
        lay.addWidget(self.__huggingFaceModelWidget)
        lay.addWidget(sep)
        lay.addWidget(self.__currentModelLbl)
        lay.addWidget(topGrpBox)
        lay.addWidget(self.__submitBtn)
        lay.addWidget(bottomGrpBox)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)
        self.setCentralWidget(mainWidget)

    def __onModelSelected(self, cur_model_name):
        self.__currentModelLbl.setText(f'{self.__current_model_prefix} {cur_model_name}')

    def __textChanged(self, text):
        f = self.__questionLineEdit.text().strip() != '' and self.__contextLineEdit.text().strip() != ''
        self.__submitBtn.setEnabled(f)
        
    def __submit(self):
        model_class = self.__huggingFaceModelWidget.getCurrentModelObject()
        model_name = self.__huggingFaceModelWidget.getCurrentModelName()
        question = self.__questionLineEdit.text()
        context = self.__contextLineEdit.text()
        answer = getAnswer(model_class, model_name, question, context)
        self.__answerBrowser.setText(answer['answer'])



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

