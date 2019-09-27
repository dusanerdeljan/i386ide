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

from PySide2.QtWidgets import QDialog, QComboBox, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout


class NewFileDialog(QDialog):
    
    def __init__(self):
        super(NewFileDialog, self).__init__()
        self.comboBox = QComboBox()
        self.comboBox.addItem("Assembly file")
        self.comboBox.addItem("C file")
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("Enter file name...")
        self.setStyleSheet("background-color: #2D2D30; color: white;")
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.create = QPushButton("Create")
        self.cancel = QPushButton("Cancel")
        self.setWindowTitle("New file")
        self.result = None
        self.initGUI()

    def initGUI(self):
        self.vbox.addWidget(self.lineEdit)
        self.vbox.addWidget(self.comboBox)
        self.hbox.addWidget(self.create)
        self.hbox.addWidget(self.cancel)
        self.create.setDefault(True)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)
        self.setFixedSize(self.sizeHint())

        self.create.clicked.connect(self.createButtonClicked)
        self.cancel.clicked.connect(self.cancelButtonClicked)

    def createButtonClicked(self):
        extension = ".S" if self.comboBox.currentIndex() == 0 else ".c"
        self.result = "{}{}".format(self.lineEdit.text().strip(), extension)
        self.close()

    def cancelButtonClicked(self):
        self.result = None
        self.close()