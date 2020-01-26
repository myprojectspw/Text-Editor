from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Second(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'MyApp'
        self.left, self.top, self.width, self.height = 10, 10, 800, 800
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Create textbox for index number 1
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Insert something:')
        self.nameLabel.move(20, 80)

        self.textbox_index1 = QLineEdit(self)
        self.textbox_index1.move(20, 100)
        self.textbox_index1.resize(280, 40)

        # Create a button in the window
        self.buttonC1 = QPushButton('Clear', self)
        self.buttonC1.move(300, 119)

        # connect buttons "CLEAR" to function
        self.buttonC1.clicked.connect(self.textbox_index1.clear)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())