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

from PySide2.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox, QFileDialog, QMessageBox
from PySide2.QtCore import Qt
from src.controller.WorkspaceConfiguration import WorkspaceConfiguration
import re
import os


class WorkspaceConfigurationEditor(QDialog):

    def __init__(self, workpsaceConfiguration, mainApplicatoin, switch=False):
        super(WorkspaceConfigurationEditor, self).__init__()
        self.workspaceConfiguration: WorkspaceConfiguration = workpsaceConfiguration
        self.mainApplication = mainApplicatoin
        self.switch = switch
        self.workspaceDirectory = None
        self.setWindowTitle("Choose a workspace directory")
        self.setStyleSheet("background-color: #2D2D30; color: white;")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setFixedSize(500, 150)
        self.comboBox = QComboBox()
        self.updateComboBox()
        self.btnOpen = QPushButton("Open workspace")
        self.cbDefault = QCheckBox("Set as default workspace")
        self.btnBrowse = QPushButton("Browse...")
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.comboBox, 4)
        self.hbox2.addWidget(self.btnBrowse, 1)
        self.vbox.addLayout(self.hbox2)
        self.hbox.addWidget(self.cbDefault)
        self.hbox.addWidget(self.btnOpen)
        self.vbox.addSpacing(20)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)
        self.btnOpen.clicked.connect(self.loadWorkpace)
        self.btnBrowse.clicked.connect(self.browseWorkspace)
        self.btnOpen.setFocus()
        if len(self.workspaceConfiguration.getWorkspaces()) == 0:
            self.btnOpen.setEnabled(False)

    def updateComboBox(self):
        self.comboBox.clear()
        self.comboBox.addItems(list(self.workspaceConfiguration.getWorkspaces()))
        if self.workspaceConfiguration.defaultWorkspace:
            self.comboBox.setCurrentText(self.workspaceConfiguration.getDefaultWorkspace())

    def browseWorkspace(self):
        directory = QFileDialog.getExistingDirectory()
        if directory == "":
            return
        wsname = directory[directory.rindex(os.path.sep) + 1:]
        regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
        if ' ' in directory or regex.search(wsname):
            msg = QMessageBox()
            msg.setStyleSheet("background-color: #2D2D30; color: white;")
            msg.setModal(True)
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Workspace path/name cannot contain whitespace special characters.")
            msg.setWindowTitle("Workspace creation error")
            msg.exec_()
            return
        self.workspaceConfiguration.addWorkspace(directory)
        self.updateComboBox()
        if not self.btnOpen.isEnabled():
            self.btnOpen.setEnabled(True)

    def loadWorkpace(self):
        if self.cbDefault.isChecked():
            self.workspaceConfiguration.setDefaultWorkspace(self.comboBox.currentText())
        if not self.switch:
            success = self.mainApplication.openWorkspaceAction(self.comboBox.currentText())
            if not success:
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Failed to load '{}' because it is deleted from the disk.".format(self.comboBox.currentText()))
                msg.setWindowTitle("Failed to load workspace.")
                msg.exec_()
                self.workspaceConfiguration.removeWorkspace(self.comboBox.currentText())
                self.updateComboBox()
                return
        else:
            self.workspaceDirectory = self.comboBox.currentText()
        self.accept()

    def closeEvent(self, arg__1):
        self.reject()
