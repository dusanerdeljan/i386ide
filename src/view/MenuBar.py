from PySide2.QtWidgets import QMenuBar, QAction, QMenu
from PySide2.QtGui import QKeySequence, QIcon


class MenuBar(QMenuBar):

    def __init__(self):
        super(MenuBar, self).__init__()
        self.setStyleSheet("background-color: #2D2D30; color: white; font-weight: 500")
        self.file = self.addMenu("File")
        self.edit = self.addMenu("Edit")
        self.view = self.addMenu("View")
        # self.run = self.addMenu("Run")
        self.help = self.addMenu("Help")

        self.createFileMenuItemActions()
        self.createEditMenuItemActions()
        self.createViewMenuItemActions()

    def createFileMenuItemActions(self):
        self.newWorkspaceAction = QAction(QIcon("resources/new_folder.png"), "New workspace", self)
        self.newWorkspaceAction.setShortcut(QKeySequence("Ctrl+N"))
        self.file.addAction(self.newWorkspaceAction)

        self.openWorkspaceAction = QAction(QIcon("resources/open_folder.png"), "Open workspace", self)
        self.openWorkspaceAction.setShortcut(QKeySequence("Ctrl+O"))
        self.file.addAction(self.openWorkspaceAction)

        self.switchWorkspaceAction = QAction(QIcon("resources/switch_folder.png"), "Switch workspace", self)
        self.switchWorkspaceAction.setShortcut((QKeySequence("Ctrl+W")))
        self.file.addAction(self.switchWorkspaceAction)

        self.saveWorkspaceAction = QAction(QIcon("resources/save_folder.png"), "Save workspace", self)
        self.saveWorkspaceAction.setShortcut(QKeySequence("Ctrl+Shift+S"))
        self.file.addAction(self.saveWorkspaceAction)

        self.saveAction = QAction(QIcon("resources/save_file.png"), "Save file", self)
        self.saveAction.setShortcut(QKeySequence("Ctrl+S"))
        self.file.addAction(self.saveAction)
        #
        # self.openAction = QAction("Open file", self)
        # self.openAction.setShortcut(QKeySequence("Ctrl+G"))
        # self.file.addAction(self.openAction)
        #
        # self.newAction = QAction("New file", self)
        # self.newAction.setShortcut(QKeySequence("Ctrl+F"))
        # self.file.addAction(self.newAction)

    def createEditMenuItemActions(self):
        self.editDefaultWorkspace = QAction(QIcon("resources/workspace.png"), "Edit default workspace", self)
        self.edit.addAction(self.editDefaultWorkspace)

    def createViewMenuItemActions(self):
        self.showTerminal = QAction("Show terminal", self)
        self.view.addAction(self.showTerminal)

        self.hideTerminal = QAction("Hide terminal", self)
        self.view.addAction(self.hideTerminal)

        self.showTree = QAction("Show project explorer", self)
        self.view.addAction(self.showTree)

        self.hideTree = QAction("Hide project explorer", self)
        self.view.addAction(self.hideTree)