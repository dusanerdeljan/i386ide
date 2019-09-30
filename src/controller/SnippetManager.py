"""
    i386ide is lightweight IDE for i386 assembly and C programming language.
    Copyright (C) 2019  Dušan Erdeljan, Marko Njegomir

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import os
import pickle
import getpass


class SnippetManager(object):

    USER = getpass.getuser()
    SAVE_FOLDER = os.path.join("/", "home", USER, ".i386ide")
    SAVE_PATH = os.path.join(SAVE_FOLDER, "snippets.conf")

    DEFAULT_SNIPPETS = {
    '.st': ".section .text\n",
    '.sd': ".section .data\n",
    '.gm': ".globl main\n",
    '.gs': ".globl _start\n",
    '.endl': """kraj:
    movl $1, %eax
    movl $0, %ebx
    int $0x80\n""",
    ".sys": """movl A, %eax
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
    ret\n"""
    }

    def __init__(self):
        self.codeSnippets = {}
        for snippet in SnippetManager.DEFAULT_SNIPPETS:
            self.codeSnippets[snippet] = SnippetManager.DEFAULT_SNIPPETS[snippet]

    def __contains__(self, item):
        return item in self.codeSnippets

    def __getitem__(self, item):
        return self.codeSnippets[item]

    def updateSnippets(self, newSnippets: dict):
        self.codeSnippets.clear()
        for key in newSnippets:
            self.codeSnippets[key] = newSnippets[key]

    def getSnippetsAbbs(self):
        return self.codeSnippets.keys()

    def saveConfiguration(self):
        if not os.path.exists(SnippetManager.SAVE_FOLDER):
            os.mkdir(SnippetManager.SAVE_FOLDER)
        with open(self.SAVE_PATH, 'wb') as metadata:
            pickle.dump(self, metadata, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def loadSnippetConfiguration():
        try:
            with open(SnippetManager.SAVE_PATH, 'rb') as file:
                snippets = pickle.load(file)
            return snippets
        except:
            return SnippetManager()