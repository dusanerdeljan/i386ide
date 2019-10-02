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

from PySide2.QtWidgets import QDialog, QLabel, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from src.model.AssemblyFileNode import AssemblyFileProxy
from src.model.CFileNode import CFileProxy
import os
import main

class CompilerOptionsEditor(QDialog):

    DEFAULT_OPTIONS = ['-g', '-m32']
    
    def __init__(self, projectProxy):
        super(CompilerOptionsEditor, self).__init__()
        self.project = projectProxy
        self.initialState = projectProxy.gccOptions
        self.setStyleSheet("background-color: #2D2D30; color: white;")
        self.setWindowTitle("Edit compiler options")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowIcon(QIcon(main.resource_path("resources/app_icon.ico")))
        self.setFixedSize(500, 200)
        self.vbox = QVBoxLayout()
        self.optionsLineEdit = QLineEdit()
        self.optionsLineEdit.setToolTip("Enter semicolon (;) separated gcc options")
        self.optionsLineEdit.setText(";".join(projectProxy.gccOptions))
        self.vbox.addWidget(self.optionsLineEdit)
        self.previewTextEdit = QTextEdit()
        self.previewTextEdit.setReadOnly(True)
        self.previewTextEdit.setHtml(self.buildCompileCommand(self.project.gccOptions))
        self.previewLabel = QLabel("Preview of the compile command")
        self.vbox.addWidget(self.previewLabel)
        self.vbox.addWidget(self.previewTextEdit, 3)
        self.hbox = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.resetButton = QPushButton("Reset to default")
        self.cancelButton = QPushButton("Cancel")
        self.saveButton.setDefault(True)
        self.hbox.addWidget(self.cancelButton)
        self.hbox.addWidget(self.resetButton)
        self.hbox.addWidget(self.saveButton)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

        self.optionsLineEdit.textChanged.connect(self.optionsChanged)

        self.saveButton.clicked.connect(self.saveButtonClicked)
        self.resetButton.clicked.connect(self.resetButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)

    def optionsChanged(self):
        options = self.optionsLineEdit.text().split(";")
        command = self.buildCompileCommand(options)
        self.previewTextEdit.setHtml(command)

    def buildCompileCommand(self, options):
        destination = os.path.join(self.project.getProjectPath(), "{}.out".format(self.project.path))
        cFiles = []
        sFiles = []
        for file in self.project.files:
            if isinstance(file, CFileProxy):
                cFiles.append(file.getFilePath())
            elif isinstance(file, AssemblyFileProxy):
                sFiles.append(file.getFilePath())
        command = ['gcc']
        command.append("<span style=\"color: #007ACC; font-weight: 800;\">{}</span>".format(' '.join(options)))
        command.extend(['-o', destination])
        if cFiles:
            command.extend(cFiles)
        if sFiles:
            command.extend(sFiles)
        return ' '.join(command)

    def closeEvent(self, arg__1):
        self.project.gccOptions = self.initialState
        self.reject()

    def cancelButtonClicked(self):
        self.project.gccOptions = self.initialState
        self.reject()

    def saveButtonClicked(self):
        self.project.gccOptions = [option.strip() for option in self.optionsLineEdit.text().split(";")]
        self.accept()

    def resetButtonClicked(self):
        self.optionsLineEdit.setText(";".join(CompilerOptionsEditor.DEFAULT_OPTIONS))