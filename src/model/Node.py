from PySide2.QtWidgets import QTreeWidgetItem, QMenu
from src.controller.PathManager import PathManager

class Node(QTreeWidgetItem):

    def __init__(self):
        super(Node, self).__init__()
        self.path = None

    def getContextMenu(self) -> QMenu:
        return QMenu()