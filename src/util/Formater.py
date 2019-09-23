from PySide2.QtGui import QColor, QTextCharFormat, QFont


class Formater(object):

    def __init__(self):
        self.stilovi = {
            'keyword': self._formatiraj(65,111,145),
            'operator': self._formatiraj(122, 250, 226),
            'literals': self._formatiraj(149, 93, 193),
            'comment': self._formatiraj(58,100,52),
            'comment_c': self._formatiraj(58, 100, 52),
            'register': self._formatiraj(55,127,115),
            'declarations': self._formatiraj(255, 195, 0),
            'label': self._formatiraj(239, 241, 90),
            'string': self._formatiraj(140,108,58),
            'string_c': self._formatiraj(140, 108, 58)
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
