from PySide2.QtWidgets import QStatusBar, QLabel, QComboBox, QWidget


class StatusBar(QStatusBar):
    
    def __init__(self):
        super(StatusBar, self).__init__()
        self.setStyleSheet("""
                        background-color: #007ACC;
                        color: white;
                        font-size: 14px;
                        """)
        self.label = QLabel("Current syntax:")
        self.label2 = QLabel("Set tab width:")
        self.comboBox = QComboBox()
        self.comboBox.addItem("Assembly")
        self.comboBox.addItem("C")
        self.comboBox.setEnabled(False)
        self.tabWidthComboBox = QComboBox()
        self.tabWidthComboBox.addItem("2")
        self.tabWidthComboBox.addItem("4")
        self.tabWidthComboBox.addItem("8")
        self.tabWidthComboBox.setCurrentText('4')
        self.addWidget(QWidget(), 6)
        self.addWidget(self.label, 1)
        self.addWidget(self.comboBox, 1)
        self.addWidget(self.label2, 1)
        self.addWidget(self.tabWidthComboBox, 1)
        self.setMaximumHeight(25)