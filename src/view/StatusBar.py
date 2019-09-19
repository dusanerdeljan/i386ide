from PySide2.QtWidgets import QStatusBar, QLabel, QComboBox, QWidget


class StatusBar(QStatusBar):
    
    def __init__(self):
        super(StatusBar, self).__init__()
        self.setStyleSheet("""
                        background-color: #007ACC;
                        color: white;
                        font-size: 14px;
                        """)
        self.label = QLabel("Choose a syntax:")
        self.comboBox = QComboBox()
        self.comboBox.addItem("Assembly")
        self.comboBox.addItem("C")
        self.addWidget(QWidget(), 2)
        self.addWidget(self.label, 1)
        self.addWidget(self.comboBox, 1)
        self.setMaximumHeight(25)