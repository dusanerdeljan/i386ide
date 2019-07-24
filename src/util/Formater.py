from PySide2.QtGui import QColor, QTextCharFormat, QFont


class Formater(object):

    def __init__(self):
        self.stilovi = {
            'keyword': self._formatiraj(214, 137, 16, 'bold'),
            'operator': self._formatiraj(122, 250, 226, 'bold'),
            'literals': self._formatiraj(149, 93, 193, 'bold'),
            'comment': self._formatiraj(40, 128, 42),
            'register': self._formatiraj(122, 250, 226),
            'declarations': self._formatiraj(255, 195, 0, 'bold'),
            'label': self._formatiraj(239, 241, 90)
        }

    def _formatiraj(self, r, g, b, stil=''):
        #_boja = QColor()
        _boja = QColor.fromRgb(r, g, b, 255)
        _format = QTextCharFormat()
        _format.setForeground(_boja)
        if 'bold' in stil:
            _format.setFontWeight(QFont.Bold)
        if 'italic' in stil:
            _format.setFontItalic(True)
        return _format
