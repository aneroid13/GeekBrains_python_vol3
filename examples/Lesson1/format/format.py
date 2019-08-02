#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PyQt5.QtGui import QIcon, QFont


class Examp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        self.t_editor = QTextEdit()
        self.setCentralWidget(self.t_editor)

        our_bold = QAction(QIcon('b.jpg'),'Bold', self)
        our_bold.triggered.connect(self.actionBold)

        our_italic = QAction(QIcon('i.jpg'), 'Italic', self)
        our_italic.triggered.connect(self.actionItalic)

        our_underlined = QAction(QIcon('u.jpg'), 'Underlined', self)
        our_underlined.triggered.connect(self.actionUnderlined)

        tool_b = self.addToolBar('Formatting')
        tool_b.addAction(our_bold)
        tool_b.addAction(our_italic)
        tool_b.addAction(our_underlined)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.show()

    def actionBold(self):
        myFont = QFont()
        myFont.setBold(True)
        self.t_editor.setFont(myFont)

    def actionItalic(self):
        myFont = QFont()
        myFont.setItalic(True)
        self.t_editor.setFont(myFont)

    def actionUnderlined(self):
        myFont = QFont()
        myFont.setUnderline(True)
        self.t_editor.setFont(myFont)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Examp()
    sys.exit(app.exec_())
