from PySide2.QtWidgets import QDockWidget, QLineEdit, QTextEdit, QCompleter
from PySide2.QtCore import Qt


class HelpWidget(QDockWidget):

    INFO = {
        'adc': """<b>adc</b> <em>src</em>, <em>dst</em><br><p>Sabira izvorni i odredisni operand i rezultat smesta u odredisni operand. Prilikom sabiranja zateceni prenos se uzima u obzir</p>"""
    }

    def __init__(self):
        super(HelpWidget, self).__init__()
        # TODO: ovo treba da bude kao neki widget u koji moze da se unese instrukcija ili registar ili direktiva
        # TODO: pa mu se onda ispise neki uredjeni HTML kao onaj tekst iz praktikuma sta ta kljucna rec znaci
        # TODO: mozda da se ispisu i neki odabrani algoritmi npr. sabiranje u dvostrukoj preciznosti sa ilustracijama
        # TODO: ili iteriranje kroz niz
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setMinimumWidth(200)
        self.setStyleSheet("background-color: #2D2D30; color: white;")
        self.searchLabel = QLineEdit()
        self.searchLabel.setPlaceholderText("Search for an instruction...")
        self.completer = QCompleter(list(HelpWidget.INFO.keys()), self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.popup().setStyleSheet("background-color: #2D2D30; color: white")
        self.searchLabel.setCompleter(self.completer)
        self.searchLabel.setStyleSheet("margin-bottom: 10px; margin-top: 10px;")
        self.setTitleBarWidget(self.searchLabel)
        self.setFeatures(QDockWidget.DockWidgetMovable)
        self.resultBox = QTextEdit()
        self.resultBox.setReadOnly(True)
        self.setWidget(self.resultBox)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and self.searchLabel.hasFocus():
            seachWord = self.searchLabel.text().strip()
            if seachWord in HelpWidget.INFO:
                self.resultBox.setHtml(HelpWidget.INFO[seachWord])
        super(HelpWidget, self).keyPressEvent(event)
