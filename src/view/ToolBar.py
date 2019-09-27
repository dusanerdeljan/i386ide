"""
    This file is part of i386ide.
    i386ide is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from PySide2.QtWidgets import QToolBar, QPushButton, QAction, QComboBox, QLabel
from PySide2.QtGui import QKeySequence, QIcon, QPixmap
from PySide2.QtCore import Qt, QSize
from src.controller.ConfigurationManager import ConfigurationManager
from src.controller.PathManager import PathManager
import os
import main

class ProjectComboBox(QComboBox):

    def __init__(self, configurationManager):
        super(ProjectComboBox, self).__init__()
        self.configurationManager = configurationManager
        self.currentIndexChanged.connect(lambda x: self.configurationManager.setCurrentProject(self.currentData()))


class ToolBar(QToolBar):

    def __init__(self, configurationManager: ConfigurationManager):
        super(ToolBar, self).__init__()
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.configurationManager = configurationManager
        self.setStyleSheet("background-color: #2D2D30; color: white; font-weight: 500")
        self.setMovable(False)
        self.compile = QAction(QIcon(main.resource_path("resources/compile.png")), "Compile", self)
        self.compile.setShortcut(QKeySequence("Ctrl+Shift+B"))
        self.debug = QAction(QIcon(main.resource_path("resources/debug.png")), "Debug", self)
        self.debug.setShortcut(QKeySequence("Ctrl+F5"))
        self.run = QAction(QIcon(main.resource_path("resources/run.png")), "Run", self)
        self.label = QLabel("Select current project")
        self.label.setStyleSheet("padding-left: 5px;")
        icon = QIcon(main.resource_path("resources/current_folder.png"))
        self.currentIcon = QLabel()
        self.currentIcon.setPixmap(icon.pixmap(QSize(20, 20)))
        self.projectComboBox = ProjectComboBox(self.configurationManager)
        self.projectComboBox.setMinimumWidth(250)
        self.run.setShortcut(QKeySequence("F5"))
        self.addAction(self.compile)
        self.addAction(self.debug)
        self.addAction(self.run)
        self.addSeparator()
        self.addWidget(self.currentIcon)
        self.addWidget(self.label)
        self.addWidget(self.projectComboBox)

    def updateComboBox(self):
        self.projectComboBox.clear()
        currentProject = self.configurationManager.currentProject
        if self.configurationManager.allProjects:
            for project in self.configurationManager.allProjects:
                self.projectComboBox.addItem(project.proxy.path, project)
            if currentProject:
                self.projectComboBox.setCurrentText(currentProject.proxy.path)

    def getCurrentProject(self):
        return self.projectComboBox.currentText()