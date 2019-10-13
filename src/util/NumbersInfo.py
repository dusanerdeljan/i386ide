"""
    i386ide is lightweight IDE for i386 assembly and C programming language.
    Copyright (C) 2019  Dušan Erdeljan, Marko Njegomir
    
    This file is part of i386ide.

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

import re

class NumbersInfo(object):
    REX = {
        'dec' : re.compile(r'[0-9]+\b'),
        'bin' : re.compile(r'0b[0-1]+\b'),
        'hex' : re.compile(r'0x[0-9a-fA-F]+\b')
    }
    @staticmethod
    def checkIfNumber(word):

        if re.match(NumbersInfo.REX['dec'], word) or re.match(NumbersInfo.REX['bin'], word) or re.match(NumbersInfo.REX['hex'], word):
            return True
        return


    @staticmethod
    def showConvertedNumbers(word):
        decimal = ""
        binary = ""
        hexadecimal = ""
        if re.match(NumbersInfo.REX['dec'], word):
            decimal = word
            binary = str(bin(int(word)))
            hexadecimal = str(hex(int(word)))
        elif re.match(NumbersInfo.REX['bin'], word):
            decimal = str(int(word, 2))
            binary = word
            hexadecimal = str(hex(int(decimal)))
        elif re.match(NumbersInfo.REX['hex'], word):
            decimal = str(int(word, 16))
            binary = str(bin(int(decimal)))
            hexadecimal = word

        return "DEC: {}\nBIN: {}\nHEX: {}".format(decimal,binary,hexadecimal)