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

from PySide2.QtWidgets import QListWidget, QListWidgetItem, QDialog, QVBoxLayout, QLabel
from PySide2.QtCore import Qt


class AutoCompleteListWidgetItem(QListWidgetItem):

    def __init__(self, text):
        super(AutoCompleteListWidgetItem, self).__init__()
        self.setText(text)

    def __str__(self):
        return self.text()


class AutocompleteWidget(QDialog):

    WIDTH = 300
    HEIGHT = 120

    def __init__(self, suggestions: list):
        super(AutocompleteWidget, self).__init__()
        self.widget = QListWidget()
        self.widget.setStyleSheet("background-color: #232323;")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.vbox = QVBoxLayout()
        self.label = QLabel("")
        self.vbox.addWidget(self.widget, 10)
        self.vbox.addWidget(self.label, 1)
        self.setLayout(self.vbox)
        self.updateSuggestionList(suggestions)
        self.result = None

    def updateSuggestionList(self, suggestions):
        self.widget.clear()
        if suggestions:
            for keyword in suggestions:
                self.widget.addItem(AutoCompleteListWidgetItem(keyword))
            self.label.setText("Number of suggestions: {}.".format(len(suggestions)))
        else:
            self.label.setText("No available suggestions.")
        self.setSize()

    def setSize(self):
        self.setFixedSize(self.minimumSizeHint())
        self.setFixedHeight(AutocompleteWidget.HEIGHT)
        self.setFixedWidth(AutocompleteWidget.WIDTH)


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == Qt.Key_Return:
            selectedItems = self.widget.selectedItems()
            if len(selectedItems) > 0:
                self.result = selectedItems[0]
            self.close()
        if e.key() == Qt.Key_Backspace:
            self.close()
        if e.key() == Qt.Key_Left:
            self.parent().setFocus()