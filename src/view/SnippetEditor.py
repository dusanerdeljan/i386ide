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

from PySide2.QtWidgets import QDialog, QVBoxLayout, QPushButton, QListWidget, QMessageBox, QTextEdit, QHBoxLayout, QListWidgetItem, QInputDialog, QLineEdit
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QFontMetrics
from src.controller.SnippetManager import SnippetManager
from copy import deepcopy
import main

class SnippetListWidgetItem(QListWidgetItem):

    def __init__(self, text):
        super(SnippetListWidgetItem, self).__init__()
        self.setText(text)

    def __str__(self):
        return self.text()

class TextEditor(QTextEdit):
    
    def __init__(self):
        super(TextEditor, self).__init__()
        self.tabSize = 4
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Tab:
            self.insertPlainText(self.tabSize * " ")
            return
        super(TextEditor, self).keyPressEvent(e)


class SnippetEditor(QDialog):
    
    def __init__(self, snippetManager: SnippetManager):
        super(SnippetEditor, self).__init__()
        self.snippetManager = snippetManager
        self.snippetDict = deepcopy(self.snippetManager.codeSnippets)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle("Edit code snippets")
        self.setStyleSheet("background-color: #3E3E42; color: white;")
        self.setFixedSize(700, 400)
        self.setWindowIcon(QIcon(main.resource_path("resources/app_icon")))
        self.listView = QListWidget()
        self.nameEdit = QLineEdit()
        self.nameEdit.setStyleSheet(
            "font-size: 14px; background-color: #1E1E1E; color: white; font-family: comic-sans; border: none;")
        self.editor = TextEditor()
        self.editor.setStyleSheet(
            "font-size: 14px; background-color: #1E1E1E; color: white; font-family: comic-sans; border: none;")
        self.editor.setTabStopWidth(4 * QFontMetrics(self.font()).width(' '))
        self.listView.setStyleSheet("background-color: #2D2D30; color: white;")
        for snippet in self.snippetManager.getSnippetsAbbs():
            self.listView.addItem(SnippetListWidgetItem(snippet))
        self.hbox = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.vbox2 = QVBoxLayout()
        self.addButton = QPushButton("Add")
        self.addButton.setStyleSheet("background-color: #2D2D30; color: white;")
        self.removeButton = QPushButton("Remove")
        self.removeButton.setStyleSheet("background-color: #2D2D30; color: white;")
        self.applyButton = QPushButton("Apply")
        self.applyButton.setStyleSheet("background-color: #2D2D30; color: white;")
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setStyleSheet("background-color: #2D2D30; color: white;")
        self.okButton = QPushButton("OK")
        self.okButton.setStyleSheet("background-color: #2D2D30; color: white;")
        self.resetButton = QPushButton("Reset to default")
        self.resetButton.setStyleSheet("background-color: #2D2D30; color: white;")
        self.vbox.addWidget(self.listView)
        self.hbox2.addWidget(self.addButton)
        self.hbox2.addWidget(self.removeButton)
        self.hbox2.addWidget(self.applyButton)
        self.vbox.addLayout(self.hbox2)
        self.vbox2.addWidget(self.nameEdit)
        self.vbox2.addWidget(self.editor)
        self.hbox3.addWidget(self.cancelButton)
        self.hbox3.addWidget(self.resetButton)
        self.hbox3.addWidget(self.okButton)
        self.vbox2.addLayout(self.hbox3)
        self.hbox.addLayout(self.vbox)
        self.hbox.addLayout(self.vbox2)
        self.setLayout(self.hbox)

        self.listView.currentItemChanged.connect(self.updateEditor)
        self.okButton.clicked.connect(self.okButtonClicked)
        self.removeButton.clicked.connect(self.removeButtonClicked)
        self.addButton.clicked.connect(self.addButtonClicked)
        self.applyButton.clicked.connect(self.appyButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)
        self.resetButton.clicked.connect(self.resetButtonClicked)

    def resetingSnippetsWarning(self):
        msg = QMessageBox()
        msg.setStyleSheet("background-color: #2D2D30; color: white;")
        msg.setParent(None)
        msg.setModal(True)
        msg.setWindowTitle("Confirm reset to default")
        msg.setText("This will delete all snippets that were created by the user!")
        msg.setInformativeText("Do you want to continue?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        retValue = msg.exec_()
        if retValue == QMessageBox.Yes:
            return True

    def resetButtonClicked(self):
        if not self.resetingSnippetsWarning():
            return
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

    def checkSnippetName(self, name, checkSelected=False):
        if checkSelected:
            isSelected = name == str(self.listView.currentItem())
        else:
            isSelected = False
        if not isSelected and name in self.snippetDict:
            msg = QMessageBox()
            msg.setStyleSheet("background-color: #2D2D30; color: white;")
            msg.setModal(True)
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Snippet abbreviation already exists.")
            msg.setWindowTitle("Wrong snippet abbreviation")
            msg.exec_()
            return False
        if ' ' in name:
            msg = QMessageBox()
            msg.setStyleSheet("background-color: #2D2D30; color: white;")
            msg.setModal(True)
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Snippet abbreviation cannot contain whitespace characters.")
            msg.setWindowTitle("Wrong snippet abbreviation")
            msg.exec_()
            return False
        if name.strip() == '':
            msg = QMessageBox()
            msg.setStyleSheet("background-color: #2D2D30; color: white;")
            msg.setModal(True)
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Snippet abbreviation cannot be an empty string.")
            msg.setWindowTitle("Wrong snippet abbreviation")
            msg.exec_()
            return False
        return True

    def addButtonClicked(self):
        name, entered = QInputDialog.getText(None, "Add code snippet", "Enter snippet abbreviation ", QLineEdit.Normal, "")
        if entered:
            if not self.checkSnippetName(name):
                return
            self.snippetDict[name] = ""
            item = SnippetListWidgetItem(name)
            self.listView.addItem(item)
            self.listView.setCurrentItem(item)

    def updateList(self, selectedName=""):
        self.listView.clear()
        for snippet in self.snippetDict:
            self.listView.addItem(SnippetListWidgetItem(snippet))
        if selectedName:
            items = self.listView.findItems(selectedName, Qt.MatchExactly)
            if len(items) > 0:
                for item in items:
                    self.listView.setItemSelected(item, True)

    def appyButtonClicked(self):
        snippet = self.listView.currentItem()
        if snippet:
            name = self.nameEdit.text()
            if not self.checkSnippetName(name, checkSelected=True):
                return
            del self.snippetDict[str(snippet)]
            self.snippetDict[name] = self.editor.toPlainText()
            self.updateList(selectedName=name)
            self.snippetManager.updateSnippets(self.snippetDict)
        return True


    def okButtonClicked(self):
        self.snippetManager.updateSnippets(self.snippetDict)
        if self.appyButtonClicked():
            self.accept()

    def updateEditor(self, snippet, previous):
        if snippet and str(snippet) in self.snippetDict:
            self.nameEdit.setText(str(snippet))
            self.editor.setText(self.snippetDict[str(snippet)])

    def cancelButtonClicked(self):
        self.reject()

    def closeEvent(self, arg__1):
        self.reject()