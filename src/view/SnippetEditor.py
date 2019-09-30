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

from PySide2.QtWidgets import QDialog, QVBoxLayout, QPushButton, QListWidget, QMessageBox, QTextEdit, QHBoxLayout, QListWidgetItem, QInputDialog, QLineEdit
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from src.controller.SnippetManager import SnippetManager
from copy import deepcopy
import main

class SnippetListWidgetItem(QListWidgetItem):

    def __init__(self, text):
        super(SnippetListWidgetItem, self).__init__()
        self.setText(text)

    def __str__(self):
        return self.text()


class SnippetEditor(QDialog):
    
    def __init__(self, snippetManager: SnippetManager):
        super(SnippetEditor, self).__init__()
        self.snippetManager = snippetManager
        self.snippetDict = deepcopy(self.snippetManager.codeSnippets)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle("Edit code snippets")
        self.setStyleSheet("background-color: #2D2D30; color: white;")
        self.setFixedSize(700, 400)
        self.setWindowIcon(QIcon(main.resource_path("resources/app_icon")))
        self.listView = QListWidget()
        self.editor = QTextEdit()
        self.editor.setTabStopWidth(16)
        for snippet in self.snippetManager.getSnippetsAbbs():
            self.listView.addItem(SnippetListWidgetItem(snippet))
        self.hbox = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.vbox2 = QVBoxLayout()
        self.addButton = QPushButton("Add")
        self.removeButton = QPushButton("Remove")
        self.saveItemButton = QPushButton("Save snippet")
        self.cancelButton = QPushButton("Cancel")
        self.saveButton = QPushButton("Save configuration")
        self.resetButton = QPushButton("Reset to default")
        self.vbox.addWidget(self.listView)
        self.hbox2.addWidget(self.addButton)
        self.hbox2.addWidget(self.removeButton)
        self.hbox2.addWidget(self.saveItemButton)
        self.vbox.addLayout(self.hbox2)
        self.vbox2.addWidget(self.editor)
        self.hbox3.addWidget(self.cancelButton)
        self.hbox3.addWidget(self.resetButton)
        self.hbox3.addWidget(self.saveButton)
        self.vbox2.addLayout(self.hbox3)
        self.hbox.addLayout(self.vbox)
        self.hbox.addLayout(self.vbox2)
        self.setLayout(self.hbox)

        self.listView.currentItemChanged.connect(self.updateEditor)
        self.saveButton.clicked.connect(self.saveButtonClicked)
        self.removeButton.clicked.connect(self.removeButtonClicked)
        self.addButton.clicked.connect(self.addButtonClicked)
        self.saveItemButton.clicked.connect(self.saveItemButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)
        self.resetButton.clicked.connect(self.resetButtonClicked)

    def saveItemButtonClicked(self):
        snippet = self.listView.currentItem()
        if snippet:
            self.snippetDict[str(snippet)] = self.editor.toPlainText()

    def resetButtonClicked(self):
        self.snippetDict.clear()
        for key in SnippetManager.DEFAULT_SNIPPETS:
            self.snippetDict[key] = SnippetManager.DEFAULT_SNIPPETS[key]
        self.updateList()

    def removeButtonClicked(self):
        snippet = self.listView.currentItem()
        if snippet:
            answer = QMessageBox.question(None, "Delete snippet",
                                          "Are you sure you want to delete snippet '{}'?".format(
                                              str(snippet)),
                                          QMessageBox.Yes | QMessageBox.No)
            if not answer == QMessageBox.Yes:
                return
            del self.snippetDict[str(snippet)]
            self.updateList()

    def addButtonClicked(self):
        name, entered = QInputDialog.getText(None, "Add code snippet", "Enter snippet abbreviation ", QLineEdit.Normal, "")
        if entered and name:
            if name in self.snippetDict:
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Snippet abbreviation already exists.")
                msg.setWindowTitle("Wrong snippet abbreviation")
                msg.exec_()
                return
            self.snippetDict[name] = ""
            item = SnippetListWidgetItem(name)
            self.listView.addItem(item)
            self.listView.setCurrentItem(item)

    def updateList(self):
        self.listView.clear()
        for snippet in self.snippetDict:
            self.listView.addItem(SnippetListWidgetItem(snippet))

    def saveButtonClicked(self):
        self.snippetManager.updateSnippets(self.snippetDict)
        self.accept()

    def updateEditor(self, snippet, previous):
        if snippet:
            self.editor.setText(self.snippetDict[str(snippet)])

    def cancelButtonClicked(self):
        self.reject()

    def closeEvent(self, arg__1):
        self.reject()