import sys
import os
import pickle
from PySide2.QtWidgets import QMainWindow, QLineEdit, QApplication, QFileDialog, QMessageBox, QDockWidget, QLabel, QInputDialog
from PySide2.QtCore import Qt, QDir
from src.view.CodeEditor import CodeEditor
from src.view.MenuBar import MenuBar
from src.view.Terminal import Terminal
from src.view.ToolBar import ToolBar
from src.view.StatusBar import StatusBar
from src.view.TreeView import TreeView
from src.view.HelpWidget import HelpWidget
from src.util.AsemblerSintaksa import AsemblerSintaksa
from src.util.CSyntax import CSyntax
from src.model.ProjectNode import ProjectNode
from src.model.AssemblyFileNode import AssemblyFileNode
from src.model.CFileNode import CFileNode
from src.model.WorkspaceNode import WorkspaceNode, WorkspaceProxy
from src.model.FileNode import FileProxy


class AsemblerIDE(QMainWindow):

    def __init__(self):
        super(AsemblerIDE, self).__init__()
        self.workspace = None
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
        self.treeDock.setTitleBarWidget(QLabel("Workspace explorer"))
        self.addDockWidget(Qt.LeftDockWidgetArea, self.treeDock)
        self.setMenuBar(self.menuBar)
        self.setMinimumSize(1200, 800)
        self.setWindowTitle("i386 Assembly Integrated Development Environment")
        self.setCentralWidget(self.editor)

        self.addMenuBarEventHandlers()
        self.addToolBarEventHandlers()
        self.addTreeViewEventHandlers()
        self.populateTreeView()
        self.statusBar.comboBox.currentTextChanged.connect(self.changeEditorSyntax)

    def changeEditorSyntax(self, text):
        if text == "Assembly":
            self.editor.sintaksa = AsemblerSintaksa(self.editor.document())
        elif text == "C":
            self.editor.sintaksa = CSyntax(self.editor.document())
        self.editor.update()

    def addTreeViewEventHandlers(self):
        self.treeView.fileDoubleCliked.connect(self.loadFileText)

    def populateTreeView(self):
        workspace = WorkspaceNode()
        workspace.setText(0, "My workspace")
        self.treeView.setRoot(workspace)
        for i in range(5):
            project = ProjectNode()
            project.setText(0, "My Project {}".format(i+1))
            assemblyFile = AssemblyFileNode()
            assemblyFile.setText(0, "procedure_{}.S".format(i+1))
            cFile = CFileNode()
            cFile.setText(0, "main_{}.c".format(i+1))
            self.treeView.addNode(workspace, project)
            self.treeView.addNode(project, assemblyFile)
            self.treeView.addNode(project, cFile)
            project.setExpanded(True)
        self.workspace = workspace

    def closeEvent(self, event):
        if self.editor.file:
            if self.editor.file.hasUnsavedChanges:
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
        self.menuBar.newWorkspaceAction.triggered.connect(self.newWorkspaceAction)
        self.menuBar.saveWorkspaceAction.triggered.connect(self.saveWorkspaceAction)
        self.menuBar.openWorkspaceAction.triggered.connect(self.openWorkspaceAction)

        self.menuBar.saveAction.triggered.connect(self.saveFileAction)
        self.menuBar.newAction.triggered.connect(self.newFileAction)
        self.menuBar.openAction.triggered.connect(self.openFileAction)

        self.menuBar.showTerminal.triggered.connect(lambda: self.terminal.show())
        self.menuBar.hideTerminal.triggered.connect(lambda: self.terminal.hide())
        self.menuBar.showTree.triggered.connect(lambda: self.treeDock.show())
        self.menuBar.hideTree.triggered.connect(lambda: self.treeDock.hide())

    def newWorkspaceAction(self):
        workspace = WorkspaceNode()
        #name, entered = QInputDialog.getText(self, "New workspace dialog", "Enter workspace name: ", QLineEdit.Normal, "New workspace")
        name = QFileDialog.getExistingDirectory(self, "New workspace", "select new workspace directory")
        if name:
            workspace.path = name
            # name ima formu home/user/.../.../{ime_workspace-a}
            workspace.setText(0, name[name.rindex(os.path.sep)+1:])
            self.workspace = workspace
            self.treeView.setRoot(self.workspace)

    def saveWorkspaceAction(self):
        if self.workspace:
            self.workspace.saveWorkspace()

    def openWorkspaceAction(self):
        name = QFileDialog.getExistingDirectory(self, "New workspace", "select new workspace directory")
        if not name:
            return
        path = os.path.join(name, ".metadata")
        if not os.path.exists(path):
            return
        with open(path, 'rb') as file:
            workspace = pickle.load(file)
        self.workspace = WorkspaceNode()
        self.workspace.proxy = workspace
        self.workspace.setText(0, name[name.rindex(os.path.sep)+1:])
        self.workspace.path = name
        self.workspace.proxy.path = name
        self.workspace.loadWorkspace()
        self.treeView.setRoot(self.workspace)
        self.treeView.expandAll()
        self.terminal.executeCommand("cd {}".format(self.workspace.path))

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

    def loadFileText(self, fileProxy):
        if fileProxy.text:
            self.editor.setPlainText(fileProxy.text)
            self.editor.file = fileProxy
        else:
            newText = self.openFileAction(fileProxy)
            fileProxy.text = newText
            fileProxy.hasUnsavedChanges = False

    def saveFileAction(self):
        if self.editor.file:
            with open(self.editor.file.getFilePath(), 'w') as file:
                file.write(self.editor.toPlainText())
                self.editor.file.hasUnsavedChanges = False
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

    def openFileAction(self, fileName: FileProxy=None):
        text = None
        if not fileName:
            fileName, _ = QFileDialog.getOpenFileName(self, "Choose a file to load", "", "*.S;;*.c")
        if fileName:
            with open(fileName.getFilePath(), 'r') as file:
                text = file.read()
                self.editor.setPlainText(text)
            self.editor.file = fileName
            # self.editor.file = FileProxy()
            # self.editor.file.path = fileName
            # self.editor.file.hasUnsavedChanges = False
        return text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ide = AsemblerIDE()
    ide.show()
    ide.editor.setFocus()
    app.exec_()
