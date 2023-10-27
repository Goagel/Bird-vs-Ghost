from PyQt5.QtCore import Qt, QTimer, QTime, QLocale
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QFont
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QHBoxLayout, QVBoxLayout, QGridLayout, 
        QGroupBox, QRadioButton,
        QPushButton, QLabel, QListWidget, QLineEdit)


from labirint import *

class MainWin(QWidget):
    def __init__(self):
        # the window which the greeting is located in:
        super().__init__()

        #apelarea metodei care creaza si configureaza elementele grafice:
        self.initUI()
        
        #apelul metodei care leaga partea vizuala (exemplu butonul) de partea functionala (functia care se executa la apasarea butonului):
        self.connects()

        # sets the window appearance (label, size, location):
        self.set_appear()
        
        # start:
        self.show()

    # crearea, configurarea si adaugarea in interfata a elementelor graficeprecum texte si butoane:
    def initUI(self):
        self.btn_play = QPushButton('Play')
        self.title_text = QLabel('Bird Vs Ghost')


        self.layout_line = QVBoxLayout()
        self.layout_line.addWidget(self.title_text, alignment = Qt.AlignCenter)
        self.layout_line.addWidget(self.btn_play, alignment = Qt.AlignCenter)      
        self.setLayout(self.layout_line)


def play_click(self):
        self.tw = TestWin()
        self.hide()
    
def connects(self):
        self.btn_play.clicked.connect(self.play_click)
       
def set_appear(self):
        self.setWindowTitle('Bird vs Ghost')
        self.resize(1000, 600)
        self.move(200, 100)

app = QApplication([])
mw = MainWin()
app.exec_()