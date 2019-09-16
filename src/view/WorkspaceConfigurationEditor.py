from PySide2.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox, QFileDialog, QMessageBox
from PySide2.QtCore import Qt
from src.controller.WorkspaceConfiguration import WorkspaceConfiguration
import re
import os


class WorkspaceConfigurationEditor(QDialog):

    def __init__(self, workpsaceConfiguration, mainApplicatoin, switch=False):
        super(WorkspaceConfigurationEditor, self).__init__()
        self.workspaceConfiguration: WorkspaceConfiguration = workpsaceConfiguration
        self.mainApplication = mainApplicatoin
        self.switch = switch
        self.workspaceDirectory = None
        self.setWindowTitle("Choose a workspace directory")
        self.setStyleSheet("background-color: #44423E; color: white;")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setFixedSize(500, 150)
        self.comboBox = QComboBox()
        self.comboBox.addItems(list(self.workspaceConfiguration.getWorkspaces()))
        if self.workspaceConfiguration.defaultWorkspace:
            self.comboBox.setCurrentText(self.workspaceConfiguration.getDefaultWorkspace())
        self.btnOpen = QPushButton("Open workspace")
        self.cbDefault = QCheckBox("Set as default workspace")
        self.btnBrowse = QPushButton("Browse...")
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.comboBox, 4)
        self.hbox2.addWidget(self.btnBrowse, 1)
        self.vbox.addLayout(self.hbox2)
        self.hbox.addWidget(self.cbDefault)
        self.hbox.addWidget(self.btnOpen)
        self.vbox.addSpacing(20)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)
        self.btnOpen.clicked.connect(self.loadWorkpace)
        self.btnBrowse.clicked.connect(self.browseWorkspace)
        self.btnOpen.setFocus()
        if len(self.workspaceConfiguration.getWorkspaces()) == 0:
            self.btnOpen.setEnabled(False)

    def browseWorkspace(self):
        directory = QFileDialog.getExistingDirectory()
        if directory == "":
            return
        wsname = directory[directory.rindex(os.path.sep) + 1:]
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if ' ' in directory or regex.search(wsname):
            msg = QMessageBox()
            msg.setModal(True)
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Workspace path/name cannot contain whitespace special characters.")
            msg.setWindowTitle("Workspace creation error")
            msg.exec_()
            return
        self.workspaceConfiguration.addWorkspace(directory)
        self.comboBox.addItem(directory)
        self.comboBox.setCurrentText(directory)
        if not self.btnOpen.isEnabled():
            self.btnOpen.setEnabled(True)

    def loadWorkpace(self):
        if self.cbDefault.isChecked():
            self.workspaceConfiguration.setDefaultWorkspace(self.comboBox.currentText())
        if not self.switch:
            self.mainApplication.openWorkspaceAction(self.comboBox.currentText())
        else:
            self.workspaceDirectory = self.comboBox.currentText()
        self.accept()

    def closeEvent(self, arg__1):
        self.reject()
