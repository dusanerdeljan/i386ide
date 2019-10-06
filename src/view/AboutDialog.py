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

from PySide2.QtWidgets import QDialog, QHBoxLayout, QLabel, QTextEdit
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import Qt, QSize
import main

class AboutDialog(QDialog):
    
    def __init__(self):
        super(AboutDialog, self).__init__()
        self.setStyleSheet("background-color: #232323;")
        self.setWindowFlags(Qt.Window)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, False)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowIcon(QIcon(main.resource_path("resources/app_icon.ico")))
        self.setWindowTitle("About i386ide")
        self.label = QLabel()
        self.label.setPixmap(QPixmap(main.resource_path("resources/about.png")))
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.label)
        self.setLayout(self.hbox)
        self.setFixedSize(520, 420)