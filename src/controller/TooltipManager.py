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

import pickle
import os
import getpass

class TooltipManager(object):

    USER = getpass.getuser()
    SAVE_FOLDER = os.path.join("/", "home", USER, ".i386ide")
    SAVE_PATH = os.path.join(SAVE_FOLDER, "tooltips.conf")

    DEFAULT_VALUE_INSTUCTIONS = True
    DEFAULT_VALUE_NUMBERS = True

    def __init__(self):
        self.showInstructionTooltips = TooltipManager.DEFAULT_VALUE_INSTUCTIONS
        self.showNumberConversion = TooltipManager.DEFAULT_VALUE_NUMBERS

    def saveConfiguration(self):
        if not os.path.exists(TooltipManager.SAVE_FOLDER):
            os.mkdir(TooltipManager.SAVE_FOLDER)
        with open(self.SAVE_PATH, 'wb') as metadata:
            pickle.dump(self, metadata, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def loadTooltipConfiguration():
        try:
            with open(TooltipManager.SAVE_PATH, 'rb') as file:
                tooltips = pickle.load(file)
            return tooltips
        except:
            return TooltipManager()