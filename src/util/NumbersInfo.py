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