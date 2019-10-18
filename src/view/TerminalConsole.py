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

from PySide2.QtWidgets import QTextEdit, QMessageBox
from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QTextCursor
from src.controller.TerminalController import TerminalController
from src.datastrctures.CommandHistoryStack import CommandHistoryStack
import os
import socket
import getpass


class TerminalConsole(QTextEdit):

    projectSwitchRequested = Signal()
    tabSwitchRequested = Signal()

    def __init__(self):
        super(TerminalConsole, self).__init__()
        self.queryWord = ""
        self.promptText = ""
        self.command = ""
        self.controller = TerminalController()
        self.controller.externalCommand.connect(self.externalShellCommandRun)
        self.username = "{}@{}".format(getpass.getuser(), socket.gethostname())
        try:
            self.cwd = '~' + os.getcwd().split(getpass.getuser())[1]
        except:
            self.cwd = '~' + os.getcwd()
        self.history = CommandHistoryStack()
        self.prepareConsole()

    def mousePressEvent(self, e):
        self.setFocus()

    def keyPressEvent(self, event):
        enterPressed = False
        if event.key() == Qt.Key_E and event.modifiers() == Qt.ControlModifier:
            self.projectSwitchRequested.emit()
            return
        if event.key() == Qt.Key_Left:
            if self.textCursor().positionInBlock() <= self.getPromptCursorPosition():
                return
        if event.key() == Qt.Key_Up:
            self.getNextPreviousCommandFromHistory(prev=True)
            return
        if event.key() == Qt.Key_Down:
            self.getNextPreviousCommandFromHistory(prev=False)
            return
        if event.key() == Qt.Key_Tab:
            if event.modifiers() == Qt.ControlModifier:
                self.tabSwitchRequested.emit()
            command = self.textCursor().block().text().replace(self.promptText, "")
            new_command = self.controller.showCommandAutocomplete(command)
            if len(new_command) == 1:
                self.outputAutocompleteResult(new_command[0])
            else:
                self.outputAutocompleteSuggestions(new_command[0], new_command[1])
            return

        if event.key() == Qt.Key_Return:
            self.command = self.textCursor().block().text().split("$")[1].strip()
            self.moveCursor(QTextCursor.End)
            enterPressed = True
            if self.command.strip() == "clear":
                self.clearCommand()
                return
        if event.key() == Qt.Key_Backspace:
            if event.modifiers() == Qt.ControlModifier:
                return
            if self.textCursor().positionInBlock() <= self.getPromptCursorPosition():
                return
            if len(self.command) == 0:
                return
            self.command = self.command[:-1]
        else:
            self.command += event.text()
        super(TerminalConsole, self).keyPressEvent(event)
        if enterPressed:
            self.outputCommandResult()

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if not mimeData.hasUrls():
            return
        self.textCursor().insertText(" ".join([mimeData.urls()[i].toLocalFile() for i in range(len(mimeData.urls()))]))
        event.acceptProposedAction()

    def clearCommand(self):
        self.clear()
        self.insertHtml(self.getPrompt())
        self.history.push("clear")
        self.command = ""

    def executeCommand(self, command):
        self.setFocus()
        while not self.textCursor().positionInBlock() == self.getPromptCursorPosition():
            self.textCursor().deletePreviousChar()
        self.moveCursor(QTextCursor.End)
        self.insertHtml('<span>{}</span>'.format(command))
        self.insertPlainText("\n")
        self.command = command
        return self.outputCommandResult()

    def outputAutocompleteSuggestions(self, new_command, suggestions):
        while not self.textCursor().positionInBlock() == self.getPromptCursorPosition():
            self.textCursor().deletePreviousChar()
        self.moveCursor(QTextCursor.End)
        output = new_command + suggestions
        self.insertHtml('<span>{}</span>'.format(output))
        self.insertPlainText("\n")
        self.insertHtml(self.getPrompt())
        self.insertHtml('<span>{}</span>'.format(new_command))
        self.moveCursor(QTextCursor.End)
        self.command = new_command

    def outputAutocompleteResult(self, new_command):
        while not self.textCursor().positionInBlock() == self.getPromptCursorPosition():
            self.textCursor().deletePreviousChar()
        self.moveCursor(QTextCursor.End)
        self.insertHtml('<span>{}</span>'.format(new_command))
        self.command = new_command


    def getNextPreviousCommandFromHistory(self, prev=True):
        while not self.textCursor().positionInBlock() == self.getPromptCursorPosition():
            self.textCursor().deletePreviousChar()
        self.moveCursor(QTextCursor.End)
        cmd = self.history.getPrev() if prev else self.history.getNext()
        self.insertHtml('<span>{}</span>'.format(cmd))
        self.command = cmd

    def outputCommandResult(self):
        if self.command.strip() == "":
            self.insertHtml(self.getPrompt())
            return False
        self.history.push(self.command)
        success = False
        commandResult = self.controller.commandEnteredHandler(self.command)
        if commandResult == "UC":
            self.insertHtml(self.getUnsupportedCommandText())
            self.insertPlainText("\n")
        elif commandResult == "ES":
            self.insertHtml(self.getExternalShellText("Proccess is running in an external shell."))
            self.insertPlainText("\n")
            success = True
        elif commandResult == "UES":
            self.insertHtml(self.getExternalShellText("Unable to start the process in an external shell."))
            self.insertPlainText("\n")
        elif commandResult == "TE":
            self.insertHtml(self.getExternalShellText("Connection timeout."))
            self.insertPlainText("\n")
        elif not commandResult['error']:
            self.insertPlainText(commandResult['output'])
            success = True
        else:
            self.insertPlainText(commandResult['error'])
            if commandResult['error'].lower() == "too many errors from stdin":
                self.insertPlainText("\n")
        self.insertHtml(self.getPrompt())
        self.command = ""
        self.moveCursor(QTextCursor.End)
        self.promptText = self.textCursor().block().text()
        return success

    def externalShellCommandRun(self, command):
        msg = QMessageBox()
        msg.setStyleSheet("background-color: #2D2D30; color: white;")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Proccess started in external shell.")
        msg.setWindowTitle(command)
        msg.exec_()

    def getColoredUsername(self):
        return '<span style="color: #3A6434; font-size: 14px; font-weight: 700;">{}</span>$ '.format(self.username)

    def getPrompt(self):
        cwd = os.getcwd()
        if getpass.getuser() in cwd:
            self.cwd = '~' + cwd.split(getpass.getuser())[1]
        else:
            self.cwd = '~' + cwd
        return '<span style="color: #3A6434; font-size: 14px; font-weight: 700;">{}</span>:  ' \
               '<span style="color: #007ACC; font-size: 14px; font-weight: 700;">{}</span>$ '.format(self.username, self.cwd)

    def getPromptCursorPosition(self):
        return len("{}:{}$ ".format(self.username, self.cwd))+1

    def getExternalShellText(self, txt):
        return '<span style="color: yellow; font-size: 14px;">{}</span>'.format(txt)

    def getUnsupportedCommandText(self):
        return '<span style="color: red; font-size: 14px;">Unsupported command!</span>'

    def prepareConsole(self):
        self.setStyleSheet("""
                background-color: #333337;
                color: white;
                font-size: 14px;
                """)
        self.insertHtml(self.getPrompt())
        self.command = ""