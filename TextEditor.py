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
        self.button = QPushButton('Start', self)
        self.button.setToolTip('Open Editor')
        self.button.move(250, 30)
        self.button.clicked.connect(self.on_click)

        self.button2 = QPushButton('Open Calculator', self)
        self.button2.move(250, 90)
        self.button2.clicked.connect(self.open_new_window)

        self.button3 = QPushButton('Algorithm NN', self)
        self.button3.move(250, 150)
        self.button3.clicked.connect(self.open_nn_window)


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

    def open_nn_window(self):
        self.button.hide()
        self.button2.hide()
        self.button3.hide()
        self.window = QtWidgets.QMainWindow()
        self.window.resize(600, 400)
        self.setWindowTitle('NN')
        self.getValues();
        self.show()
        #self.window.show()

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

    def getValues(self):
        df = pd.read_csv("C:/Users/pa-wo/Desktop/Praca/Projekty Programistyczne/Text-Editor/leaf.csv", header=None)
        data = df[(df[0] == 3) | (df[0] == 5)]
        train, test = train_test_split(data.copy(), test_size=0.2, random_state=123)
        print(train[5])
        plt.scatter(x=train[2], y=train[5])
        a = train[2].tolist()
        b = train[5].tolist()
        cols = []
        for l in train[0]:
            if l == 5:
                cols.append(False)
            else:
                cols.append(True)
        cmap = {False: (0, 0, 200), True: (255, 255, 0)}
        brushes = [pg.mkBrush(cmap[x]) for x in cols]
        pg.plot(a, b, pen=None, symbol='o', symbolBrush=brushes)

#Main Function
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextEditor()
    sys.exit(app.exec_())

