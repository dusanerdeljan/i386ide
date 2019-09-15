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
from src.view.TabWidget import EditorTabWidget
from src.util.AsemblerSintaksa import AsemblerSintaksa
from src.util.CSyntax import CSyntax
from src.model.ProjectNode import ProjectNode
from src.model.AssemblyFileNode import AssemblyFileNode
from src.model.CFileNode import CFileNode
from src.model.WorkspaceNode import WorkspaceNode, WorkspaceProxy
from src.model.FileNode import FileProxy
from src.controller.ConfigurationManager import ConfigurationManager


class AsemblerIDE(QMainWindow):

    def __init__(self):
        super(AsemblerIDE, self).__init__()
        self.workspace = None
        self.configurationManager = ConfigurationManager()
        self.editorTabs = EditorTabWidget()
        self.menuBar = MenuBar()
        self.terminal = Terminal()
        self.toolBar = ToolBar(self.configurationManager)
        self.statusBar = StatusBar()
        self.treeView = TreeView(self.configurationManager)
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
        self.setCentralWidget(self.editorTabs)
        self.setStyleSheet("background-color:  #566573 ; color: white;")

        self.addTabWidgetEventHandlers()
        self.addMenuBarEventHandlers()
        self.addToolBarEventHandlers()
        self.addTreeViewEventHandlers()
        self.populateTreeView()
        self.statusBar.comboBox.currentTextChanged.connect(self.changeEditorSyntax)

    def changeEditorSyntax(self, text):
        currentTab = self.editorTabs.getCurrentTab()
        if currentTab:
            if text == "Assembly":
                currentTab.editor.sintaksa = AsemblerSintaksa(currentTab.editor.document())
            elif text == "C":
                currentTab.editor.sintaksa = CSyntax(currentTab.editor.document())
            currentTab.editor.update()

    def addTabWidgetEventHandlers(self):
        self.editorTabs.currentChanged.connect(self.activeTabChanged)

    def addTreeViewEventHandlers(self):
        self.treeView.fileDoubleCliked.connect(self.loadFileText)
        self.treeView.newProjectAdded.connect(lambda: self.toolBar.updateComboBox())

    def activeTabChanged(self, index):
        if index == -1:
            return
        syntax = "Assembly" if self.editorTabs.tabs[index].path[-1].lower() == "s" else "C"
        self.statusBar.comboBox.setCurrentText(syntax)
        self.changeEditorSyntax(syntax)

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
        for proxy in self.editorTabs.tabs:
            if proxy.hasUnsavedChanges:
                msg = QMessageBox()
                msg.setParent(None)
                msg.setModal(True)
                msg.setWindowTitle("Confirm Exit")
                msg.setText("The file {}/{} has been modified.".format(proxy.parent.path, proxy.path))
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

        self.menuBar.showTerminal.triggered.connect(lambda: self.terminal.show())
        self.menuBar.hideTerminal.triggered.connect(lambda: self.terminal.hide())
        self.menuBar.showTree.triggered.connect(lambda: self.treeDock.show())
        self.menuBar.hideTree.triggered.connect(lambda: self.treeDock.hide())

    def newWorkspaceAction(self):
        workspace = WorkspaceNode()
        name = QFileDialog.getExistingDirectory(self, "New workspace", "select new workspace directory")
        if name:
            workspace.path = name
            proxy = WorkspaceProxy()
            proxy.path = name
            workspace.proxy = proxy
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
        projects = self.treeView.getProjects()
        if projects:
            self.configurationManager.allProjects.clear()
            self.configurationManager.allProjects.extend(projects)
        self.toolBar.updateComboBox()
        self.treeView.expandAll()
        self.terminal.executeCommand("cd {}".format(self.workspace.path))

    def addToolBarEventHandlers(self):
        self.toolBar.compile.triggered.connect(self.compileAction)
        self.toolBar.run.triggered.connect(self.runAction)
        self.toolBar.debug.triggered.connect(self.debugAction)

    def debugAction(self):
        currentProject: ProjectNode = self.configurationManager.currentProject
        if currentProject:
            commandString = currentProject.proxy.getProjectDebugCommand()
            self.terminal.console.setFocus()
            if self.terminal.executeCommand(currentProject.proxy.getProjectCompileCommand()):
                self.terminal.executeCommand(commandString)

    def runAction(self):
        currentProject: ProjectNode = self.configurationManager.currentProject
        if currentProject:
            commandString = currentProject.proxy.getProjectRunCommand()
            self.terminal.console.setFocus()
            if self.terminal.executeCommand(currentProject.proxy.getProjectCompileCommand()):
                self.terminal.executeCommand(commandString)

    def checkExecutable(self):
        if self.editor.filePath:
            destination = self.editor.filePath[:-1] + "out"
            return os.path.exists(destination)
        return None

    def compileAction(self):
        currentProject: ProjectNode = self.configurationManager.currentProject
        if currentProject:
            commandString = currentProject.proxy.getProjectCompileCommand()
            self.terminal.console.setFocus()
            self.terminal.executeCommand(commandString)

    def loadFileText(self, fileProxy):
        text = self.openFileAction(fileProxy)
        fileProxy.text = text
        fileProxy.hasUnsavedChanges = False
        if fileProxy.getFilePath()[-1].lower() == "c":
            currentText = "C"
        else:
            currentText = "Assembly"
        update = True
        if len(self.editorTabs.tabs) == 0:
            self.editorTabs.tabs.append(fileProxy)
            update = False
        self.editorTabs.addNewTab(fileProxy, update)
        self.statusBar.comboBox.setCurrentText(currentText)

    def saveFileAction(self):
        proxy = self.editorTabs.getCurrentFileProxy()
        if proxy:
            with open(proxy.getFilePath(), 'w') as file:
                file.write(proxy.text)
                proxy.hasUnsavedChanges = False
        return True

    def openFileAction(self, fileName: FileProxy):
        text = None
        if fileName.text:
            return fileName.text
        with open(fileName.getFilePath(), 'r') as file:
            text = file.read()
        return text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ide = AsemblerIDE()
    ide.show()
    app.exec_()
