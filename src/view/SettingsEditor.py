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

from PySide2.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from src.controller.TooltipManager import TooltipManager
import main

class SettingsEditor(QDialog):
    
    def __init__(self, tooltipManager: TooltipManager):
        super(SettingsEditor, self).__init__()
        self.tooltipManager = tooltipManager
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle("Edit IDE settings")
        self.setStyleSheet("background-color: #2D2D30; color: white;")
        self.setFixedSize(500, 150)
        self.setWindowIcon(QIcon(main.resource_path("resources/app_icon")))
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.saveButton = QPushButton("Save settings")
        self.cancelButton = QPushButton("Cancel")
        self.resetButton = QPushButton("Reset to defaults")
        self.tooltipLabel = QLabel("<center>Tooltip configuration</centr>")
        self.instructionsTooltopCheckBox = QCheckBox("Show instructions tooltips")
        self.instructionsTooltopCheckBox.setChecked(self.tooltipManager.showInstructionTooltips)
        self.numbersTooltipCheckBox = QCheckBox("Show converted numbers")
        self.numbersTooltipCheckBox.setChecked(self.tooltipManager.showNumberConversion)
        self.vbox.addWidget(self.tooltipLabel)
        self.vbox.addWidget(self.instructionsTooltopCheckBox)
        self.vbox.addWidget(self.numbersTooltipCheckBox)
        self.hbox.addWidget(self.cancelButton)
        self.hbox.addWidget(self.resetButton)
        self.hbox.addWidget(self.saveButton)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

        self.saveButton.clicked.connect(self.saveButtonClicked)
        self.resetButton.clicked.connect(self.resetButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)

    def saveButtonClicked(self):
        self.tooltipManager.showInstructionTooltips = self.instructionsTooltopCheckBox.isChecked()
        self.tooltipManager.showNumberConversion = self.numbersTooltipCheckBox.isChecked()
        self.accept()

    def resetButtonClicked(self):
        self.instructionsTooltopCheckBox.setChecked(TooltipManager.DEFAULT_VALUE_INSTUCTIONS)
        self.numbersTooltipCheckBox.setChecked(TooltipManager.DEFAULT_VALUE_NUMBERS)

    def cancelButtonClicked(self):
        self.reject()

    def closeEvent(self, arg__1):
        self.reject()