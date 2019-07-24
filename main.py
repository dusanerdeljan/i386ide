import sys
import os
from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QDockWidget, QLabel
from PySide2.QtCore import Qt
from src.view.CodeEditor import CodeEditor
from src.view.MenuBar import MenuBar
from src.view.Terminal import Terminal
from src.view.ToolBar import ToolBar
from src.view.StatusBar import StatusBar
from src.view.TreeView import TreeView
from src.view.HelpWidget import HelpWidget
from src.util.AsemblerSintaksa import AsemblerSintaksa
from src.util.CSyntax import CSyntax


class AsemblerIDE(QMainWindow):

    def __init__(self):
        super(AsemblerIDE, self).__init__()
        self.editor = CodeEditor()
        self.menuBar = MenuBar()
        self.terminal = Terminal()
        self.toolBar = ToolBar()
        self.statusBar = StatusBar()
        self.treeView = TreeView()
        self.help = HelpWidget()
        self.setStatusBar(self.statusBar)
        self.addToolBar(self.toolBar)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.terminal)
        # self.addDockWidget(Qt.RightDockWidgetArea, self.help)
        self.treeDock = QDockWidget()
        self.treeDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.treeDock.setStyleSheet("background-color: #44423E; color: white;")
        self.treeDock.setFeatures(QDockWidget.DockWidgetMovable)
        self.treeDock.setWidget(self.treeView)
        self.treeDock.setTitleBarWidget(QLabel("TreeView Placeholder"))
        self.addDockWidget(Qt.LeftDockWidgetArea, self.treeDock)
        self.setMenuBar(self.menuBar)
        self.setMinimumSize(1200, 800)
        self.setWindowTitle("i386 Assembly Integrated Development Environment")
        self.setCentralWidget(self.editor)

        self.addMenuBarEventHandlers()
        self.addToolBarEventHandlers()
        self.statusBar.comboBox.currentTextChanged.connect(self.changeEditorSyntax)

    def changeEditorSyntax(self, text):
        if text == "Assembly":
            self.editor.sintaksa = AsemblerSintaksa(self.editor.document())
        elif text == "C":
            self.editor.sintaksa = CSyntax(self.editor.document())
        self.editor.update()

    def closeEvent(self, event):
        if self.editor.hasUnsavedChanges:
            msg = QMessageBox()
            self.setParent(None)
            msg.setModal(True)
            msg.setWindowTitle("Confirm Exit")
            msg.setText("The file has been modified.")
            msg.setInformativeText("Do you want to save changes?")
            msg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Save)
            retValue = msg.exec_()
            if retValue == QMessageBox.Save:
                if not self.saveFileAction():
                    event.ignore()
                    return
            elif retValue == QMessageBox.Discard:
                pass
            else:
                event.ignore()
                return
        super(AsemblerIDE, self).closeEvent(event)

    def addMenuBarEventHandlers(self):
        self.menuBar.saveAction.triggered.connect(self.saveFileAction)
        self.menuBar.newAction.triggered.connect(self.newFileAction)
        self.menuBar.openAction.triggered.connect(self.openFileAction)

        self.menuBar.showTerminal.triggered.connect(lambda: self.terminal.show())
        self.menuBar.hideTerminal.triggered.connect(lambda: self.terminal.hide())
        self.menuBar.showTree.triggered.connect(lambda: self.treeDock.show())
        self.menuBar.hideTree.triggered.connect(lambda: self.treeDock.hide())

    def addToolBarEventHandlers(self):
        self.toolBar.compile.triggered.connect(self.compileAction)
        self.toolBar.run.triggered.connect(self.runAction)
        self.toolBar.debug.triggered.connect(self.debugAction)

    def debugAction(self):
        if not self.editor.executablePath:
            if self.checkExecutable():
                self.editor.executablePath = self.editor.filePath[:-1] + "out"
            else:
                msg = QMessageBox()
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("You have to compile the file first.")
                msg.setWindowTitle("Debugger error.")
                msg.exec_()
                return
        self.terminal.console.setFocus()
        self.terminal.console.setFocus()
        self.terminal.executeCommand("ddd {}".format(self.editor.executablePath))

    def runAction(self):
        if not self.editor.executablePath:
            if self.checkExecutable():
                self.editor.executablePath = self.editor.filePath[:-1] + "out"
            else:
                msg = QMessageBox()
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("You have to compile the file first.")
                msg.setWindowTitle("Execution error.")
                msg.exec_()
                return
        self.terminal.console.setFocus()
        self.terminal.executeCommand("{}".format(self.editor.executablePath))

    def checkExecutable(self):
        if self.editor.filePath:
            destination = self.editor.filePath[:-1] + "out"
            return os.path.exists(destination)
        return None

    def compileAction(self):
        if not self.editor.filePath:
            msg = QMessageBox()
            msg.setModal(True)
            msg.setIcon(QMessageBox.Critical)
            msg.setText("You have to save the file first.")
            msg.setWindowTitle("Compilation error.")
            msg.exec_()
            return
        if self.editor.hasUnsavedChanges:
            self.saveFileAction()
        destination = self.editor.filePath[:-1] + "out"
        command = ['gcc', '-g', '-m32', '-o', destination, self.editor.filePath]
        commandStrng = ' '.join(command)
        # fileName = self.editor.getOpenFileName()
        self.terminal.console.setFocus()
        if self.terminal.executeCommand(commandStrng):
            self.editor.executablePath = destination

    def saveFileAction(self):
        if self.editor.filePath:
            with open(self.editor.filePath, 'w') as file:
                file.write(self.editor.toPlainText())
                self.editor.hasUnsavedChanges = False
                return True
        else:
            fileName, _ = QFileDialog.getSaveFileName(self, "Choose where you want to save the file.")
            if fileName:
                with open(fileName, 'w') as file:
                    file.write(self.editor.toPlainText())
                self.editor.filePath = fileName
                self.editor.hasUnsavedChanges = False
                return True
            return False

    def newFileAction(self):
        self.editor.clear()
        self.editor.filePath = None
        self.editor.hasUnsavedChanges = True

    def openFileAction(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose a file to load", "", "*.S;;*.c")
        if fileName:
            with open(fileName, 'r') as file:
                self.editor.setPlainText(file.read())
        self.editor.filePath = fileName
        self.editor.hasUnsavedChanges = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ide = AsemblerIDE()
    ide.show()
    ide.editor.setFocus()
    app.exec_()
