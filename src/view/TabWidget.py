from PySide2.QtWidgets import QTabWidget, QWidget, QMessageBox
from PySide2.QtCore import Signal
from src.view.CodeEditor import CodeEditor
from src.model.FileNode import FileProxy
from src.controller.PathManager import PathManager
import os
import main

class EditorTab(QWidget):

    fileChanged = Signal(FileProxy)
    
    def __init__(self, fileProxy: FileProxy):
        super(EditorTab, self).__init__()
        self.editor = CodeEditor(fileProxy)
        #self.editor.setPlainText(fileProxy.text)
        fileProxy.hasUnsavedChanges = False
        self.tabName = "{}/{}".format(fileProxy.parent.path, fileProxy.path)
        self.editor.fileChanged.connect(lambda fileProxy: self.fileChanged.emit(fileProxy))

class EditorTabWidget(QTabWidget):
    
    def __init__(self):
        super(EditorTabWidget, self).__init__()
        self.tabBar().setStyleSheet("QTabBar:tab {background-color: #2D2D30; color: white; height: 25px;}"
                                    " QTabBar:tab:selected {background-color: #007ACC;}")
        self.tabBar().setMaximumHeight(30)
        self.projectTabs = dict()
        self.tabs = []
        self.closedTabsStyleSheet = "background-image: url(\"{}\"); background-repeat: no-repeat; background-position: center; color: white;".format(main.resource_path("resources/tab_background.png"))
        self.openTabsStyleSheet = "background-color: #2D2D30; color: white;"
        self.setStyleSheet(self.closedTabsStyleSheet)
        self.setTabsClosable(True)
        self.setMovable(False)
        self.tabCloseRequested.connect(self.closeTab)

    def addNewTab(self, fileProxy, update=True):
        key = "{}/{}".format(fileProxy.parent.path, fileProxy.path)
        if key in self.projectTabs:
            self.setCurrentIndex(self.tabs.index(fileProxy))
            return
        self.setStyleSheet(self.openTabsStyleSheet)
        self.update()
        tab = EditorTab(fileProxy)
        tab.fileChanged.connect(self.fileChanged)
        self.projectTabs[key] = tab
        self.addTab(tab.editor, tab.tabName)
        if update:
            self.tabs.append(fileProxy)
        self.setCurrentIndex(self.tabs.index(fileProxy))

    def fileChanged(self, fileProxy: FileProxy):
        key = "{}/{}".format(fileProxy.parent.path, fileProxy.path)
        if key in self.projectTabs:
            tabIndex = self.tabs.index(fileProxy)
            self.setTabText(tabIndex, key+"*")

    def removeChangeIdentificator(self, fileProxy: FileProxy):
        key = "{}/{}".format(fileProxy.parent.path, fileProxy.path)
        if key in self.projectTabs:
            tabIndex = self.tabs.index(fileProxy)
            self.setTabText(tabIndex, key)

    def getCurrentFileProxy(self):
        if self.tabs:
            return self.tabs[self.currentIndex()]

    def getCurrentTab(self):
        proxy = self.getCurrentFileProxy()
        if proxy:
            key = "{}/{}".format(proxy.parent.path, proxy.path)
            if key in self.projectTabs:
                return self.projectTabs[key]
        return None

    def closeAllTabs(self):
        for index in range(len(self.tabs)-1, -1, -1):
            if not self.closeTab(index):
                return False
        return True

    def closeTab(self, index, askToSave=True):
        proxy: FileProxy = self.tabs[index]
        key = "{}/{}".format(proxy.parent.path, proxy.path)
        if proxy.hasUnsavedChanges and askToSave:
            msg = QMessageBox()
            msg.setStyleSheet("background-color: #2D2D30; color: white;")
            msg.setParent(None)
            msg.setModal(True)
            msg.setWindowTitle("Close tab")
            msg.setText("The file {}/{} has been modified.".format(proxy.parent.path, proxy.path))
            msg.setInformativeText("Do you want to save changes?")
            msg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Save)
            retValue = msg.exec_()
            if retValue == QMessageBox.Save:
                proxy.saveFile()
            elif retValue == QMessageBox.Discard:
                pass
            else:
                return False
        self.tabs.pop(index)
        del self.projectTabs[key]
        self.removeTab(index)
        if len(self.tabs) == 0:
            self.setStyleSheet(self.closedTabsStyleSheet)
            self.update()
        return True