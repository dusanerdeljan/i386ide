from PySide2.QtWidgets import QTextEdit, QMessageBox
from PySide2.QtCore import Qt
from PySide2.QtGui import QTextCursor
from src.controller.TerminalController import TerminalController
from src.datastrctures.CommandHistoryStack import CommandHistoryStack
import os
import socket


class TerminalConsole(QTextEdit):

    def __init__(self):
        super(TerminalConsole, self).__init__()
        self.command = ""
        self.controller = TerminalController()
        self.controller.externalCommand.connect(self.externalShellCommandRun)
        self.username = "{}@{}".format(os.getlogin(), socket.gethostname())
        try:
            self.cwd = '~' + os.getcwd().split(os.getlogin())[1]
        except:
            self.cwd = '~' + os.getcwd()
        self.history = CommandHistoryStack()
        self.prepareConsole()

    def mousePressEvent(self, e):
        self.setFocus()

    def keyPressEvent(self, event):
        enterPressed = False
        if event.key() == Qt.Key_Left:
            if self.textCursor().positionInBlock() <= self.getPromptCursorPosition():
                return
        if event.key() == Qt.Key_Up:
            self.getNextPreviousCommandFromHistory(prev=True)
            return
        if event.key() == Qt.Key_Down:
            self.getNextPreviousCommandFromHistory(prev=False)
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
        if os.getlogin() in cwd:
            self.cwd = '~' + cwd.split(os.getlogin())[1]
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