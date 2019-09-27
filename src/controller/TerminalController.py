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

from PySide2.QtCore import QObject, Signal
import threading
import subprocess
import shlex
import os


class TerminalController(QObject):

    externalCommand = Signal(str)

    def commandEnteredHandler(self, command: str):
        command = command.strip()
        if command.startswith("./") or command.startswith("/"):
            try :
                thread = threading.Thread(target=self.runShell, args=[command, not command.startswith("ddd")])
                thread.start()
                # os.system(command)
                self.externalCommand.emit(command)
                return "ES" # external shell
            except Exception:
                return "UES"
        try:
            if command.startswith("cd") and len(command.split(" ")) >= 2:
                return self.executeCDCommand(command)
            proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            o, e = proc.communicate(timeout=10)
            code = proc.returncode
            return {
                'output': o.decode('utf-8'),
                'error': e.decode('utf-8'),
                'code': code
            }
        except subprocess.TimeoutExpired:
            return "TE" # timeout expired
        except Exception:
            return "UC" # unsupported command

    def executeCDCommand(self, command):
        destination = command.split("cd")[1].strip()
        os.chdir(destination)
        return  {
            'output': "",
            'error': "",
            'code': 0
        }


    def runShell(self, command: str, useShell):
        command = "x-terminal-emulator" + " -e 'bash -c \"{}; read -rsn1 -p \"Terminate...\"\"'".format(command)
        os.system(command)
