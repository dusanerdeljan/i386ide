from PySide2.QtWidgets import QTreeWidgetItem, QMenu


class Node(QTreeWidgetItem):

    def __init__(self):
        super(Node, self).__init__()

    def getContextMenu(self) -> QMenu:
        return QMenu()