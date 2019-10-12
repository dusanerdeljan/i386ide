"""
    i386ide is lightweight IDE for i386 assembly and C programming language.
    Copyright (C) 2019  Dušan Erdeljan, Marko Njegomir

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

from PySide2.QtWidgets import QTabWidget, QWidget, QMessageBox, QVBoxLayout
from PySide2.QtCore import Signal
from src.view.CodeEditor import CodeEditor
from src.view.FindDialog import FindDialog
from src.model.FileNode import FileProxy
from src.controller.PathManager import PathManager
from src.controller.SnippetManager import SnippetManager
from src.controller.TooltipManager import TooltipManager
import os
import main

class TabWidget(QWidget):

    def __init__(self, fileProxy: FileProxy, snippetManager: SnippetManager, tooltipManager: TooltipManager):
        super(TabWidget, self).__init__()
        self.editor = CodeEditor(fileProxy, snippetManager, tooltipManager)
        self.find = FindDialog(self.editor)
        self.find.setVisible(False)
        self.find.escapePressed.connect(lambda: self.find.hide())
        self.editor.escapePressed.connect(lambda: self.find.hide())
        self.vbox = QVBoxLayout()
        self.vbox.setSpacing(0)
        self.vbox.addWidget(self.find)
        self.vbox.addWidget(self.editor)
        self.setLayout(self.vbox)

class EditorTab(QWidget):

    fileChanged = Signal(FileProxy)
    tabSwitchRequested = Signal()
    
    def __init__(self, fileProxy: FileProxy, snippetManager: SnippetManager, tooltipManager: TooltipManager):
        super(EditorTab, self).__init__()
        self.widget = TabWidget(fileProxy, snippetManager, tooltipManager)
        fileProxy.hasUnsavedChanges = False
        self.tabName = "{}/{}".format(fileProxy.parent.path, fileProxy.path)
        self.widget.editor.fileChanged.connect(lambda fileProxy: self.fileChanged.emit(fileProxy))
        self.widget.editor.tabSwitchRequested.connect(lambda: self.tabSwitchRequested.emit())

class EditorTabWidget(QTabWidget):

    tabSwitchRequested = Signal()
    
    def __init__(self, snippetManager: SnippetManager, tooltipManager: TooltipManager):
        super(EditorTabWidget, self).__init__()
        self.tabBar().setStyleSheet("QTabBar:tab {background-color: #2D2D30; color: white; height: 25px;}"
                                    " QTabBar:tab:selected {background-color: #007ACC;}")
        self.tabBar().setMaximumHeight(30)
        self.projectTabs = dict()
        self.tabs = []
        self.snippetManager = snippetManager
        self.tooltipManager = tooltipManager
        self.closedTabsStyleSheet = "background-color: #2D2D30; background-image: url(\"{}\"); background-repeat: no-repeat; background-position: center; color: white;".format(main.resource_path("resources/tab_background.png"))
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
        tab = EditorTab(fileProxy, self.snippetManager, self.tooltipManager)
        tab.fileChanged.connect(self.fileChanged)
        tab.tabSwitchRequested.connect(lambda: self.tabSwitchRequested.emit())
        self.projectTabs[key] = tab
        self.addTab(tab.widget, tab.tabName)
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