#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PyQt5.QtGui import QIcon, QFont, QPixmap


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


        self.t_editor = QTextEdit()

        self.setCentralWidget(self.t_editor)

        smile = QAction(QIcon('ab.gif'),'Smile', self)
        smile.triggered.connect(self.actionSmile)

        melancholy = QAction(QIcon('ac.gif'), 'Melancholy', self)
        melancholy.triggered.connect(self.actionMelancholy)

        surprise = QAction(QIcon('ai.gif'), 'Surprise', self)
        surprise.triggered.connect(self.actionSurprise)

        toolbar = self.addToolBar('Formatting')
        toolbar.addAction(smile)
        toolbar.addAction(melancholy)
        toolbar.addAction(surprise)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.show()

    def actionSmile(self):
        url = 'ab.gif'
        self.t_editor.setHtml('<img src="%s" />' % url)

    def actionMelancholy(self):
        url = 'ac.gif'
        self.t_editor.setHtml('<img src="%s" />' % url)

    def actionSurprise(self):
        url = 'ai.gif'
        self.t_editor.setHtml('<img src="%s" />' % url)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
