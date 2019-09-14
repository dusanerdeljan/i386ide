from PySide2.QtWidgets import QToolBar, QPushButton, QAction, QComboBox, QLabel
from PySide2.QtGui import QKeySequence
from src.controller.ConfigurationManager import ConfigurationManager

class ProjectComboBox(QComboBox):

    def __init__(self, configurationManager):
        super(ProjectComboBox, self).__init__()
        self.configurationManager = configurationManager
        self.currentIndexChanged.connect(lambda x: self.configurationManager.setCurrentProject(self.currentData()))


class ToolBar(QToolBar):

    def __init__(self, configurationManager: ConfigurationManager):
        super(ToolBar, self).__init__()
        self.configurationManager = configurationManager
        self.setStyleSheet("background-color: #676867; border-bottom: 2px solid grey; color: white; font-weight: 500")
        self.setMovable(False)
        self.compile = QAction("Compile", self)
        self.compile.setShortcut(QKeySequence("Ctrl+Shift+B"))
        self.debug = QAction("Debug", self)
        self.debug.setShortcut(QKeySequence("Ctrl+F5"))
        self.run = QAction("Run", self)
        self.label = QLabel("Select current project")
        self.projectComboBox = ProjectComboBox(self.configurationManager)
        self.projectComboBox.setMinimumWidth(150)
        self.run.setShortcut(QKeySequence("F5"))
        self.addAction(self.compile)
        self.addAction(self.debug)
        self.addAction(self.run)
        self.addSeparator()
        self.addWidget(self.label)
        self.addWidget(self.projectComboBox)

    def updateComboBox(self):
        self.projectComboBox.clear()
        if self.configurationManager.allProjects:
            for project in self.configurationManager.allProjects:
                self.projectComboBox.addItem(project.proxy.path, project)

    def getCurrentProject(self):
        return self.projectComboBox.currentText()