from src.model.Node import Node
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMenu, QAction, QMessageBox
from src.view.NewFileDialog import NewFileDialog
from src.model.AssemblyFileNode import AssemblyFileNode, AssemblyFileProxy
from src.model.CFileNode import CFileNode, CFileProxy
import os


class ProjectProxy(object):

    def __init__(self):
        self.path = None
        self.files = []
        self.parent = None

    def addFile(self, proxy):
        self.files.append(proxy)


class ProjectNode(Node):

    def __init__(self):
        super(ProjectNode, self).__init__()
        self.menu = QMenu()
        self.proxy = ProjectProxy()
        self.saveAction = QAction("Save project")
        self.deleteAction = QAction("Remove project")
        self.renameAction = QAction("Rename project")
        self.compileAction = QAction("Compile project")
        self.runAction = QAction("Run project")
        self.newFileAction = QAction("New file")
        self.menu.addAction(self.saveAction)
        self.menu.addAction(self.compileAction)
        self.menu.addAction(self.runAction)
        self.menu.addSeparator()
        self.menu.addAction(self.newFileAction)
        self.menu.addSeparator()
        self.menu.addAction(self.renameAction)
        self.menu.addAction(self.deleteAction)

        self.connectActions()

    def getContextMenu(self) -> QMenu:
        return self.menu

    def connectActions(self):
        self.newFileAction.triggered.connect(self.createNewFile)
        self.deleteAction.triggered.connect(self.deleteProject)

    def createNewFile(self):
        dialog = NewFileDialog()
        dialog.exec_()
        if dialog.result:
            rootPath = os.path.join(self.parent().path, self.path, dialog.result)
            if os.path.exists(rootPath):
                msg = QMessageBox()
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("File with the same name already exists.")
                msg.setWindowTitle("File creation error")
                msg.exec_()
                return
            if dialog.result[-1] == "S":
                node = AssemblyFileNode()
            else:
                node = CFileNode()
            print(node)
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
        del self

    def loadProject(self):
        for proxy in self.proxy.files:
            file = None
            if isinstance(proxy, AssemblyFileProxy):
                file = AssemblyFileNode()
            elif isinstance(proxy, CFileProxy):
                file = CFileNode()
            proxy.parent = self.proxy
            file.setText(0, proxy.path)
            file.path = proxy.path
            file.proxy = proxy
            self.addChild(file)

