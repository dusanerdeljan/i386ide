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

from PySide2.QtWidgets import QDockWidget, QLineEdit, QTextEdit, QCompleter
from PySide2.QtCore import Qt
from src.util.InstructionsInfo import InstructionsInfo


class HelpWidget(QDockWidget):

    def __init__(self):
        super(HelpWidget, self).__init__()
        # TODO: ovo treba da bude kao neki widget u koji moze da se unese instrukcija ili registar ili direktiva
        # TODO: pa mu se onda ispise neki uredjeni HTML kao onaj tekst iz praktikuma sta ta kljucna rec znaci
        # TODO: mozda da se ispisu i neki odabrani algoritmi npr. sabiranje u dvostrukoj preciznosti sa ilustracijama
        # TODO: ili iteriranje kroz niz
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setMinimumWidth(200)
        self.setStyleSheet("background-color: #2D2D30; color: white;")
        self.searchLabel = QLineEdit()
        self.searchLabel.setPlaceholderText("Search for an instruction...")
        self.completer = QCompleter(list(InstructionsInfo.INFO.keys()), self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.popup().setStyleSheet("background-color: #2D2D30; color: white")
        self.searchLabel.setCompleter(self.completer)
        self.searchLabel.setStyleSheet("margin-bottom: 10px; margin-top: 10px;")
        self.setTitleBarWidget(self.searchLabel)
        self.setFeatures(QDockWidget.DockWidgetMovable)
        self.resultBox = QTextEdit()
        self.resultBox.setReadOnly(True)
        self.setWidget(self.resultBox)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and self.searchLabel.hasFocus():
            seachWord = self.searchLabel.text().strip()
            if seachWord in InstructionsInfo.INFO:
                self.resultBox.setHtml(InstructionsInfo.INFO[seachWord])
        super(HelpWidget, self).keyPressEvent(event)
