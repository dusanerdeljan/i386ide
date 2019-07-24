from PySide2.QtWidgets import QMenuBar, QAction, QMenu
from PySide2.QtGui import QKeySequence


class MenuBar(QMenuBar):

    def __init__(self):
        super(MenuBar, self).__init__()
        self.setStyleSheet("background-color: #676867; border-bottom: 2px solid grey; color: white; font-weight: 500")
        self.file = self.addMenu("File")
        self.edit = self.addMenu("Edit")
        self.view = self.addMenu("View")
        self.run = self.addMenu("Run")
        self.help = self.addMenu("Help")

        self.createFileMenuItemActions()
        self.createEditMenuItemActions()
        self.createViewMenuItemActions()

    def createFileMenuItemActions(self):
        self.saveAction = QAction("Save file", self)
        self.saveAction.setShortcut(QKeySequence("Ctrl+S"))
        self.file.addAction(self.saveAction)

        self.openAction = QAction("Open file", self)
        self.openAction.setShortcut(QKeySequence("Ctrl+O"))
        self.file.addAction(self.openAction)

        self.newAction = QAction("New file", self)
        self.newAction.setShortcut(QKeySequence("Ctrl+N"))
        self.file.addAction(self.newAction)

    def createEditMenuItemActions(self):
        self.compileConfiguration = QAction("Compiler configuration", self)
        self.compileConfiguration.setShortcut(QKeySequence("Ctrl+Shift+C"))
        self.edit.addAction(self.compileConfiguration)

        self.debugConfiguration = QAction("Debug configuration", self)
        self.debugConfiguration.setShortcut(QKeySequence("Ctrl+Shift+D"))
        self.edit.addAction(self.debugConfiguration)

        self.runConfiguration = QAction("Run configuration", self)
        self.runConfiguration.setShortcut(QKeySequence("Ctrl+Shift+R"))
        self.edit.addAction(self.runConfiguration)

    def createViewMenuItemActions(self):
        self.showTerminal = QAction("Show terminal", self)
        self.view.addAction(self.showTerminal)

        self.hideTerminal = QAction("Hide terminal", self)
        self.view.addAction(self.hideTerminal)

        self.showTree = QAction("Show project explorer", self)
        self.view.addAction(self.showTree)

        self.hideTree = QAction("Hide project explorer", self)
        self.view.addAction(self.hideTree)