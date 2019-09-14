from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QAction
from PySide2.QtCore import Qt, Signal
from src.model.WorkspaceNode import WorkspaceNode, WorkspaceProxy
from src.model.FileNode import FileNode, FileProxy
from src.model.ProjectNode import ProjectNode
from src.controller.ConfigurationManager import ConfigurationManager

class TreeView(QTreeWidget):

    fileDoubleCliked = Signal(FileProxy)
    newProjectAdded = Signal(ProjectNode)
    
    def __init__(self, configurationManager: ConfigurationManager):
        super(TreeView, self).__init__()
        self.configurationManager = configurationManager
        self.setStyleSheet("background-color: #44423E; color: white;")
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

    def setRoot(self, item: QTreeWidgetItem):
        self.clear()
        self.rootNode = item
        self.addTopLevelItem(item)
        self.setHeaderLabel(item.text(0))
        self.rootNode.eventManager.projectAdded.connect(self.newProject)
        item.setExpanded(True)