from PySide2.QtGui import QSyntaxHighlighter, QTextCharFormat
from PySide2.QtCore import QRegExp, QRegularExpressionMatch, QRegularExpression, Qt
from src.util.Formater import Formater
import re


class CSyntax(QSyntaxHighlighter):
    keywords_c = ['long', 'unsigned', 'short', 'int', 'double', 'float', 'char', 'struct', 'typedef', 'for', 'while',
                'union', 'return', 'if', 'else', 'break', 'continue', 'const', 'void', 'switch', 'case', 'default']
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
        # self.rules += [(r'(\/\*[^(\*\/)]*\*\/)', 0, self.formater.stilovi['comment'])]
        self.rules += [(r'\b%s\b' % w, self.formater.stilovi['keyword']) for w in CSyntax.keywords_c]
        # self.rules += [(r'\b%s\b' % w, 0, self.formater.stilovi['declarations']) for w in CSyntax.functions]
        self.rules += [(QRegExp(r'\b(?!(?:if|switch|while|void|for)[\s*|(])\b[A-Za-z0-9\_]+\s*(?=\([^\)]*\)\s*)'),
                        self.formater.stilovi['declarations'])]
        self.rules += [(QRegExp(r'//[^\n]*'), self.formater.stilovi['comment_c'])]
        self.rules += [(QRegExp(r'#[^\n]*'), self.formater.stilovi['string_c'])]
        self.rules += [(QRegExp(r"\".*\""), self.formater.stilovi['string'])]
        self.rules += [(QRegExp(r"\'.?\'"), self.formater.stilovi['string'])]
        # self.multiline_comment_start = r'/\*.*'
        # self.multiline_comment_end = r'[^\*/]*\*/'
        # self.multiline_comment_start = r'/\\*'
        # self.multiline_comment_end = r'\\*/'
        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(Qt.red)
        self.commentStartExpression = QRegExp("/\\*")
        self.commentEndExpression = QRegExp("\\*/")

        # self.rules = [(QRegExp(pat), index, fmt) for (pat, index, fmt) in self.rules]

    def highlightBlock(self, text):
        # for pattern, n, format in self.rules:
        #     exp = QRegExp(pattern)
        #     index = exp.indexIn(text)
        #     while index >= 0:
        #         length = exp.matchedLength()
        #         # length = pattern.cap(n).lenght()
        #         self.setFormat(index, length, format)
        #         index = exp.indexIn(text, index + length)
        for pattern, format in self.rules:
            exp = QRegExp(pattern)
            index = exp.indexIn(text)
            while index >= 0:
                length = exp.matchedLength()
                # length = pattern.cap(n).lenght()
                self.setFormat(index, length, format)
                index = exp.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        start_index = 0
        if self.previousBlockState() != 1:
            # start_index = exp.indexIn(text)
            start_index = self.commentStartExpression.indexIn(text)
        while start_index >= 0:
            # rex = QRegularExpression(self.multiline_comment_end)
            # match = rex.match(text, start_index)
            # end_index = match.capturedStart()
            end_index = self.commentEndExpression.indexIn(text, start_index)
            if end_index == -1:
                self.setCurrentBlockState(1)
                comment_length = len(text) - start_index
            else:
                # comment_length = end_index - start_index + match.capturedLength()
                comment_length = end_index - start_index + self.commentEndExpression.matchedLength()
            self.setFormat(start_index, comment_length, self.formater.stilovi['comment'])
            start_index = self.commentStartExpression.indexIn(text, start_index + comment_length)
