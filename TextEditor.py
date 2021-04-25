#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from pyqtgraph.canvas import Canvas
from scipy.spatial import distance
from sklearn.model_selection import train_test_split
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import pyqtgraph as pg
import Second

class TextEditor(QMainWindow):

    def __init__(self):
        super().__init__()
        #self.initUI()
        self.mainWindow()
    
    def initUI(self):
        self.setWindowTitle('QNotatnik')
        self.resize(600,400)
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
        # self.button = QPushButton('Start', self)
        # self.button.setToolTip('Open Editor')
        # self.button.move(250, 30)
        # self.button.clicked.connect(self.on_click)

        self.button2 = QPushButton('Open Calculator', self)
        self.button2.move(250, 90)
        self.button2.clicked.connect(self.open_new_window)

        self.button3 = QPushButton('GCD algorithm', self)
        self.button3.move(250, 150)
        self.button3.clicked.connect(self.open_gcd_window)

        self.button3 = QPushButton('Bishop Position', self)
        self.button3.move(250, 210)
        self.button3.clicked.connect(self.open_bi_window)

        self.show()

#Otwiera nowe okno i tutaj funkcje masz dawac
    def open_new_window(self):
        self.button.hide()
        self.button2.hide()
        self.button3.hide()
        self.window = QtWidgets.QMainWindow()
        self.window.resize(600, 400)
        self.setWindowTitle('Kalkulator')
        self.initMenu()
        self.initLayout()
        self.initLCD()
        self.initButtons()
        self.show()
        #self.window.show()

    def open_gcd_window(self):
        # self.button.hide()
        # self.button2.hide()
        # self.button3.hide()
        self.window = QtWidgets.QMainWindow()
        self.window.resize(600, 400)
        self.setWindowTitle('GCD')
        a, okPressed = QInputDialog.getText(self, "Get a", "Your position:", QLineEdit.Normal, "")
        b, okPressed = QInputDialog.getText(self, "Get b", "Your position:", QLineEdit.Normal, "")
        if okPressed and a != '' and b != '':
            print(self.getGCD(int(a),int(b)));
        self.show()
        #self.window.show()

    def open_bi_window(self):
        self.window = QtWidgets.QMainWindow()
        self.window.resize(600, 400)
        self.setWindowTitle('Bishop')
        text, okPressed = QInputDialog.getText(self, "Get text", "Your position:", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.getPositionsOfBishop(text);
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
        nowy.triggered.connect(lambda:self.newFile())

        otworz = QAction('Otwórz', self)
        self.menuFile.addAction(otworz)
        otworz.triggered.connect(lambda:self.openFile())

        zapisz = QAction('Zapisz', self)
        self.menuFile.addAction(zapisz)
        zapisz.triggered.connect(lambda:self.saveFile(1))

        zapiszJ = QAction('Zapisz jako...', self)
        self.menuFile.addAction(zapiszJ)
        zapiszJ.triggered.connect(lambda:self.saveFile(2))

        koniec = QAction('Koniec', self)
        self.menuFile.addAction(koniec)
        koniec.triggered.connect(self.close)

    def newFile(self):
        self.text.clear()
        self.fileName =""
        self.statusBar().showMessage('Tworzenie nowego pliku')

    def openFile(self):
        filename = QFileDialog.getOpenFileName(self, str("Open File"), os.getenv('HOME'),str("Text Files(*.txt)"))
        self.fileName = filename[0]
        self.statusBar().showMessage('Otwieranie pliku')
        with open(self.fileName, 'r') as f:
            file_text = f.read()
            self.text.setText(file_text)

    def saveFile(self,val):
        if val == 2 or (val == 1 and self.fileName == ""):
            filename = QFileDialog.getSaveFileName(self, str("Save File"), os.getenv('HOME'),str("Text Files(*.txt)"))
            self.fileName = filename[0]
        self.statusBar().showMessage('Zapisywanie pliku')   
        with open(self.fileName, 'w') as f:
            my_text = self.text.toPlainText()
            f.write(my_text)        

    def createMenuEdit(self):
        wytnij = QAction('Wytnij', self)
        wytnij.setShortcut('Ctrl+X')
        self.menuEdit.addAction(wytnij)
        wytnij.triggered.connect(lambda:self.text.cut())
        wytnij.triggered.connect(lambda:self.statusBar().showMessage('Wycinanie tekstu'))

        kopiuj = QAction('Kopiuj', self)
        kopiuj.setShortcut('Ctrl+C')
        self.menuEdit.addAction(kopiuj)
        kopiuj.triggered.connect(lambda:self.text.copy())
        kopiuj.triggered.connect(lambda:self.statusBar().showMessage('Kopiowanie tekstu'))

        wklej = QAction('Wklej', self)
        wklej.setShortcut('Ctrl+V')
        self.menuEdit.addAction(wklej)
        wklej.triggered.connect(lambda:self.text.paste())
        wklej.triggered.connect(lambda:self.statusBar().showMessage('Wklejanie tekstu'))

        zaznacz = QAction('Zaznacz wszystko', self)
        zaznacz.setShortcut('Ctrl+A')
        self.menuEdit.addAction(zaznacz)
        zaznacz.triggered.connect(lambda:self.text.selectAll())
        zaznacz.triggered.connect(lambda:self.statusBar().showMessage('Zaznaczanie calego tekstu'))

    def initToolBar(self):
        self.toolbar = self.addToolBar('toolBar')
        for i in range(1,10):
            self.toolbar.addAction(QAction(QIcon(str(i)+'.png'), str(i), self))

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
        fontSize.addItems(['40','30','20','10','5'])
        leftLayout.addWidget(fontSize)
        fontSize.currentIndexChanged.connect(lambda:self.textSettings(fontSize,self.fontGroup.checkedButton()))
        
        fonts = [QRadioButton('Times New Roman'),QRadioButton('Arial'),QRadioButton('Courier New')]
        for i in range(3):
            if i == 0:
                fonts[i].setChecked(True)
            fonts[i].toggled.connect(lambda:self.textSettings(fontSize,self.fontGroup.checkedButton()))
            self.fontGroup.addButton(fonts[i],i)
            leftLayout.addWidget(fonts[i])

        gridColors = QGridLayout(self)
        leftLayout.addLayout(gridColors)
        colors = ['blue','red','brown','green','black','pink','white','yellow','purple']
        positions = [(i,j) for i in range(3) for j in range(3)]

        buttons = []
        i=0
        for position, color in zip(positions, colors):
            button = QPushButton()
            buttons.append(button)
            i=i+1
            self.fontColors.addButton(button,i)
            button.setStyleSheet("background-color: "+ str(color))
            gridColors.addWidget(button,*position)
        
        buttons[0].clicked.connect(lambda:self.textColor(buttons[0]))
        buttons[1].clicked.connect(lambda:self.textColor(buttons[1]))
        buttons[2].clicked.connect(lambda:self.textColor(buttons[2]))
        buttons[3].clicked.connect(lambda:self.textColor(buttons[3]))
        buttons[4].clicked.connect(lambda:self.textColor(buttons[4]))
        buttons[5].clicked.connect(lambda:self.textColor(buttons[5]))
        buttons[6].clicked.connect(lambda:self.textColor(buttons[6]))
        buttons[7].clicked.connect(lambda:self.textColor(buttons[7]))
        buttons[8].clicked.connect(lambda:self.textColor(buttons[8]))

    def textSettings(self,size,type):
        font = QtGui.QFont(type.text(),int(size.currentText()))
        self.text.setFont(font)
        self.statusBar().showMessage('Zmiana rozmiaru lub czcionki')

    def textColor(self,color):
        tmp = color.palette().button().color()
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Base, tmp)
        self.text.setPalette(palette)
        self.statusBar().showMessage('Zmiana koloru tekstu')

    def rightSideWidget(self):
        self.mainLayout.addWidget(self.text)
        font = QtGui.QFont("Times New Roman",40)
        self.text.setFont(font)

    #Functions For Calculator
    def initMenu(self):
        menubar = self.menuBar()
        #tworzymy ikonki z domyslnymi pozycjami
        menubar.addMenu('&Widok')
        menubar.addMenu('&Edycja')
        menubar.addMenu('&Pomoc')
        #zeby znikalo po kliknieciu
        menubar.setNativeMenuBar(False)

    def initLayout(self):
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        self.mainLayout = QGridLayout()
        centralWidget.setLayout(self.mainLayout)

    def initLCD(self):
        #ustawiamy LCD
        lcd = QLCDNumber()
        #jego wielkosc
        lcd.setMinimumHeight(100)
        #oraz jego pozycje
        self.mainLayout.addWidget(lcd, 0, 0, 3 , 5)

    def initButtons(self):
        #nazwy buttonow
        names = ['MC', 'MR', 'MS', 'M+', 'M-',
                '←', 'CE', 'C', '+/-', '√',
                '7', '8', '9','/','%',
                '4', '5', '6','*','1/x',
                 '1', '2', '3','-','=',
                '0','', ',', '+','']
 
        #ustawienie pozycji buttonow w jakiej mają być
        positions = [(i+3,j) for i in range(9) for j in range(5)]

        for position, name in zip(positions, names):

            #jezeli brak anzwy to continue
            if name == '':
                continue
            #pobieramy nazwe i ustawiamy szerokosc
            button = QPushButton(name)
            button.setMinimumWidth(30)
            #ustawiamy zeby sie rozciagal
            button.setSizePolicy( QSizePolicy.Preferred, QSizePolicy.Minimum)
            if name == '0':
                #ustawiamy wielkosc i pozycje
                #1,2 oznacza ze albo zlaczony albo nie
                self.mainLayout.addWidget(button, 8,0,1,2)
            elif name == '=':
                self.mainLayout.addWidget(button, 7,4,2,1)
            else:
                #jak nie to pojedynczy kwadracik
                self.mainLayout.addWidget(button, *position)

    def getGCD(self, a, b):
        return self.hcfnaive(a, b)

    def hcfnaive(self, a, b):
        if (b == 0):
            return a
        else:
            return self.hcfnaive(b, a % b)

    def getPositionsOfBishop(self, position):
        startPosition = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
            "g": 7,
            "h": 8
        }
        finalPositions = {
            1: "a",
            2: "b",
            3: "c",
            4: "d",
            5: "e",
            6: "f",
            7: "g",
            8: "h",
        }
        b1 = [char for char in position]
        x0 = startPosition[b1[0]]
        y0 = int(b1[1])

        x = x0
        y = y0
        lista = []

        while x >= 1 and y >= 1:
            if (x != x0 and y != y0):
                lista.append((finalPositions[x], y))
            x -= 1
            y -= 1

        x = x0
        y = y0

        while x <= 8 and y <= 8:
            if (x != x0 and y != y0):
                lista.append((finalPositions[x], y))
            x += 1
            y += 1

        x = x0
        y = y0

        while x <= 8 and y >= 1:
            if (x != x0 and y != y0):
                lista.append((finalPositions[x], y))
            x += 1
            y -= 1

        x = x0
        y = y0

        while x >= 1 and x <= 8:
            if (x != x0 and y != y0):
                lista.append((finalPositions[x], y))
            x -= 1
            y += 1

        print(lista)


#Main Function
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextEditor()
    sys.exit(app.exec_())

