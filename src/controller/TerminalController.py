from PySide2.QtCore import QObject, Signal
import _thread
import subprocess
import shlex
import os


class TerminalController(QObject):

    externalCommand = Signal(str)

    def commandEnteredHandler(self, command: str):
        command = command.strip()
        if command.startswith("./") or command.startswith("/"):
            try :
                _thread.start_new_thread(self.runShell, (command, not command.startswith("ddd"), ))
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
        command = "gnome-terminal" + " -e 'bash -c \"{}; sleep 1\"'".format(command)
        # splitedCommand = command.split(" ") if command.startswith("ddd") else shlex.split(command)
        os.system(command)
