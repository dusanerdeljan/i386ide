from src.model.Node import Node
from PySide2.QtGui import QIcon
from PySide2.QtCore import Signal, QObject
from PySide2.QtWidgets import QMenu, QAction, QMessageBox
from src.view.NewFileDialog import NewFileDialog
from src.model.AssemblyFileNode import AssemblyFileNode, AssemblyFileProxy
from src.model.CFileNode import CFileNode, CFileProxy
import os
import re


class ProjectProxy(object):

    def __init__(self):
        self.path = None
        self.files = []
        self.parent = None

    def addFile(self, proxy):
        self.files.append(proxy)

    def getProjectPath(self):
        return os.path.join(self.parent.path, self.path)

    def getProjectCompileCommand(self):
        destination = os.path.join(self.getProjectPath(), "{}.out".format(self.path))
        cFiles = []
        sFiles = []
        for file in self.files:
            if isinstance(file, CFileProxy):
                cFiles.append(file.getFilePath())
            elif isinstance(file, AssemblyFileProxy):
                sFiles.append(file.getFilePath())
        print(self.files)
        command = ['gcc', '-g', '-m32', '-o', destination]
        if cFiles:
            command.extend(cFiles)
        if sFiles:
            command.extend(sFiles)
        return ' '.join(command)

    def getProjectDebugCommand(self):
        return "ddd {}.out".format(os.path.join(self.getProjectPath(), self.path))

    def getProjectRunCommand(self):
        return "{}.out".format(os.path.join(self.getProjectPath(), self.path))


class ProjectEventManager(QObject):

    projectCompileRequested = Signal(ProjectProxy)
    projectDebugRequested = Signal(ProjectProxy)
    projectRunRequested = Signal(ProjectProxy)

    def __init__(self):
        super(ProjectEventManager, self).__init__()


class ProjectNode(Node):

    def __init__(self):
        super(ProjectNode, self).__init__()
        self.eventManager = ProjectEventManager()
        self.menu = QMenu()
        self.proxy = ProjectProxy()
        self.saveAction = QAction("Save project")
        self.deleteAction = QAction("Remove project")
        self.renameAction = QAction("Rename project")
        self.compileAction = QAction("Compile project")
        self.runAction = QAction("Run project")
        self.debugAction = QAction("Debug project")
        self.newFileAction = QAction("New file")
        self.menu.addAction(self.saveAction)
        self.menu.addAction(self.compileAction)
        self.menu.addAction(self.debugAction)
        self.menu.addAction(self.runAction)
        self.menu.addSeparator()
        self.menu.addAction(self.newFileAction)
        self.menu.addSeparator()
        self.menu.addAction(self.renameAction)
        self.menu.addAction(self.deleteAction)

        self.connectActions()

    def getContextMenu(self) -> QMenu:
        return self.menu

    def __str__(self):
        return self.proxy.path

    def connectActions(self):
        self.newFileAction.triggered.connect(self.createNewFile)
        self.deleteAction.triggered.connect(self.deleteProject)
        self.compileAction.triggered.connect(lambda: self.eventManager.projectCompileRequested.emit(self.proxy))
        self.debugAction.triggered.connect(lambda: self.eventManager.projectDebugRequested.emit(self.proxy))
        self.runAction.triggered.connect(lambda: self.eventManager.projectRunRequested.emit(self.proxy))

    def createNewFile(self):
        dialog = NewFileDialog()
        dialog.exec_()
        if dialog.result:
            rootPath = os.path.join(self.parent().path, self.path, dialog.result)
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if " " in dialog.result or regex.search(dialog.result):
                msg = QMessageBox()
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("File name cannot contain whitespace or special characters.")
                msg.setWindowTitle("File creation error")
                msg.exec_()
                return
            if os.path.exists(rootPath):
                msg = QMessageBox()
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("File with the same name already exists.")
                msg.setWindowTitle("File creation error")
                msg.exec_()
                return
            node = None
            if dialog.result[-1] == "S":
                node = AssemblyFileNode()
            else:
                node = CFileNode()
            node.setText(0, dialog.result)
            node.path = dialog.result
            if isinstance(node, AssemblyFileNode):
                node.proxy = AssemblyFileProxy()
            elif isinstance(node, CFileNode):
                node.proxy = CFileProxy()
            node.proxy.path = dialog.result
            node.proxy.parent = self.proxy
            self.addChild(node)
            os.mknod(rootPath)
            self.proxy.addFile(node.proxy)


    def deleteProject(self):
        answer = QMessageBox.question(None, "Delete project", "Are you sure you want to delete project {}".format(self.text(0)), QMessageBox.Yes | QMessageBox.No)
        if not answer == QMessageBox.Yes:
            return
        for child in self.takeChildren():
            del child
        self.parent().removeChild(self)
        self.proxy.parent.projects.remove(self.proxy)

    def loadProject(self):
        for proxy in self.proxy.files:
            file = None
            if isinstance(proxy, AssemblyFileProxy):
                file = AssemblyFileNode()
            elif isinstance(proxy, CFileProxy):
                file = CFileNode()
            if file:
                proxy.parent = self.proxy
                file.setText(0, proxy.path)
                file.path = proxy.path
                file.proxy = proxy
                self.addChild(file)
        # load assembly and C files which are not added through the IDE but are the part of project folder
        projectPath = self.proxy.getProjectPath()
        for filePath in os.listdir(projectPath):
            if filePath not in [file.path for file in self.proxy.files]:
                node = None
                proxy = None
                if filePath.lower().endswith(".s"):
                    node = AssemblyFileNode()
                    proxy = AssemblyFileProxy()
                elif filePath.lower().endswith(".c"):
                    node = CFileNode()
                    proxy = CFileProxy()
                if node:
                    proxy.path = filePath
                    node.setText(0, filePath)
                    node.path = filePath
                    node.proxy = proxy
                    node.proxy.parent = self.proxy
                    self.addChild(node)
                    self.proxy.files.append(node.proxy)


