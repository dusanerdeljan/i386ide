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

import sys
import os
import pickle
import re
import platform
from PySide2.QtWidgets import QMainWindow, QLineEdit, QApplication, QFileDialog, QMessageBox, QDockWidget, QLabel, QInputDialog
from PySide2.QtCore import Qt, QDir, QTimer
from PySide2.QtGui import QIcon
from src.view.MenuBar import MenuBar
from src.view.Terminal import Terminal
from src.view.ToolBar import ToolBar
from src.view.StatusBar import StatusBar
from src.view.TreeView import TreeView
from src.view.HelpWidget import HelpWidget
from src.view.TabWidget import EditorTabWidget, EditorTab
from src.view.WorkspaceConfigurationEditor import WorkspaceConfigurationEditor
from src.view.DefaultWorkspaceEditor import DefaultWorkspaceEditor
from src.view.AsciiTableWidget import AsciiTableWidget
from src.view.SnippetEditor import SnippetEditor
from src.view.SettingsEditor import SettingsEditor
from src.view.AboutDialog import AboutDialog
from src.util.AsemblerSintaksa import AsemblerSintaksa
from src.util.CSyntax import CSyntax
from src.model.ProjectNode import ProjectNode, ProjectProxy
from src.model.AssemblyFileNode import AssemblyFileNode
from src.model.CFileNode import CFileNode
from src.model.WorkspaceNode import WorkspaceNode, WorkspaceProxy
from src.model.FileNode import FileProxy
from src.controller.ConfigurationManager import ConfigurationManager
from src.controller.WorkspaceConfiguration import WorkspaceConfiguration
from src.controller.PathManager import PathManager
from src.controller.SnippetManager import SnippetManager
from src.controller.TooltipManager import TooltipManager
from time import localtime, strftime

class AsemblerIDE(QMainWindow):

    def __init__(self):
        super(AsemblerIDE, self).__init__()
        self.workspace = None
        PathManager.START_DIRECTORY = os.getcwd()
        self.workspaceConfiguration = WorkspaceConfiguration.loadConfiguration()
        self.snippetManager = SnippetManager.loadSnippetConfiguration()
        self.tooltipManager = TooltipManager.loadTooltipConfiguration()
        self.configurationManager = ConfigurationManager()
        self.editorTabs = EditorTabWidget(self.snippetManager, self.tooltipManager)
        self.menuBar = MenuBar()
        self.terminal = Terminal()
        self.toolBar = ToolBar(self.configurationManager)
        self.statusBar = StatusBar()
        self.treeView = TreeView(self.configurationManager)
        self.help = HelpWidget()
        self.ascii = AsciiTableWidget()
        self.setStatusBar(self.statusBar)
        self.addToolBar(self.toolBar)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.terminal)
        self.addDockWidget(Qt.RightDockWidgetArea, self.help)
        self.addDockWidget(Qt.RightDockWidgetArea, self.ascii)
        self.splitDockWidget(self.help, self.ascii, Qt.Vertical)
        self.treeDock = QDockWidget()
        self.treeDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.treeDock.setStyleSheet("background-color: #2D2D30; color: white;")
        self.treeDock.setFeatures(QDockWidget.DockWidgetMovable)
        self.treeDock.setWidget(self.treeView)
        self.treeDock.setTitleBarWidget(QLabel("Workspace explorer"))
        self.addDockWidget(Qt.LeftDockWidgetArea, self.treeDock)
        self.setMenuBar(self.menuBar)
        self.setMinimumSize(1200, 800)
        self.setWindowTitle("i386 Assembly Integrated Development Environment")
        self.setCentralWidget(self.editorTabs)
        self.setStyleSheet("background-color: #3E3E42; color: white;")
        self.setWindowIcon(QIcon(resource_path("resources/app_icon.ico")))

        self.addTabWidgetEventHandlers()
        self.addMenuBarEventHandlers()
        self.addToolBarEventHandlers()
        self.addTreeViewEventHandlers()
        self.checkWorkspaceConfiguration()
        #self.populateTreeView()
        self.statusBar.comboBox.currentTextChanged.connect(self.changeEditorSyntax)
        self.statusBar.tabWidthComboBox.currentTextChanged.connect(self.changeEditorTabWidth)
        self.timer = QTimer()
        self.timer.start(600000)
        self.timer.timeout.connect(self.makeBackupSave)

    def makeBackupSave(self):
        self.workspace.saveBackup()

    def changeEditorTabWidth(self, text):
        currentTab: EditorTab = self.editorTabs.getCurrentTab()
        if currentTab:
            currentTab.editor.tabSize = int(text)


    def changeEditorSyntax(self, text):
        currentTab: EditorTab = self.editorTabs.getCurrentTab()
        if currentTab:
            if text == "Assembly":
                currentTab.editor.sintaksa = AsemblerSintaksa(currentTab.editor.document())
            elif text == "C":
                currentTab.editor.sintaksa = CSyntax(currentTab.editor.document())
            currentTab.editor.update()

    def checkWorkspaceConfiguration(self):
        defaultWorkspace = self.workspaceConfiguration.getDefaultWorkspace()
        if defaultWorkspace:
            if self.openWorkspaceAction(defaultWorkspace):
                self.show()
                return
            else:
                self.workspaceConfiguration.removeWorkspace(defaultWorkspace)
        dialog = WorkspaceConfigurationEditor(self.workspaceConfiguration, self)
        if dialog.exec_():
            self.show()
        else:
            sys.exit(0)

    def addTabWidgetEventHandlers(self):
        self.editorTabs.currentChanged.connect(self.activeTabChanged)

    def addTreeViewEventHandlers(self):
        self.treeView.fileDoubleCliked.connect(self.loadFileText)
        self.treeView.workspaceReload.connect(lambda wsProxy: self.openWorkspaceAction(wsProxy.path))
        self.treeView.workspaceRename.connect(lambda oldPath, wsProxy: self.workspaceConfiguration.replaceWorkpsace(oldPath, wsProxy.path))
        self.treeView.newProjectAdded.connect(lambda: self.toolBar.updateComboBox())
        self.treeView.projectCompile.connect(lambda proxy: self.compileAction(proxy))
        self.treeView.projectDebug.connect(lambda proxy: self.debugAction(proxy))
        self.treeView.projectRun.connect(lambda proxy: self.runAction(proxy))
        self.treeView.projectRemove.connect(lambda proxy: self.removeProject(proxy))
        self.treeView.projectRename.connect(lambda oldPath, project: self.renameProject(oldPath, project))
        self.treeView.fileRemove.connect(lambda fileProxy: self.removeFile(fileProxy))
        self.treeView.fileRename.connect(lambda oldPath, fileProxy: self.renameFile(oldPath, fileProxy))
        self.treeView.fileSave.connect(lambda fileProxy: self.updateEditorTrie(fileProxy))

    def renameFile(self, oldPath: str, fileProxy: FileProxy):
        # fileProxy.text = None
        key = "{}/{}".format(fileProxy.parent.path, oldPath)
        if key in self.editorTabs.projectTabs:
            newKey = "{}/{}".format(fileProxy.parent.path, fileProxy.path)
            tab = self.editorTabs.projectTabs.pop(key)
            self.editorTabs.projectTabs[newKey] = tab
            tab.tabName = newKey
            index = self.editorTabs.tabs.index(fileProxy)
            self.editorTabs.setTabText(index, newKey)

    def renameProject(self, oldPath: str, project: ProjectNode):
        self.toolBar.updateComboBox()
        for fileProxy in project.proxy.files:
            oldKey = "{}/{}".format(oldPath, fileProxy.path)
            if oldKey in self.editorTabs.projectTabs:
                newKey = "{}/{}".format(project.proxy.path, fileProxy.path)
                tab = self.editorTabs.projectTabs.pop(oldKey)
                self.editorTabs.projectTabs[newKey] = tab
                tab.tabName = newKey
                index = self.editorTabs.tabs.index(fileProxy)
                self.editorTabs.setTabText(index, newKey)

    def removeFile(self, proxy: FileProxy):
        key = "{}/{}".format(proxy.parent.path, proxy.path)
        if key in self.editorTabs.projectTabs:
            self.editorTabs.closeTab(self.editorTabs.tabs.index(proxy), askToSave=False)

    def removeProject(self, proxy: ProjectProxy):
        for file in proxy.files:
            if file in self.editorTabs.tabs:
                self.editorTabs.closeTab(self.editorTabs.tabs.index(file), askToSave=False)
        self.toolBar.updateComboBox()

    def activeTabChanged(self, index):
        if index == -1:
            self.statusBar.tabWidthComboBox.setCurrentText('4')
            return
        syntax = "Assembly" if self.editorTabs.tabs[index].path[-1].lower() == "s" else "C"
        proxy = self.editorTabs.tabs[index]
        key = "{}/{}".format(proxy.parent.path, proxy.path)
        self.statusBar.comboBox.setCurrentText(syntax)
        self.statusBar.tabWidthComboBox.setCurrentText(str(self.editorTabs.projectTabs[key].editor.tabSize))
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
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setParent(None)
                msg.setModal(True)
                msg.setWindowTitle("Confirm Exit")
                msg.setText("The file {}/{} has been modified.".format(proxy.parent.path, proxy.path))
                msg.setInformativeText("Do you want to save the changes?")
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
        self.workspaceConfiguration.saveConfiguration()
        self.snippetManager.saveConfiguration()
        self.tooltipManager.saveConfiguration()
        self.workspace.proxy.closedNormally = True
        self.saveWorkspaceAction()
        super(AsemblerIDE, self).closeEvent(event)

    def addMenuBarEventHandlers(self):
        self.menuBar.newWorkspaceAction.triggered.connect(self.newWorkspaceAction)
        self.menuBar.saveWorkspaceAction.triggered.connect(self.saveWorkspaceAction)
        self.menuBar.openWorkspaceAction.triggered.connect(self.openWorkspaceAction)
        self.menuBar.switchWorkspaceAction.triggered.connect(self.switchWorkspaceAction)

        self.menuBar.saveAction.triggered.connect(self.saveFileAction)
        self.menuBar.editDefaultWorkspace.triggered.connect(self.editDefaultWorkspaceConfiguration)
        self.menuBar.editCodeSnippets.triggered.connect(self.editCodeSnippets)
        self.menuBar.editSettings.triggered.connect(self.editSettings)

        self.menuBar.showTerminal.triggered.connect(lambda: self.terminal.show())
        self.menuBar.hideTerminal.triggered.connect(lambda: self.terminal.hide())
        self.menuBar.showTree.triggered.connect(lambda: self.treeDock.show())
        self.menuBar.hideTree.triggered.connect(lambda: self.treeDock.hide())
        self.menuBar.showHelp.triggered.connect(lambda: self.help.show())
        self.menuBar.hideHelp.triggered.connect(lambda: self.help.hide())
        self.menuBar.showAscii.triggered.connect(lambda: self.ascii.show())
        self.menuBar.hideAscii.triggered.connect(lambda: self.ascii.hide())

        self.menuBar.aboutAction.triggered.connect(self.showAbout)

    def showAbout(self):
        dialog = AboutDialog()
        dialog.exec_()

    def switchWorkspaceAction(self):
        dialog = WorkspaceConfigurationEditor(self.workspaceConfiguration, self, switch=True)
        if dialog.exec_() and dialog.workspaceDirectory:
            self.workspace.proxy.closedNormally = True
            self.saveWorkspaceAction()
            if not self.editorTabs.closeAllTabs():
                return
            self.openWorkspaceAction(dialog.workspaceDirectory)

    def editDefaultWorkspaceConfiguration(self):
        editor = DefaultWorkspaceEditor(self.workspaceConfiguration)
        if editor.exec_():
            self.workspaceConfiguration.saveConfiguration()

    def editCodeSnippets(self):
        editor = SnippetEditor(self.snippetManager)
        if editor.exec_():
            self.snippetManager.saveConfiguration()

    def editSettings(self):
        editor = SettingsEditor(self.tooltipManager)
        if editor.exec_():
            self.tooltipManager.saveConfiguration()

    def newWorkspaceAction(self):
        if not self.editorTabs.closeAllTabs():
            return False
        workspace = WorkspaceNode()
        name = QFileDialog.getExistingDirectory(self, "New workspace", "select new workspace directory")
        if name:
            wsname = name[name.rindex(os.path.sep)+1:]
            regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
            if ' ' in name or regex.search(wsname):
                msg = QMessageBox()
                msg.setStyleSheet("background-color: #2D2D30; color: white;")
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Workspace path/name cannot contain whitespace or special characters.")
                msg.setWindowTitle("Workspace creation error")
                msg.exec_()
                return False
            workspace.path = name
            proxy = WorkspaceProxy()
            proxy.path = name
            workspace.proxy = proxy
            workspace.setIcon(0, QIcon(resource_path("resources/workspace.png")))
            workspace.setText(0, wsname)
            self.workspace = workspace
            self.treeView.setRoot(self.workspace)
            self.saveWorkspaceAction()
            self.configurationManager.allProjects = []
            self.configurationManager.currentProject = None
            self.toolBar.updateComboBox()
            self.terminal.executeCommand("cd {}".format(self.workspace.path))
            self.workspaceConfiguration.addWorkspace(self.workspace.proxy.path)
            return True
        return False

    def saveWorkspaceAction(self):
        if self.workspace:
            self.workspace.saveWorkspace()

    def openWorkspaceAction(self, workspacePath=None):
        if not self.editorTabs.closeAllTabs():
            return
        if not workspacePath:
            name = QFileDialog.getExistingDirectory(self, "Open workspace", "select new workspace directory")
            if not name:
                return
        else:
            name = workspacePath
        regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
        if ' ' in name or regex.search(os.path.basename(name)):
            msg = QMessageBox()
            msg.setStyleSheet("background-color: #2D2D30; color: white;")
            msg.setModal(True)
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Workspace path/name cannot contain whitespace or special characters.")
            msg.setWindowTitle("Workspace creation error")
            msg.exec_()
            return False
        workspace = WorkspaceProxy()
        path = os.path.join(name, ".metadata")
        if os.path.exists(path):
            with open(path, 'rb') as file:
                workspace = pickle.load(file)
        self.workspace = WorkspaceNode()
        self.workspace.proxy = workspace
        try:
            closed_normally = self.workspace.proxy.closedNormally
            if not closed_normally:
                decision = self.restoreBackupMessage(name)
                if decision:
                    if self.openBackupAction(workspacePath):
                        return True
                    else:
                        msg = QMessageBox()
                        msg.setStyleSheet("background-color: #2D2D30; color: white;")
                        msg.setModal(True)
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText(
                            "Failed to load {} because it is deleted from the disk."
                            "\nRegular workspace save will be restored.".format(".backup workspace file"))
                        msg.setWindowTitle("Failed to load backup workspace.")
                        msg.exec_()

            self.workspace.setIcon(0, QIcon(resource_path("resources/workspace.png")))
            self.workspace.setText(0, name[name.rindex(os.path.sep) + 1:])
            self.workspace.path = name
            self.workspace.proxy.path = name
            self.workspace.proxy.closedNormally = False
            success = self.workspace.loadWorkspace()
            if not success:
                return False
            self.treeView.setRoot(self.workspace)
            projects = self.treeView.getProjects()
            if projects:
                self.configurationManager.allProjects.clear()
                self.configurationManager.allProjects.extend(projects)
            self.toolBar.updateComboBox()
            self.treeView.expandAll()
            self.terminal.executeCommand("cd {}".format(self.workspace.path))
            self.workspaceConfiguration.addWorkspace(self.workspace.proxy.path)
            if workspacePath:
                self.workspace.saveWorkspace(workspacePath)
            return True

        except:
            self.workspace.proxy.closedNormally = True
            self.workspace.path = workspacePath
            self.workspace.proxy.path = workspacePath
            self.workspace.saveWorkspace(workspacePath)
            return self.openWorkspaceAction(workspacePath)

    def restoreBackupMessage(self, wsName):
        try:
            msg = QMessageBox()
            msg.setStyleSheet("background-color: #2D2D30; color: white;")
            msg.setParent(None)
            msg.setModal(True)
            msg.setWindowTitle("Workspace recovery")
            time = strftime('%m/%d/%Y %H:%M:%S', localtime(os.path.getmtime(os.path.join(wsName, ".backup"))))
            msg.setText("The workplace {} was closed unexpectedly.\n"
                        "\nTime the backup was created: {}".format(wsName, time))
            msg.setInformativeText("Would you like to recover from backup?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.Yes)
            retValue = msg.exec_()
            if retValue == QMessageBox.Yes:
                return True
            else:
                return
        except:
            return False

    def openBackupAction(self, workspacePath):
        name = workspacePath
        workspace = WorkspaceProxy()
        path = os.path.join(name, ".backup")
        if os.path.exists(path):
            with open(path, 'rb') as file:
                workspace = pickle.load(file)
        else:
            return False
        self.workspace = WorkspaceNode()
        self.workspace.proxy = workspace
        self.workspace.setIcon(0, QIcon(resource_path("resources/workspace.png")))
        self.workspace.setText(0, name[name.rindex(os.path.sep) + 1:])
        self.workspace.path = name
        self.workspace.proxy.path = name
        self.workspace.proxy.closedNormally = False
        success = self.workspace.loadBackupWorkspace(workspacePath)
        if not success:
            return False
        self.treeView.setRoot(self.workspace)
        projects = self.treeView.getProjects()
        if projects:
            self.configurationManager.allProjects.clear()
            self.configurationManager.allProjects.extend(projects)
        self.toolBar.updateComboBox()
        self.treeView.expandAll()
        self.terminal.executeCommand("cd {}".format(self.workspace.path))
        self.workspaceConfiguration.addWorkspace(self.workspace.proxy.path)
        if workspacePath:
            self.workspace.saveWorkspace(workspacePath)

        return True

    def addToolBarEventHandlers(self):
        self.toolBar.compile.triggered.connect(self.compileAction)
        self.toolBar.run.triggered.connect(self.runAction)
        self.toolBar.debug.triggered.connect(self.debugAction)

    def debugAction(self, projectProxy=None):
        currentProject: ProjectNode = self.configurationManager.currentProject
        proxy = None
        if projectProxy:
            proxy = projectProxy
        else:
            if currentProject:
                proxy = currentProject.proxy
        if proxy:
            commandString = proxy.getProjectDebugCommand()
            self.terminal.console.setFocus()
            if self.terminal.executeCommand(proxy.getProjectCompileCommand()):
                copmileString = proxy.getProjectCompileCommand()
                if ' -g ' not in copmileString:
                    msg = QMessageBox()
                    msg.setStyleSheet("background-color: #2D2D30; color: white;")
                    msg.setModal(True)
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Please set '-g' option in compiler configuration to be able to debug your project.")
                    msg.setWindowTitle("Debug warning")
                    msg.exec_()
                    return False
                self.terminal.executeCommand(commandString)
            self.toolBar.projectComboBox.setCurrentText(proxy.path)

    def runAction(self, projectProxy=None):
        currentProject: ProjectNode = self.configurationManager.currentProject
        proxy = None
        if projectProxy:
            proxy = projectProxy
        else:
            if currentProject:
                proxy = currentProject.proxy
        if proxy:
            commandString = proxy.getProjectRunCommand()
            self.terminal.console.setFocus()
            if self.terminal.executeCommand(proxy.getProjectCompileCommand()):
                self.terminal.executeCommand(commandString)
            self.toolBar.projectComboBox.setCurrentText(proxy.path)

    def compileAction(self, projectProxy=None):
        currentProject: ProjectNode = self.configurationManager.currentProject
        proxy = None
        if projectProxy:
            proxy = projectProxy
        else:
            if currentProject:
                proxy = currentProject.proxy
        if proxy:
            commandString = proxy.getProjectCompileCommand()
            self.terminal.console.setFocus()
            self.terminal.executeCommand(commandString)
            self.toolBar.projectComboBox.setCurrentText(proxy.path)

    def checkExecutable(self):
        if self.editor.filePath:
            destination = self.editor.filePath[:-1] + "out"
            return os.path.exists(destination)
        return None

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

    def updateEditorTrie(self, proxy: FileProxy):
        key = "{}/{}".format(proxy.parent.path, proxy.path)
        if key in self.editorTabs.projectTabs:
            self.editorTabs.projectTabs[key].editor.updateTrie()
            self.editorTabs.removeChangeIdentificator(proxy)

    def saveFileAction(self):
        if len(self.editorTabs.tabs):
            proxy = self.editorTabs.getCurrentFileProxy()
            if proxy and proxy.hasUnsavedChanges:
                with open(proxy.getFilePath(), 'w') as file:
                    file.write(proxy.text)
                    proxy.hasUnsavedChanges = False
                self.updateEditorTrie(proxy)
            self.saveWorkspaceAction()
            return True

    def openFileAction(self, fileName: FileProxy):
        text = None
        # if fileName.text:
        #     return fileName.text
        with open(fileName.getFilePath(), 'r') as file:
            text = file.read()
        return text


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        # base_path = PathManager.START_DIRECTORY
    except Exception:
        # base_path = os.path.abspath(".")
        base_path = PathManager.START_DIRECTORY

    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if platform.system() != "Linux":
        msg = QMessageBox()
        msg.setStyleSheet("background-color: #2D2D30; color: white;")
        msg.setModal(True)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("You are using {} and the only currently supported operating system is Linux.".format(platform.system()))
        msg.setWindowTitle("Unsupported operating system")
        msg.exec_()
        sys.exit(1)
    else:
        ide = AsemblerIDE()
    app.exec_()
