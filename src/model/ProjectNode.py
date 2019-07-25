from src.model.Node import Node
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMenu, QAction, QMessageBox
from src.view.NewFileDialog import NewFileDialog
from src.model.AssemblyFileNode import AssemblyFileNode
from src.model.CFileNode import CFileNode


class ProjectNode(Node):

    def __init__(self):
        super(ProjectNode, self).__init__()
        self.menu = QMenu()
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
            node = AssemblyFileNode if dialog.result[-1].lower() == "S" else CFileNode()
            node.setText(0, dialog.result)
            self.addChild(node)

    def deleteProject(self):
        answer = QMessageBox.question(None, "Delete project", "Are you sure you want to delete project {}".format(self.text(0)), QMessageBox.Yes | QMessageBox.No)
        if not answer == QMessageBox.Yes:
            return
        for child in self.takeChildren():
            del child
        self.parent().removeChild(self)
