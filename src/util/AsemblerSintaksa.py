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

from PySide2.QtGui import QSyntaxHighlighter
from PySide2.QtCore import QRegExp
from src.util.Formater import Formater


class AsemblerSintaksa(QSyntaxHighlighter):
    keywords = ['add', 'addl', 'addw', 'addb', 'sub', 'subl', 'subw', 'subb', 'and', 'andl', 'andw', 'andb', 'or', 'orl', 'orw', 'orb',
                'xor', 'xorl', 'xorw', 'xorb', 'shl', 'shll', 'shlw', 'shlb', 'shr', 'shrl', 'shrw', 'shrb', 'sar', 'sarl', 'sarw', 'sarb',
                'jne', 'je', 'jl', 'jg', 'ja', 'jb', 'test', 'testl', 'testw', 'testb', 'lea', 'leal', 'leaw', 'leab', 'int',
                'call', 'clc', 'cld', 'cmp', 'cmpl', 'cmpw', 'cmpb', 'dec', 'decl', 'decw', 'decb', 'inc', 'incl', 'incw', 'incb',
                'div', 'divl', 'divw', 'divb', 'mul', 'mull', 'mulw', 'mulb', 'idiv', 'idivl', 'idivw', 'idivb',
                'imul', 'imull', 'imulw', 'imulb', 'jae', 'jbe', 'jnae', 'jnbe', 'jge', 'jle', 'jng', 'jnl',
                'jna', 'jnb', 'jnge', 'jnle', 'jc', 'jnc', 'jz', 'jnz', 'jo', 'jno', 'js', 'jns', 'jcxz', 'jecxz',
                'lods', 'lodsl', 'lodsw', 'lodsb', 'loop', 'loopw', 'loopl', 'mov', 'movl', 'movb', 'movw',
                'neg', 'negl', 'negw', 'negb', 'nop', 'not', 'notl', 'notw', 'notb', 'pop', 'popl', 'push', 'pushl',
                'rcl', 'rcll', 'rclw', 'rclb', 'rcr', 'rcrl', 'rcrw', 'rcrb', 'ret', 'rol', 'roll', 'rolw', 'rolb',
                'std','stc', 'stos', 'xchg', 'xchgl', 'xchgw', 'xchgb', 'jmp', 'adc', 'adcl', 'adcw', 'adcb', 'sbbl', 'sbb', 'sbbw', 'sbbb']
    registers = ['%eax', '%ebx', '%ecx', '%edx', '%ax', '%al', '%ah', '%bx', '%bl', '%bh', '%cx', '%cl', '%ch', '%dx', '%dl', '%dh', '%esi', '%edi', '%esp', '%ebp']
    declarations = ['section', 'data', 'text', 'marco', 'ascii', 'globl', 'long', 'byte', 'quad', 'fill']

    def __init__(self, dokument):
        super(AsemblerSintaksa, self).__init__(dokument)
        self.rules = []
        self.formater = Formater()
        self.rules += [(r'\b%s\b' % w, 0, self.formater.stilovi['keyword']) for w in AsemblerSintaksa.keywords]
        self.rules += [(r'%s' % r, 0, self.formater.stilovi['register']) for r in AsemblerSintaksa.registers]
        self.rules += [(r'#[^\n]*', 0, self.formater.stilovi['comment'])]
        self.rules += [(r'\$[0-9]+\b', 0, self.formater.stilovi['literals'])]
        self.rules += [(r'\$0b[0-1]+\b', 0, self.formater.stilovi['literals'])]
        self.rules += [(r'\$0x[0-9a-fA-F]+\b', 0, self.formater.stilovi['literals'])]
        self.rules += [(r'\$[a-zA-Z_0-9]+\b', 0, self.formater.stilovi['literals'])]
        self.rules += [(r"\$\'[^']*\'", 0, self.formater.stilovi['literals'])]
        self.rules += [(r'\.%s\b' % d, 0, self.formater.stilovi['declarations']) for d in AsemblerSintaksa.declarations]
        self.rules += [(r'^(?!#).*[a-zA-Z0-9\_\-]+\:\s*', 0, self.formater.stilovi['label'])]
        self.rules += [(r"\".*\"", 0, self.formater.stilovi['string'])]
        self.rules += [(r"\'.?\'", 0, self.formater.stilovi['string'])]
        self.rules = [(QRegExp(pat), index, fmt) for (pat, index, fmt) in self.rules]

    def highlightBlock(self, text):
        for pattern, n, format in self.rules:
            exp = QRegExp(pattern)
            index = exp.indexIn(text)
            while index >= 0:
                length = exp.matchedLength()
                self.setFormat(index, length, format)
                index = exp.indexIn(text, index+length)
        # self.setCurrentBlockState(0)
