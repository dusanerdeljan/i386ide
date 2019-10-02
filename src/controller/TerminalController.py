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

from PySide2.QtCore import QObject, Signal
import threading
import subprocess
import shlex
import os

class TerminalController(QObject):
    def __init__(self):
        super().__init__()
        self.previous_directory = None
        self.tab_counter = 0
        self.previous_command = ""
        self.previous_results = []
    externalCommand = Signal(str)


    def showCommandAutocomplete(self, command):
        if command != self.previous_command:
            self.tab_counter = 0
        else:
            self.tab_counter += 1
        self.previous_command = command

        result = self.commandAutocompleteHandler(command)
        if not result:
            return [self.previous_command]

        if self.tab_counter > 1:  # double tab to list autocomplete suggestions
            html_results = "<table>"
            counter = 0
            for sug in self.previous_results:
                if counter == 0:
                    html_results += "<tr>"
                html_results += '<td align = "left">' + sug + "&nbsp;&nbsp;&nbsp;&nbsp;</td>"
                counter += 1
                if counter > 4:
                    html_results += "</tr>"
                    counter = 0
            html_results += "</table>"
            return [self.previous_command, html_results]

        if result[0] != "":
            self.tab_counter = 0
        else:
            self.tab_counter += 1
        return [self.previous_command + result[0]]

    def commandAutocompleteHandler(self, input: str):
        # also works. I left it in case i need it for compatibility
        # command = "compgen -o default " + command + '\t'
        # process = subprocess.run(command, universal_newlines=True, stdin=subprocess.PIPE, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash')
        # print(process.stdout)
        # print(process.stderr)

        # works
        arguments = shlex.split(input)

        if len(arguments) == 0:
            return
        expression = "" + arguments[-1].strip()

        if expression.startswith("/"):  # folders
            command = "compgen -d " + expression
        elif expression.startswith("./"):  # programs or folders if there are not programs
            command = "compgen -c " + expression
        elif len(arguments) == 1:  # command or folder if there are no commands
            command = "compgen -c -o default " + expression
        else:
            command = "compgen -o default " + expression

        process = subprocess.Popen('/bin/bash', universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate(command, timeout=10)
        results = out.split()
        self.previous_results = list(dict.fromkeys(results))
        results = set(self.previous_results)  # so there would not be duplicates, example: POST, test
        if len(results) == 0:
            return
        if len(results) == 1:
            autocompleted_word = results.pop()  # does autocomplete if its the only result
            if os.path.isdir(autocompleted_word):
                additional_sufix = "/"
            else:
                additional_sufix = " "
            autocomplete_sufix = autocompleted_word[len(expression):]
            return [autocomplete_sufix + additional_sufix]
        else:  # looking for the longest prefix
            number_of_hits = len(results)
            element = next(iter(results))
            expanded_word = expression
            i = len(expression)
            brojac = 0
            while i < len(element):
                for r in results:
                    if r.startswith(element[0:i+1]):
                        brojac += 1
                if brojac != number_of_hits:
                    break
                expanded_word += element[i]
                i += 1
                brojac = 0

            autocomplete_sufix = expanded_word[len(expression):]
            return [autocomplete_sufix, results]


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
            if " ".join(command.split()) == "cd -":
                return self.executeCDBackCommand(command)
            elif command.startswith("cd") and len(command.split(" ")) >= 2:
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
        self.previous_directory = os.getcwd()
        destination = command.split("cd")[1].strip()
        os.chdir(destination)
        return  {
            'output': "",
            'error': "",
            'code': 0
        }

    def executeCDBackCommand(self, command):
        current_dir = os.getcwd()
        os.chdir(self.previous_directory)
        if self.previous_directory:
           self.previous_directory = current_dir
        return  {
            'output': self.previous_directory + "\n",
            'error': "",
            'code': 0
        }

    def runShell(self, command: str, useShell):
        command = "x-terminal-emulator" + " -e 'bash -c \"{}; read -rsn1 -p \"Terminate...\"\"'".format(command)
        os.system(command)
