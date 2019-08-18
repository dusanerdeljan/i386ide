from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QAction
from PySide2.QtCore import Qt, Signal
from src.model.FileNode import FileNode, FileProxy
from src.model.ProjectNode import ProjectNode


class TreeView(QTreeWidget):

    fileDoubleCliked = Signal(FileProxy)
    
    def __init__(self):
        super(TreeView, self).__init__()
        self.setStyleSheet("background-color: #44423E; color: white;")
        self.setColumnCount(1)
        self.setHeaderLabel("Workspace explorer")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

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

    def setRoot(self, item: QTreeWidgetItem):
        self.clear()
        self.addTopLevelItem(item)
        self.setHeaderLabel(item.text(0))
        item.setExpanded(True)