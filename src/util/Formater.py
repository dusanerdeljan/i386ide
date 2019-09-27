"""
    This file is part of i386ide.
    i386ide is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

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
