from PySide2.QtWidgets import QTextEdit, QWidget, QPlainTextEdit
from PySide2.QtCore import QSize, Qt, QRect
from PySide2.QtGui import QColor, QPainter, QTextFormat, QFont
from src.util.AsemblerSintaksa import AsemblerSintaksa
from src.view.AutocompleteWidget import AutocompleteWidget
from src.datastrctures.Trie import Trie
from src.model.FileNode import FileProxy


class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):

    def __init__(self):
        super(CodeEditor, self).__init__()

        # podaci vezani za asmeblerski fajl
        self.file: FileProxy = None

        # snipeti
        self.codeSnipets = {
            '.st': ".section .text\n",
            '.sd': ".section .data\n",
            '.gm': ".globl main\n",
            '.gs': ".globl _start\n",
            '.endl': """kraj:
    movl $1, %eax
    movl $0, %ebx
    int $0x80\n""",
            ".sys": """    movl A, %eax
    movl B, %ebx
    movl C, %ecx
    movl D, %edx
    int $0x80\n""",
            '.full': """# autor Imenko Prezimenic SW123456
# Potprogram radi...
.section .data
# sekcija za promenljive
.section .text
.globl main
main:
    # polazna tacka programa
kraj:
    movl $1, %eax
    movl $0, %ebx
    int $0x80\n""",
            '.stackfull': """# autor Imenko Prezimenic SW123456
# Potprogram radi...
.section .data
# sekcija za promenljive
.section .text
.globl ime_potprograma
ime_potprograma:
    pushl %ebp
    movl %esp, %ebp 
    # polazna tacka programa
kraj:
    movl %ebp, %esp
    popl %ebp
    ret\n""",
        }

        self.tabSize = 4
        self.autocompleteWidgetOpen = False
        self.queryWord = ""
        self.widget = None
        self.instructionsTrie = Trie()
        self.insertInstructionsInTrie()

        # self.setTabStopWidth(self.fontMetrics().width(" ") * self.tabSize)
        self.setStyleSheet(
            "font-size: 14px; background-color: #44423E; color: white; font-family: comic-sans; border: none;")
        self.sintaksa = AsemblerSintaksa(self.document())
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        #self.textChanged.connect(self.setUnsavedChanges)

    def setUnsavedChanges(self):
        if self.file:
            self.file.hasUnsavedChanges = True
            self.file.text = self.toPlainText()

    def insertInstructionsInTrie(self):
        for keyword in AsemblerSintaksa.keywords:
            self.instructionsTrie.insert(keyword)
        for register in AsemblerSintaksa.registers:
            self.instructionsTrie.insert(register)
        for declaration in AsemblerSintaksa.declarations:
            self.instructionsTrie.insert(".{}".format(declaration))

    def mousePressEvent(self, e):
        if self.autocompleteWidgetOpen:
            self.closeAutoSuggestionWidget()
            self.queryWord = ""
        else:
            super(CodeEditor, self).mousePressEvent(e)

    def keyPressEvent(self, e):
        startLength = len(self.toPlainText())
        enterPressed = False
        numSpaces = 0
        if e.key() == Qt.Key_Return:
            if self.autocompleteWidgetOpen:
                self.closeAutoSuggestionWidget()
            self.queryWord = ""
            enterPressed = True
            # napravi da se prenosi spacing sa pocetka prethodne linije
            currentLine = self.textCursor().block().text()
            for i in currentLine:
                if i == '\t':
                    numSpaces += self.tabSize
                elif i == ' ':
                    numSpaces += 1
                else:
                    break
        elif e.key() == Qt.Key_Colon or e.key() == Qt.Key_Equal:
            if isinstance(self.sintaksa, AsemblerSintaksa):
                self.insertLabelInTrie()
        elif e.key() == Qt.Key_Tab:
            self.queryWord = ""
            self.insertPlainText(self.tabSize * " ")
            return
        elif e.key() == Qt.Key_Down and self.autocompleteWidgetOpen:
            self.widget.widget.setFocus()
            try:
                self.widget.widget.setCurrentRow(0)
            except Exception:
                pass
            return
        elif e.key() == Qt.Key_Backspace:
            self.queryWord = self.queryWord[:-1]
            if self.autocompleteWidgetOpen:
                if self.queryWord.strip() == "":
                    self.closeAutoSuggestionWidget()
        elif e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_Space:
            if self.autocompleteWidgetOpen:
                return
            self.loadQueryWord()
            if isinstance(self.sintaksa, AsemblerSintaksa):
                if self.queryWord in self.codeSnipets:
                    while not self.textCursor().atBlockStart():
                        self.textCursor().deletePreviousChar()
                    self.insertPlainText(self.codeSnipets[self.queryWord])
                    # self.moveCursor(QTextCursor.End)
                    self.queryWord = ""
                    return
                cursorPosition = self.cursorRect()
                self.showAutocompleteWidget(cursorPosition)
        elif e.key() == Qt.Key_Space:
            self.queryWord = ""
        elif e.key() == Qt.Key_Left or e.key() == Qt.Key_Right or e.key() == Qt.Key_Up:
            if self.autocompleteWidgetOpen:
                self.closeAutoSuggestionWidget()
        elif e.key() == Qt.Key_Escape:
            if self.autocompleteWidgetOpen:
                self.closeAutoSuggestionWidget()
        else:
            self.queryWord += e.text()
        super(CodeEditor, self).keyPressEvent(e)
        if self.autocompleteWidgetOpen:
            if isinstance(self.sintaksa, AsemblerSintaksa):
                self.updateSuggestions()
        if enterPressed and numSpaces:
            self.insertPlainText(numSpaces * " ")
        endLength = len(self.toPlainText())
        if (endLength - startLength) != 0:
            self.setUnsavedChanges()

    def insertLabelInTrie(self):
        currentLineCursorIndex = self.textCursor().positionInBlock()
        currentLine = self.textCursor().block().text()
        foundChar = False
        label = ""
        for i in range(currentLineCursorIndex-1, -1, -1):
            if currentLine[i] == " ":
                if foundChar:
                    break
                else:
                    continue
            label = currentLine[i] + label
            foundChar = True
        if not label.strip() == "":
            self.instructionsTrie.insert(label)


    def updateSuggestions(self):
        suggestions = []
        try:
            suggestions = self.instructionsTrie.get_autocompletes(self.queryWord)
        except Exception:
            suggestions = []
        self.widget.updateSuggestionList(suggestions)

    def loadQueryWord(self):
        currentLineCursorIndex = self.textCursor().positionInBlock()
        self.queryWord = ""
        if currentLineCursorIndex:
            currentLine = self.textCursor().block().text()
            for i in range(currentLineCursorIndex - 1, -1, -1):
                if currentLine[i] == " ":
                    break
                self.queryWord = currentLine[i] + self.queryWord

    def showAutocompleteWidget(self, position):
        self.autocompleteWidgetOpen = True
        currentLineCursorIndex = self.textCursor().positionInBlock()
        self.queryWord = ""
        if currentLineCursorIndex:
            currentLine = self.textCursor().block().text()
            for i in range(currentLineCursorIndex - 1, -1, -1):
                if currentLine[i] == " ":
                    break
                self.queryWord = currentLine[i] + self.queryWord
        try:
            suggestions = self.instructionsTrie.get_autocompletes(self.queryWord)
        except Exception:
            suggestions = None
        self.widget = AutocompleteWidget(suggestions)
        self.widget.setParent(self)
        self.widget.setGeometry(position.x() + 5, position.y() + 16, 200, 200)
        self.widget.setSize()
        self.widget.exec_()
        self.autocompleteWidgetOpen = False
        self.setFocus()
        self.insertAutocompletedKeyword()

    def insertAutocompletedKeyword(self):
        autocompletion = None
        if self.widget:
            autocompletion = self.widget.result
        if autocompletion:
            self.insertPlainText(str(autocompletion)[len(self.queryWord)::])
        self.queryWord = ""
        self.widget = None

    def closeAutoSuggestionWidget(self):
        self.autocompleteWidgetOpen = False
        self.widget.close()
        self.widget = None

    def getOpenFileName(self):
        if self.file:
            return self.file.path

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor.fromRgb(103, 104, 103, 127)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), QColor.fromRgb(103, 104, 103, 255))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(QColor.fromRgb(196, 198, 196, 255))
                painter.setFont(QFont("Sans serif", 8, QFont.Bold))
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignJustify, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1
