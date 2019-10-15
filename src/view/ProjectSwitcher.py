"""
    i386ide is lightweight IDE for i386 assembly and C programming language.
    Copyright (C) 2019  Dušan Erdeljan, Marko Njegomir

    This file is part of i386ide.

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

from PySide2.QtWidgets import QListWidget, QListWidgetItem, QDialog, QVBoxLayout, QLabel
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from src.controller.ConfigurationManager import ConfigurationManager
import main

class ProjectSwitcherListItem(QListWidgetItem):

    def __init__(self, projectProxy):
        super(ProjectSwitcherListItem, self).__init__()
        self.setIcon(QIcon(main.resource_path("resources/project.png")))
        self.setText(projectProxy.path)
        self.projectProxy = projectProxy

class ProjectSwitcher(QDialog):
    
    def __init__(self, configurationManager: ConfigurationManager, projectComboBox):
        super(ProjectSwitcher, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.configurationManager = configurationManager
        self.projectComboBox = projectComboBox
        self.latestProjectIndex = -1
        self.setStyleSheet("background-color: #232323; color: white;")
        self.projectList = QListWidget()
        self.vbox = QVBoxLayout()
        self.pathLabel = QLabel()
        self.pathLabel.setStyleSheet("font-size: 10px; color: grey;")
        self.vbox.addWidget(QLabel("<center>Project switcher</center>"), 1)
        self.vbox.addWidget(self.projectList, 10)
        self.vbox.addWidget(self.pathLabel, 1)
        self.setLayout(self.vbox)

    def showSwitcher(self):
        self.latestProjectIndex = self.getCurrentProjectIndex()
        self.updateProjectList()
        self.updateProjectListCurrentItem(self.latestProjectIndex)
        self.setFixedSize(self.sizeHint())
        self.setFixedWidth(500)
        self.show()

    def getCurrentProjectIndex(self):
        for i in range(len(self.configurationManager.allProjects)):
            if self.configurationManager.allProjects[i].proxy.getProjectPath() == self.configurationManager.currentProject.proxy.getProjectPath():
                return i
        return -1   # should never execute

    def updateProjectList(self):
        self.projectList.clear()
        for project in self.configurationManager.allProjects:
            self.projectList.addItem(ProjectSwitcherListItem(project.proxy))

    def updateProjectListCurrentItem(self, index):
        self.projectList.setCurrentRow(index)
        projectProxy = self.projectList.currentItem().projectProxy
        self.pathLabel.setText(projectProxy.getProjectPath())

    def hideSwitcher(self):
        if self.latestProjectIndex >= -1:
            self.projectComboBox.setCurrentText(self.projectList.currentItem().projectProxy.path)
        self.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab or event.key() == Qt.Key_Down or event.key() == Qt.Key_E:
            self.latestProjectIndex = (self.latestProjectIndex + 1) % len(self.configurationManager.allProjects)
        elif event.key() == Qt.Key_Up or event.key() == Qt.Key_Backtab:
            self.latestProjectIndex -= 1
            if self.latestProjectIndex < 0:
                self.latestProjectIndex = len(self.configurationManager.allProjects) - 1
        self.updateProjectListCurrentItem(self.latestProjectIndex)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Backtab:
            return
        if event.modifiers() != Qt.ControlModifier:
            if self.latestProjectIndex != -1:
                self.projectComboBox.setCurrentText(self.projectList.currentItem().projectProxy.path)
            self.latestProjectIndex = -1
            self.hideSwitcher()

    def focusOutEvent(self, event):
        super(ProjectSwitcher, self).focusOutEvent(event)
        self.hide()
