from PySide2.QtGui import QSyntaxHighlighter
from PySide2.QtCore import QRegExp
from src.util.Formater import Formater


class CSyntax(QSyntaxHighlighter):

    keywords = ['long', 'unsigned', 'short', 'int', 'double', 'float', 'char', 'struct', 'typedef', 'for', 'while', 'union', 'return', 'if', 'else', 'break', 'continue', 'const', 'void']
    functions = ['printf', 'scanf', 'malloc', 'calloc', 'memset', 'sizeof', 'free',
                 'getc', 'gets', 'getchar', 'puts', 'putchar', 'clearerr', 'fopen', 'fclose', 'getw',
                 'putw', 'fgetc', 'putc', 'fputc', 'fgets', 'fputs', 'feof', 'fprintf', 'fscanf',
                 'fgetchar', 'fputchar', 'fseek', 'SEEK_SET', 'SEEK_CUR', 'SEEK_END', 'ftell', 'rewind',
                 'sprintf', 'sscanf', 'remove', 'fflush', 'realloc', 'abs', 'div', 'abort', 'exit', 'system',
                 'atoi', 'atol', 'atof', 'strtod', 'strtol', 'getenv', 'setenv', 'putenv', 'perror', 'rand', 'delay']

    def __init__(self, dokument):
        super(CSyntax, self).__init__(dokument)
        self.rules = []
        self.formater = Formater()
        self.rules += [(r'\b%s\b' % w, 0, self.formater.stilovi['keyword']) for w in CSyntax.keywords]
        self.rules += [(r'\b%s\b' % w, 0, self.formater.stilovi['declarations']) for w in CSyntax.functions]
        self.rules += [(r'//[^\n]*', 0, self.formater.stilovi['comment'])]
        self.rules += [(r'#[^\n]*', 0, self.formater.stilovi['string'])]
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
        self.setCurrentBlockState(0)
