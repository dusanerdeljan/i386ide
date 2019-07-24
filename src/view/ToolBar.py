from PySide2.QtWidgets import QToolBar, QPushButton, QAction
from PySide2.QtGui import QKeySequence


class ToolBar(QToolBar):

    def __init__(self):
        super(ToolBar, self).__init__()
        self.setStyleSheet("background-color: #676867; border-bottom: 2px solid grey; color: white; font-weight: 500")
        self.setMovable(False)
        self.compile = QAction("Compile", self)
        self.compile.setShortcut(QKeySequence("Ctrl+Shift+B"))
        self.debug = QAction("Debug", self)
        self.debug.setShortcut(QKeySequence("Ctrl+F5"))
        self.run = QAction("Run", self)
        self.run.setShortcut(QKeySequence("F5"))
        self.addAction(self.compile)
        self.addAction(self.debug)
        self.addAction(self.run)