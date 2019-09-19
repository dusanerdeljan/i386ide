from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QAction
from PySide2.QtCore import Qt, Signal
from src.model.WorkspaceNode import WorkspaceNode, WorkspaceProxy
from src.model.FileNode import FileNode, FileProxy
from src.model.ProjectNode import ProjectNode, ProjectProxy
from src.controller.ConfigurationManager import ConfigurationManager

class TreeView(QTreeWidget):

    fileDoubleCliked = Signal(FileProxy)
    newProjectAdded = Signal(ProjectNode)
    workspaceReload = Signal(WorkspaceProxy)
    workspaceRename = Signal(str, WorkspaceProxy)

    projectCompile = Signal(ProjectProxy)
    projectDebug = Signal(ProjectProxy)
    projectRun = Signal(ProjectProxy)
    projectRemove = Signal(ProjectProxy)
    projectRename = Signal(str, ProjectNode)

    fileRemove = Signal(FileProxy)
    fileRename = Signal(str, FileProxy)
    
    def __init__(self, configurationManager: ConfigurationManager):
        super(TreeView, self).__init__()
        self.configurationManager = configurationManager
        self.setStyleSheet("background-color: #2D2D30; color: white;")
        self.setColumnCount(1)
        self.setHeaderLabel("Workspace explorer")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.rootNode: WorkspaceNode = None

    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.pos())
        if not item:
            return
        super(TreeView, self).mouseDoubleClickEvent(event)
        if isinstance(item, FileNode):
            self.fileDoubleCliked.emit(item.proxy)

    def showContextMenu(self, pos):
        item = self.itemAt(pos)
        if not item:
            return
        menu = item.getContextMenu()
        if menu:
            menu.exec_(self.viewport().mapToGlobal(pos))


    def addNode(self, parent: QTreeWidgetItem, item: QTreeWidgetItem):
        parent.addChild(item)

    def getProjects(self):
        children = []
        if self.rootNode:
            for childIndex in range(0, self.rootNode.childCount()):
                children.append(self.rootNode.child(childIndex))
        return children

    def newProject(self, project: ProjectNode):
        self.configurationManager.allProjects.append(project)
        self.newProjectAdded.emit(project)

    def removeProject(self, project: ProjectNode):
        self.configurationManager.allProjects.remove(project)
        self.projectRemove.emit(project.proxy)

    def renameProject(self, oldPath, project: ProjectNode):
        self.projectRename.emit(oldPath, project)

    def connectWorkspaceEventHandlers(self):
        self.rootNode.eventManager.projectAdded.connect(self.newProject)
        self.rootNode.eventManager.projectCompile.connect(lambda proxy: self.projectCompile.emit(proxy))
        self.rootNode.eventManager.projectDebug.connect(lambda proxy: self.projectDebug.emit(proxy))
        self.rootNode.eventManager.projectRun.connect(lambda proxy: self.projectRun.emit(proxy))
        self.rootNode.eventManager.projectRemove.connect(self.removeProject)
        self.rootNode.eventManager.projectRename.connect(self.renameProject)
        self.rootNode.eventManager.workspaceReload.connect(lambda wsProxy: self.workspaceReload.emit(wsProxy))
        self.rootNode.eventManager.workspaceRename.connect(lambda oldPath, wsProxy: self.workspaceRename.emit(oldPath, wsProxy))
        self.rootNode.eventManager.fileRemove.connect(lambda fileProxy: self.fileRemove.emit(fileProxy))
        self.rootNode.eventManager.fileRename.connect(lambda oldPath, fileProxy: self.fileRename.emit(oldPath, fileProxy))

    def setRoot(self, item: QTreeWidgetItem):
        self.clear()
        self.rootNode = item
        self.addTopLevelItem(item)
        self.setHeaderLabel(item.text(0))
        self.connectWorkspaceEventHandlers()
        item.setExpanded(True)