#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class TextEditor(QMainWindow):

    def __init__(self):
        super().__init__()
        # self.initUI()
        self.mainWindow()

    def initUI(self):
        self.setWindowTitle('QNotatnik')
        self.resize(600, 400)
        self.statusBar()
        self.text = QTextEdit()
        self.fileName = ''

        self.initMenuBar()
        self.initToolBar()
        self.initLayout()

        self.leftSideWidget()
        self.rightSideWidget()
        self.show()

    def mainWindow(self):
        self.setWindowTitle('Menu')
        self.resize(600, 400)
        self.statusBar()
        button = QPushButton('PyQt5 button', self)
        button.setToolTip('Open Editor')
        button.move(500, 30)
        button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        self.initUI()

    def initMenuBar(self):
        menubar = self.menuBar()
        self.menuFile = menubar.addMenu('&Plik')
        menubar.addAction(self.menuFile.menuAction())
        self.createMenuFile()

        self.menuEdit = menubar.addMenu('&Edycja')
        menubar.addAction(self.menuEdit.menuAction())
        self.createMenuEdit()

    def createMenuFile(self):
        nowy = QAction('Nowy', self)
        self.menuFile.addAction(nowy)
        nowy.triggered.connect(lambda: self.newFile())

        otworz = QAction('Otwórz', self)
        self.menuFile.addAction(otworz)
        otworz.triggered.connect(lambda: self.openFile())

        zapisz = QAction('Zapisz', self)
        self.menuFile.addAction(zapisz)
        zapisz.triggered.connect(lambda: self.saveFile(1))

        zapiszJ = QAction('Zapisz jako...', self)
        self.menuFile.addAction(zapiszJ)
        zapiszJ.triggered.connect(lambda: self.saveFile(2))

        koniec = QAction('Koniec', self)
        self.menuFile.addAction(koniec)
        koniec.triggered.connect(self.close)

    def newFile(self):
        self.text.clear()
        self.fileName = ""
        self.statusBar().showMessage('Tworzenie nowego pliku')

    def openFile(self):
        filename = QFileDialog.getOpenFileName(self, str("Open File"), os.getenv('HOME'), str("Text Files(*.txt)"))
        self.fileName = filename[0]
        self.statusBar().showMessage('Otwieranie pliku')
        with open(self.fileName, 'r') as f:
            file_text = f.read()
            self.text.setText(file_text)

    def saveFile(self, val):
        if val == 2 or (val == 1 and self.fileName == ""):
            filename = QFileDialog.getSaveFileName(self, str("Save File"), os.getenv('HOME'), str("Text Files(*.txt)"))
            self.fileName = filename[0]
        self.statusBar().showMessage('Zapisywanie pliku')
        with open(self.fileName, 'w') as f:
            my_text = self.text.toPlainText()
            f.write(my_text)

    def createMenuEdit(self):
        wytnij = QAction('Wytnij', self)
        wytnij.setShortcut('Ctrl+X')
        self.menuEdit.addAction(wytnij)
        wytnij.triggered.connect(lambda: self.text.cut())
        wytnij.triggered.connect(lambda: self.statusBar().showMessage('Wycinanie tekstu'))

        kopiuj = QAction('Kopiuj', self)
        kopiuj.setShortcut('Ctrl+C')
        self.menuEdit.addAction(kopiuj)
        kopiuj.triggered.connect(lambda: self.text.copy())
        kopiuj.triggered.connect(lambda: self.statusBar().showMessage('Kopiowanie tekstu'))

        wklej = QAction('Wklej', self)
        wklej.setShortcut('Ctrl+V')
        self.menuEdit.addAction(wklej)
        wklej.triggered.connect(lambda: self.text.paste())
        wklej.triggered.connect(lambda: self.statusBar().showMessage('Wklejanie tekstu'))

        zaznacz = QAction('Zaznacz wszystko', self)
        zaznacz.setShortcut('Ctrl+A')
        self.menuEdit.addAction(zaznacz)
        zaznacz.triggered.connect(lambda: self.text.selectAll())
        zaznacz.triggered.connect(lambda: self.statusBar().showMessage('Zaznaczanie calego tekstu'))

    def initToolBar(self):
        self.toolbar = self.addToolBar('toolBar')
        for i in range(1, 10):
            self.toolbar.addAction(QAction(QIcon(str(i) + '.png'), str(i), self))

    def initLayout(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        self.mainLayout = QHBoxLayout()
        centralWidget.setLayout(self.mainLayout)

    def leftSideWidget(self):
        leftLayout = QVBoxLayout(self)
        self.mainLayout.addLayout(leftLayout)
        self.fontGroup = QButtonGroup()
        self.fontColors = QButtonGroup()

        fontSize = QComboBox(self)
        fontSize.addItems(['40', '30', '20', '10', '5'])
        leftLayout.addWidget(fontSize)
        fontSize.currentIndexChanged.connect(lambda: self.textSettings(fontSize, self.fontGroup.checkedButton()))

        fonts = [QRadioButton('Times New Roman'), QRadioButton('Arial'), QRadioButton('Courier New')]
        for i in range(3):
            if i == 0:
                fonts[i].setChecked(True)
            fonts[i].toggled.connect(lambda: self.textSettings(fontSize, self.fontGroup.checkedButton()))
            self.fontGroup.addButton(fonts[i], i)
            leftLayout.addWidget(fonts[i])

        gridColors = QGridLayout(self)
        leftLayout.addLayout(gridColors)
        colors = ['blue', 'red', 'brown', 'green', 'black', 'pink', 'white', 'yellow', 'purple']
        positions = [(i, j) for i in range(3) for j in range(3)]

        buttons = []
        i = 0
        for position, color in zip(positions, colors):
            button = QPushButton()
            buttons.append(button)
            i = i + 1
            self.fontColors.addButton(button, i)
            button.setStyleSheet("background-color: " + str(color))
            gridColors.addWidget(button, *position)

        buttons[0].clicked.connect(lambda: self.textColor(buttons[0]))
        buttons[1].clicked.connect(lambda: self.textColor(buttons[1]))
        buttons[2].clicked.connect(lambda: self.textColor(buttons[2]))
        buttons[3].clicked.connect(lambda: self.textColor(buttons[3]))
        buttons[4].clicked.connect(lambda: self.textColor(buttons[4]))
        buttons[5].clicked.connect(lambda: self.textColor(buttons[5]))
        buttons[6].clicked.connect(lambda: self.textColor(buttons[6]))
        buttons[7].clicked.connect(lambda: self.textColor(buttons[7]))
        buttons[8].clicked.connect(lambda: self.textColor(buttons[8]))

    def textSettings(self, size, type):
        font = QtGui.QFont(type.text(), int(size.currentText()))
        self.text.setFont(font)
        self.statusBar().showMessage('Zmiana rozmiaru lub czcionki')

    def textColor(self, color):
        tmp = color.palette().button().color()
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Base, tmp)
        self.text.setPalette(palette)
        self.statusBar().showMessage('Zmiana koloru tekstu')

    def rightSideWidget(self):
        self.mainLayout.addWidget(self.text)
        font = QtGui.QFont("Times New Roman", 40)
        self.text.setFont(font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextEditor()
    sys.exit(app.exec_())
