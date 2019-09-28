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

from PySide2.QtWidgets import QStatusBar, QLabel, QComboBox, QWidget


class StatusBar(QStatusBar):
    
    def __init__(self):
        super(StatusBar, self).__init__()
        self.setStyleSheet("""
                        background-color: #007ACC;
                        color: white;
                        font-size: 14px;
                        """)
        self.label = QLabel("Current syntax:")
        self.label2 = QLabel("Set tab width:")
        self.comboBox = QComboBox()
        self.comboBox.addItem("Assembly")
        self.comboBox.addItem("C")
        self.comboBox.setEnabled(False)
        self.tabWidthComboBox = QComboBox()
        self.tabWidthComboBox.addItem("2")
        self.tabWidthComboBox.addItem("4")
        self.tabWidthComboBox.addItem("8")
        self.tabWidthComboBox.setCurrentText('4')
        self.addWidget(QWidget(), 6)
        self.addWidget(self.label, 1)
        self.addWidget(self.comboBox, 1)
        self.addWidget(self.label2, 1)
        self.addWidget(self.tabWidthComboBox, 1)
        self.setMaximumHeight(25)