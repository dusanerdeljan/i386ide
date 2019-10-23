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

class Documentation(object):

    INFO = {
        'Overview': """<h1 id="installingi386ide">INSTALLING i386ide</h1>""",
        'Linux': """<h1 id="installation">Installation</h1>""",
        'Tips': """<h1 id="basic">Basic</h1>""",
        'User interface': """<h1 id="basiclayout">Basic layout</h1>""",
        'Settings': """<h1 id="basicsettings">Basic settings</h1>

<p>Currently there are settings options for setting up a default workspace, tool tips and snippets. 
We plan to make a unified settings menu in the future that will contain all the relevant options in one place.</p>

<h2 id="defaultworkspace">Default workspace</h2>

<p>To edit the default workspace, click on the <code style='background-color: grey;'>Edit default workspace</code> option in the <code style='background-color: grey;'>Edit</code> drop-down menu.</p>

<h3 id="changedefaultworkspace">Change default workspace</h3>

<p>To change the default workspace, simply select the name of the workspace from the combo box, and click on the <code style='background-color: grey;'>Save workspace configuration</code> button.</p>

<h3 id="disabledefaultworkspace">Disable default workspace</h3>

<p>If you want to disable default workspace, select the <code style='background-color: grey;'>No default workspace</code> item in the combo box, and click on the <code style='background-color: grey;'>Save workspace configuration</code> button.</p>

<h2 id="editcodesnippets">Edit code snippets</h2>

<p>Code snippets editing can be accessed by clicking on the <code style='background-color: grey;'>Edit code snippets</code> option in the <code style='background-color: grey;'>Edit</code> drop-down menu.
For more information about snippets, see the Code snippets section in the user guide.</p>

<h2 id="editidesettings">Edit IDE settings</h2>

<p>To find the IDE settings menu, click on the <code style='background-color: grey;'>Edit IDE settings</code> option in the <code style='background-color: grey;'>Edit</code> drop-down menu.
Currently there are only and options for tooltips.</p>

<h3 id="tooltipconfiguration">Tooltip configuration</h3>

<p>To enable/disable tooltips for instructions simply toggle the checkbox in front of the <code style='background-color: grey;'>Show instructions tooltips</code> option.</p>

<p>To enable/disable automatic numbers conversion tooltips, simply toggle the checkbox in front of the <code style='background-color: grey;'>Show converted numbers</code> option.</p>

<p><code style='background-color: grey;'>Reset to defaults</code> button will reset the setting to the default values. <br />
To save the changes you made click on the <code style='background-color: grey;'>Save changes</code> button. To discard the changes, click on the <code style='background-color: grey;'>Cancel</code> button.</p>""",
        'Basic editing': """<h1 id="basicediting">Basic editing</h1>

<p>Code editing in i386ide was designed to be highly intuitive, and most of the basic features will hopefully feel familiar to most new users. Therefore we will highlight some interesting features that will improve your user experience.</p>

<h2 id="saveandautosave">Save and Auto Save</h2>

<p>Both manual and automatic saving is available in i386ide.</p>

<p>User can save the currently selected file manually by using a default shortcut <code style='background-color: grey;'>Ctrl+ S</code>. <br />
All files in the Workspace can be saved manually by using a default shortcut <code style='background-color: grey;'>Ctrl + Shift + S</code>. <br />
In case there are any unsaved changes in the current workspace, user will be notified and asked if he wants to save or discard the changes when files are being closed.</p>

<p>Automatic backup save is created every 5 minutes by default. <br />
Backup save is also created at the same time the regular save is being performed.</p>

<h2 id="crashdetectionforbackupactivation">Crash detection for backup activation</h2>

<p>If the program was closed abruptly because of power failure or some other cause, i386ide will be able to detect it.
In that case, next time the user starts the same workspace that was being used when the program was closed, he will be asked if he wants to restore backup of all the files in that workspace.</p>

<h2 id="findandreplace">Find and replace</h2>

<p>User can quickly open a search widget by using a default hotkey <code style='background-color: grey;'>Ctrl + F</code>. <br />
Expression can then be interred in the <code style='background-color: grey;'>Find</code> field, and the matching results will be highlighted in the text in real time. <br />
It is possible to cycle through the matching results by pressing <code style='background-color: grey;'>Enter</code> by default.</p>

<p>To replace a word specified in the <code style='background-color: grey;'>Find</code> field, user should put a replacement word into the <code style='background-color: grey;'>Replace</code> field and hit <code style='background-color: grey;'>Enter</code> while the <code style='background-color: grey;'>Replace</code> field is in focus. <br />
All matching results can be replaced by clicking on the <code style='background-color: grey;'>Replace all</code> button.</p>

<h2 id="indentation">Indentation</h2>

<p>By default, i386ide uses 4 spaces for indentation. <br />
Number of spaces used for indentation can be easily changed by selecting the desired indentation value in the bottom right corner of the program.</p>""",
        'Code completion': """<h1 id="codecompletion">Code completion</h1>

<p>Words can be completed in the code by using the default shortcut <code style='background-color: grey;'>Ctrl + Space</code> and by selecting the desired word from the list of suggestions. User can then press the <code style='background-color: grey;'>Enter</code> key to insert the selected word, or <code style='background-color: grey;'>Escape</code> key to close the list of suggestions for completion.</p>

<p>When Assembly file is opened or manually saved, it is then scanned for labels and values in <code style='background-color: grey;'>.section data</code>. <br />
These labels, values and instructions will then show up in the list of suggestions when using code completion.</p>

<p>The same shortcut <code style='background-color: grey;'>Ctrl + Space</code> can be used for snippets insertion.</p>""",
        'Code navigation': """<h1 id="codenavigation">Code navigation</h1>

<p>Jumping to definitions is easy because i386ide offers one click solutions for both Assembly and C files.</p>

<h2 id="assemblyfiles">Assembly files</h2>

<p>In Assembly files it is possible to jump to any label declaration, or any value from the .section data. <br />
Simply hold <code style='background-color: grey;'>Ctrl</code> and left click on the underlined word to jump to its declaration.</p>

<p>Use <code style='background-color: grey;'>Ctrl + Left arrow key</code> to jump back to the position where you clicked the word.</p>

<h2 id="cfiles">C files</h2>

<p>In C files it is possible to jump to function definition by simply holding <code style='background-color: grey;'>Ctrl</code> and left clicking on the name of the function.</p>

<p>Use <code style='background-color: grey;'>Ctrl + Left arrow key</code> to jump back to the position where you clicked the word.</p>""",
        'Compiling code': """<h1 id="compilingcode">Compiling code</h1>

<p>For compiling code, i386ide offers one click compiling, per project compiler options, automatic linking of all the files in the project. <br />
The compiled file is also automatically created when you use <code style='background-color: grey;'>Run</code> or <code style='background-color: grey;'>Debug</code> actions.</p>

<h2 id="compilingprojects">Compiling projects</h2>

<p>To compile the code in the currently selected project click on the <code style='background-color: grey;'>Compile</code> button in the toolbar, or use the <code style='background-color: grey;'>Ctrl + Shift + F5</code> shortcut. <br />
A new <code style='background-color: grey;'>.out</code> file will be created in the project directory and will be named after the project that is being compiled.  </p>

<h2 id="compileroptions">Compiler options</h2>

<p>The compiler will use the default compiler options <code style='background-color: grey;'>-g;-m32</code> when compiling, unless some other compiler options are specified. <br />
To manually specify what options should be used when compiling the selected project,  <code style='background-color: grey;'>right click</code> on the project in the tree view and select <code style='background-color: grey;'>Compiler options</code>. <br />
A new window will appear with the text field where you can enter new options separated with <code style='background-color: grey;'>;</code>. <br />
There you also have the options to <code style='background-color: grey;'>Save</code> the changes, <code style='background-color: grey;'>Cancel</code> or <code style='background-color: grey;'>Reset to default</code>, witch will set the options to <code style='background-color: grey;'>-g;-m32</code>.</p>

<p>For more information on gcc compiler options please visit the <a href="https://gcc.gnu.org/onlinedocs/gcc/Option-Summary.html">https://gcc.gnu.org/onlinedocs/gcc/Option-Summary.html</a>.</p>

<h2 id="manuallycompilefromterminal">Manually compile from terminal</h2>

<p>It is also possible to manually compile using the built-in terminal, just like you would use any other terminal for compiling. <br />
Files can be compiled by using any compiler available on your system.</p>

<p>You can either use full paths when compiling from the terminal, or position yourself in the project folder using the <code style='background-color: grey;'>cd</code> command, and compile the files present in the project folder without having to type in the full path of the files.</p>

<h3 id="assemblefiles">Assemble files</h3>

<p>To manually assemble files use <code style='background-color: grey;'>as -o {file.o} {file.S}</code></p>

<h3 id="linkingfiles">Linking files</h3>

<p>To manually link files use <code style='background-color: grey;'>ld -o {project_name.out} {file_names.o}</code></p>""",
        'Debugging code': """<h1 id="debuggingcode">Debugging code</h1>

<p>For debugging, i386ide uses the Data Display Debugger by default.  </p>

<p>To debug the code, simply click on the <code style='background-color: grey;'>Debug</code> button in the toolbar, or use the <code style='background-color: grey;'>Ctrl + F5</code> shortcut, and the project files will be automatically compiled and linked and the created <code style='background-color: grey;'>.out</code> file will be opened in Data Display Debugger.</p>

<p>File created for the debugging will be compiled using the Compiler options specified for the project. <br />
Name of the file will be the same as the name of the project that is being debugged.</p>

<p>For more information about debugging with Data Display Debugger please visit the <a href="https://www.gnu.org/software/ddd/">https://www.gnu.org/software/ddd/</a>.</p>

<h2 id="manualdebuggingfromtheterminal">Manual debugging from the terminal</h2>

<p>When manually debugging, you can use <code style='background-color: grey;'>ddd</code> or <code style='background-color: grey;'>gdb</code>. <br />
Just position yourself in the project folder by using the <code style='background-color: grey;'>cd</code> commands, and type the desired command in the build in terminal.</p>""",
        'Running code': """<h1 id="runningcode">Running code</h1>

<p>To run the code in the project, simply click on the <code style='background-color: grey;'>Run</code> button in the toolbar, or use the default hotkey <code style='background-color: grey;'>F5</code>.</p>

<p>Project files will be automatically compiled and linked using the specified compiler options for the project. Then the created <code style='background-color: grey;'>.out</code> file will be started in a separate thread in a new window.</p>

<h2 id="manuallyrunthefilefromtheterminal">Manually run the file from the terminal</h2>

<p>To manually run the compiled file just use <code style='background-color: grey;'>./{name_of_the_file.out}</code>. <br />
You may want to position yourself in the directory that contains the <code style='background-color: grey;'>.out</code> file you want to run by using the <code style='background-color: grey;'>cd</code> commands.</p>""",
        'Integrated terminal': """<h1 id="integratedterminal">Integrated terminal</h1>

<p>i386ide offers a built-in terminal that can be useful in a variety of ways.</p>

<h2 id="usingyourowncommands">Using your own commands</h2>

<p>You can enter your own command bash commands like you would do in the linux terminal.  </p>

<p>That includes useful commands such as:</p>

<ul>
<li><code style='background-color: grey;'>cd {some_path}</code> for changing the directory</li>

<li><code style='background-color: grey;'>cd ..</code> to go to the parent directory</li>

<li><code style='background-color: grey;'>cd -</code> to go back to the previous directory</li>

<li><code style='background-color: grey;'>ls</code> to list the contents of the current working directory <br />
... and much more.</li>
</ul>

<h2 id="autocompletion">Auto completion</h2>

<p>Auto completing behaves similarly to the linux terminal auto completion because it relies on bash compgen function.</p>

<p>Press <code style='background-color: grey;'>Tab</code> once to try to auto complete the last word in the current command. <br />
If the word was not auto completed there are either multiple suggestions or no suggestions at all available.</p>

<p>To list all the available suggestions press <code style='background-color: grey;'>Tab</code> twice, and the list of available auto complete suggestions will be displayed in the terminal.</p>

<h2 id="displayingbackgroundcommands">Displaying background commands</h2>

<p>When the i386ide executes a command like <code style='background-color: grey;'>Compile</code>, <code style='background-color: grey;'>Debug</code> or <code style='background-color: grey;'>Run</code> automatically, that command is printed in the terminal with all the options and parameters. <br />
This transparency allows for a better understanding and faster learning of how these processes look like for Assembly or C code.</p>

<h3 id="displayingerrors">Displaying errors</h3>

<p>If some errors occur, they will also be displayed in the terminal. <br />
This can allow you to precisely understand what went wrong with the execution of the command.</p>

<h2 id="externalshellforrunningprograms">External shell for running programs</h2>

<p>When the <code style='background-color: grey;'>.out</code> file is executed, either manually or by using the <code style='background-color: grey;'>Run</code> command, that program is then started in an external shell in a separate thread.</p>""",
        'Snippets': """<h1 id="snippets">Snippets</h1>

<p>Creating and inserting code snippets can speed up your coding.</p>

<h2 id="insertingsnippets">Inserting snippets</h2>

<p>To insert a snippet, type in a snippet name and press <code style='background-color: grey;'>Ctrl + Space</code>, and the snippet will be inserted in the code at the same location.</p>

<h2 id="snippeteditor">Snippet editor</h2>

<p>To open an editor for code snippets select the <code style='background-color: grey;'>Edit code snippets</code> option from the <code style='background-color: grey;'>Edit</code> drop-down menu.</p>

<p>In the snippet editor, a list of existing snippets is displayed on the left side of the window. <br />
On the right side is a field with the name of the selected snippet, and a larger text field with the contents of the snippet.</p>

<h3 id="addingsnippet">Adding snippet</h3>

<p>To add a snippet, press the <code style='background-color: grey;'>Add</code> button, and enter a unique snippet name, then click the <code style='background-color: grey;'>Ok</code> button.</p>

<h3 id="removingsnippet">Removing snippet</h3>

<p>To remove a snippet, select the snippet in the list of snippets, and press the <code style='background-color: grey;'>Remove</code> button, and then confirm you want to remove the snippet.</p>

<h3 id="changesnippetname">Change snippet name</h3>

<p>To change the name of the snippet, select the snippet in list of snippets on the left, and then change the name of the selected snippet in the field on the right. You have to choose an unique name for the snippet. <br />
Then you need to press the <code style='background-color: grey;'>Apply</code> or <code style='background-color: grey;'>Ok</code> button to confirm the changes.</p>

<h3 id="changesnippetcontent">Change snippet content</h3>

<p>To change the content of the snippet, select the snippet in list of snippets on the left, and then change the content of the selected snippet in the big text field on the right. <br />
Then you need to press the <code style='background-color: grey;'>Apply</code> or <code style='background-color: grey;'>Ok</code> button to confirm the changes.</p>

<h3 id="cancelingchanges">Canceling changes</h3>

<p>If you don't want to save the changes you made while editing snippet, you can just select some other snippet without clicking <code style='background-color: grey;'>Apply</code> button beforehand, or just click the <code style='background-color: grey;'>Cancel</code> button.</p>

<h3 id="resettodefault">Reset to default</h3>

<p><code style='background-color: grey;'>Reset to default</code> will delete all the snippets in the snippet list, and populate it with the default snippets.
This <strong>will delete</strong> all snippets created by the user, and any changes made to the default snippets will be lost.</p>"""
    }