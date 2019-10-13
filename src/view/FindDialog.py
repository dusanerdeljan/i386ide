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

from PySide2.QtWidgets import QDialog, QLineEdit, QPlainTextEdit, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QFrame
from PySide2.QtGui import QIcon, QTextCursor
from PySide2.QtCore import Qt, Signal
import re
import main

class FindLineEdit(QLineEdit):

    enterPressed = Signal()
    
    def __init__(self):
        super(FindLineEdit, self).__init__()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.enterPressed.emit()
        super(FindLineEdit, self).keyPressEvent(e)


class FindDialog(QFrame):

    escapePressed = Signal()

    def __init__(self, editor: QPlainTextEdit):
        super(FindDialog, self).__init__()
        self.setLineWidth(0)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("background-color: #232323; color: white; padding: 0px; margin: 0px;")
        self.setWindowFlags(Qt.Dialog)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowIcon(QIcon(main.resource_path("resources/app_icon.ico")))
        self.setWindowTitle("Find & Replace")
        self.editor = editor
        self.text = self.editor.toPlainText()
        self.lastMatch = None
        self.findLabel = FindLineEdit()
        self.findLabel.setFixedWidth(200)
        self.findLabel.enterPressed.connect(self.findLabelEnterPressed)
        self.findLabel.setPlaceholderText("Find...")
        self.findLabel.textChanged.connect(lambda: self.find(continueSearch=False))
        self.replaceLabel = FindLineEdit()
        self.replaceLabel.setPlaceholderText("Replace...")
        self.replaceLabel.setFixedWidth(200)
        self.replaceLabel.enterPressed.connect(self.replaceLabelEnterPressed)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.findLabel)
        self.hbox.addWidget(self.replaceLabel)
        self.replaceAllButton = QPushButton("Repalce all")
        self.replaceAllButton.setStyleSheet("background-color: #232323; color: white;")
        self.replaceAllButton.clicked.connect(self.replaceAllButtonClicked)
        self.hbox.addWidget(self.replaceAllButton)
        self.setLayout(self.hbox)
        self.findLabel.setFocus()
        self.setFixedHeight(40)
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.hideWidget()
        super(FindDialog, self).keyPressEvent(e)

    def hideWidget(self):
        self.escapePressed.emit()

    def findLabelEnterPressed(self):
        success = self.find(continueSearch=True)
        if not success:
            self.find(continueSearch=False)

    def moveCursor(self, start, end):
        cursor = self.editor.textCursor()
        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end-start)
        self.editor.setTextCursor(cursor)

    def replaceAllButtonClicked(self):
        previousCursor = self.editor.textCursor()
        while self.find():
            self.replace()
            previousCursor = self.editor.textCursor()
        self.editor.setTextCursor(previousCursor)

    def replaceLabelEnterPressed(self):
        self.replace()

    def replace(self):
        if self.lastMatch and self.editor.textCursor().hasSelection():
            self.editor.textCursor().insertText(self.replaceLabel.text())
            self.editor.setUnsavedChanges()

    def find(self, continueSearch=None):
        searchTerm = re.escape(self.findLabel.text())
        if searchTerm == "":
            return False
        self.text = self.editor.toPlainText()
        regex = re.compile(searchTerm, re.I)
        start = self.lastMatch.start() + 1 if (self.lastMatch and continueSearch) else 0
        self.lastMatch = regex.search(self.text, start)
        if self.lastMatch:
            self.editor.lastFind = searchTerm
            self.moveCursor(self.lastMatch.start(), self.lastMatch.end())
            return True
        else:
            self.editor.moveCursor(QTextCursor.End)
            return False
