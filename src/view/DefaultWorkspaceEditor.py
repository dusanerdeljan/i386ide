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

from PySide2.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QLabel
from PySide2.QtCore import Qt
from src.controller.WorkspaceConfiguration import WorkspaceConfiguration

class DefaultWorkspaceEditor(QDialog):
    
    def __init__(self, workspaceConfiguration):
        super(DefaultWorkspaceEditor, self).__init__()
        self.workspaceConfiguration: WorkspaceConfiguration = workspaceConfiguration
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle("Edit default workspace")
        self.setStyleSheet("background-color: #2D2D30; color: white;")
        self.setFixedSize(500, 150)
        self.label = QLabel("Default workspace")
        self.comboBox = QComboBox()
        self.comboBox.addItems(list(self.workspaceConfiguration.getWorkspaces()))
        defualt = self.workspaceConfiguration.getDefaultWorkspace()
        self.comboBox.addItem("No default workspace")
        if defualt:
            self.comboBox.setCurrentText(defualt)
        else:
            self.comboBox.setCurrentText("No default workspace")
        self.btnSave = QPushButton("Save workspace configuration")
        self.btnSave.clicked.connect(self.saveConfiguration)
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.hbox1.addWidget(self.label, 1)
        self.hbox1.addWidget(self.comboBox, 4)
        self.hbox2.addWidget(self.btnSave)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.setLayout(self.vbox)

    def saveConfiguration(self):
        default = self.comboBox.currentText()
        if default == "No default workspace":
            self.workspaceConfiguration.setDefaultWorkspace(None)
        else:
            self.workspaceConfiguration.setDefaultWorkspace(default)
        self.accept()

    def closeEvent(self, event):
        self.reject()

