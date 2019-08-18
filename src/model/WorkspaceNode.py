from PySide2.QtWidgets import QMenu, QAction, QInputDialog, QLineEdit, QMessageBox
from src.model.Node import Node
from src.model.ProjectNode import ProjectNode, ProjectProxy
import os
import pickle


class WorkspaceProxy(object):

    def __init__(self):
        self.path = None
        self.projects = []

    def addProject(self, projectProxy):
        self.projects.append(projectProxy)


class WorkspaceNode(Node):
    
    def __init__(self):
        super(WorkspaceNode, self).__init__()
        self.menu = QMenu()
        self.proxy = WorkspaceProxy()
        self.newProjectAction = QAction("New project")
        self.saveAction = QAction("Save workspace")
        self.renameAction = QAction("Rename workspace")
        self.switchAction = QAction("Switch workspace")
        self.menu.addAction(self.newProjectAction)
        self.menu.addAction(self.saveAction)
        self.menu.addAction(self.switchAction)
        self.menu.addAction(self.renameAction)

        self.connectActions()

    def getContextMenu(self) -> QMenu:
        return self.menu

    def connectActions(self):
        self.newProjectAction.triggered.connect(self.createNewProject)
        self.saveAction.triggered.connect(self.saveWorkspace)

    def createNewProject(self):
        name, entered = QInputDialog.getText(None, "New project", "Enter project name: ", QLineEdit.Normal, "New project")
        if entered:
            if os.path.exists(os.path.join(self.path, name)):
                msg = QMessageBox()
                msg.setModal(True)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Folder with the same name already exists.")
                msg.setWindowTitle("Project creation error")
                msg.exec_()
                return
            project = ProjectNode()
            project.path = name
            project.proxy.path = name
            project.proxy.parent = self.proxy
            project.setText(0, name)
            self.addChild(project)
            newPath = os.path.join(self.path, name)
            os.mkdir(newPath)
            self.proxy.addProject(project.proxy)

    def saveWorkspace(self):
        with open(os.path.join(self.path, '.metadata'), 'wb') as metadata:
            pickle.dump(self.proxy, metadata, protocol=pickle.HIGHEST_PROTOCOL)

    def loadWorkspace(self):
        for projectProxy in self.proxy.projects:
            projectProxy.parent = self.proxy
            project = ProjectNode()
            project.setText(0, projectProxy.path)
            project.path = projectProxy.path
            project.proxy = projectProxy
            project.loadProject()
            self.addChild(project)