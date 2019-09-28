"""
    i386ide is lightweight IDE for i386 assembly and C programming language.
    Copyright (C) 2019  Dušan Erdeljan, Marko Njegomir

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

from PySide2.QtWidgets import QDockWidget, QLabel
from PySide2.QtCore import Qt
from src.view.TerminalConsole import TerminalConsole


class Terminal(QDockWidget):

    def __init__(self):
        super(Terminal, self).__init__()
        self.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetMovable)
        self.titleLabel = QLabel()
        self.titleLabel.setStyleSheet("background-color: #3E3E42; color: white")
        self.titleLabel.setText("Terminal")
        self.setTitleBarWidget(self.titleLabel)
        self.console = TerminalConsole()
        self.setWidget(self.console)

    def executeCommand(self, command):
        return self.console.executeCommand(command)

    def getUsername(self):
        return self.console.username
