"""
    i386ide is lightweight IDE for i386 assembly and C programming language.
    Copyright (C) 2019  Dušan Erdeljan, Marko Njegomir
    
    This file is part of i386ide.

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

from PySide2.QtWidgets import QListWidget, QListWidgetItem, QDialog, QVBoxLayout, QLabel
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from src.model.CFileNode import CFileProxy
from src.model.AssemblyFileNode import AssemblyFileProxy
import main


class TabSwithcerListItem(QListWidgetItem):
    
    def __init__(self, fileProxy):
        super(TabSwithcerListItem, self).__init__()
        if isinstance(fileProxy, AssemblyFileProxy):
            self.setIcon(QIcon(main.resource_path("resources/s.png")))
        elif isinstance(fileProxy, CFileProxy):
            self.setIcon(QIcon(main.resource_path("resources/c.png")))
        self.setText("{}/{}".format(fileProxy.parent.path, fileProxy.path))


class TabSwitcher(QDialog):
    
    def __init__(self, tabs):
        super(TabSwitcher, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.latestTabIndex = -1
        self.setStyleSheet("background-color: #232323; color: white;")
        self.tabs = tabs
        self.tabList = QListWidget()
        self.vbox = QVBoxLayout()
        self.pathLabel = QLabel()
        self.pathLabel.setStyleSheet("font-size: 10px; color: grey;")
        self.vbox.addWidget(QLabel("<center>Tab switcher</center>"), 1)
        self.vbox.addWidget(self.tabList, 10)
        self.vbox.addWidget(self.pathLabel, 1)
        self.setLayout(self.vbox)

    def showSwitcher(self):
        self.latestTabIndex = self.tabs.currentIndex()
        self.updateTabList()
        self.updateTabListCurrentItem(self.latestTabIndex)
        self.setFixedSize(self.sizeHint())
        self.setFixedWidth(500)
        self.show()

    def updateTabListCurrentItem(self, index):
        self.tabList.setCurrentRow(index)
        fileProxy = self.tabs.tabs[index]
        self.pathLabel.setText(fileProxy.getFilePath())

    def updateTabList(self):
        self.tabList.clear()
        for proxy in self.tabs.tabs:
            self.tabList.addItem(TabSwithcerListItem(proxy))

    def hideSwitcher(self):
        if self.latestTabIndex != -1:
            self.tabs.setCurrentIndex(self.latestTabIndex)
        self.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab or event.key() == Qt.Key_Down:
            self.latestTabIndex = (self.latestTabIndex + 1) % self.tabs.count()
        elif event.key() == Qt.Key_Up or event.key() == Qt.Key_Backtab:
            self.latestTabIndex -= 1
            if self.latestTabIndex < 0:
                self.latestTabIndex = self.tabs.count() - 1
        self.updateTabListCurrentItem(self.latestTabIndex)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Backtab:
            return
        if event.modifiers() != Qt.ControlModifier:
            if self.latestTabIndex != -1:
                self.tabs.setCurrentIndex(self.latestTabIndex)
            self.latestTabIndex = -1
            self.hideSwitcher()
        
    def focusOutEvent(self, event):
        super(TabSwitcher, self).focusOutEvent(event)
        self.hide()