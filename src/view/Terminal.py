from PySide2.QtWidgets import QDockWidget, QLabel
from PySide2.QtCore import Qt
from src.view.TerminalConsole import TerminalConsole


class Terminal(QDockWidget):

    def __init__(self):
        super(Terminal, self).__init__()
        self.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetMovable)
        self.titleLabel = QLabel()
        self.titleLabel.setStyleSheet("background-color: #44423E; border-top: 2px solid black; color: white")
        self.titleLabel.setText("Terminal")
        self.setTitleBarWidget(self.titleLabel)
        self.console = TerminalConsole()
        self.setWidget(self.console)

    def executeCommand(self, command):
        return self.console.executeCommand(command)

    def getUsername(self):
        return self.console.username
