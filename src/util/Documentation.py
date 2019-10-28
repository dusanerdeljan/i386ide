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
        'Overview': """<h1 id="usingi386ide">Using i386ide</h1>

<p>There are many ways i386ide can be used. It can be run directly from the source code, it can be installed using scripts and it can even be run by simply downloading an executable file for the designated system.</p>

<h2 id="compatibleoperatingsystems">Compatible operating systems</h2>

<p>Our IDE was designed to run on Ubuntu Linux, but it can also run on many different distributions of Linux. <br /><br />
For more information, visit the <a style='color: #007ACC;'   href="="https://github.com/dusanerdeljan/i386ide/wiki/Linux">Linux</a> section of this guide.</p>

<h2 id="additionalrequirements">Additional requirements</h2>

<p>To properly use all features of the i386ide some additional software will have to be installed on the system.</p>

<p>This currently includes gcc (GNU Compiler Collection) and ddd (Data display debugger).</p>

<p>If you are using a 64-bit operating system you will also need gcc-multilib.</p>

<p>There are some additional requirements when running from the source code that are described in detail in the Linux section.</p>""",
        'Linux': """<h1 id="linux">Linux</h1>

<p>Our IDE was designed and tested to work on Linux Ubuntu 16.04 or higher.  </p>

<p>It was also tested on different Linux distributions, and so far it works on:</p>

<ul>
<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Linux#ubuntu">Ubuntu 16.04 and higher</a>  </li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Linux#debian">Debian 10.1.0</a>  </li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Linux#mint">Mint 19.2</a>  </li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Linux#fedora">Fedora 30.1.2</a></li>
</ul>

<h1 id="ubuntu">UBUNTU</h1>

<p>Ubuntu 16.04 or later is required to run i386ide.  </p>

<p>We tried to make it run on some older distribution of Ubuntu, such as 12.04, 14.04, but there were many problems with some outdated files that we were not able to solve (most were related to the old version of glibc).</p>

<h2 id="commonprerequisites">Common prerequisites</h2>

<p>To properly run, compile and debug <a style='color: #007ACC;'   href="https://gcc.gnu.org/">gcc</a> and <a style='color: #007ACC;'   href="https://www.gnu.org/software/ddd/">ddd</a> are required.</p>

<h3 id="gcc">GCC</h3>

<p>To check if you have gcc installed enter this command in the terminal: <br />
<code style='background-color: grey;'>gcc --version</code> <br />
It should list the version of the installed gcc, or tell you if it is not installed.
For 64-bit operating systems gcc-multilib is also needed.</p>

<p>To install gcc enter these commands: <br />
<code style='background-color: grey;'>sudo apt-get install gcc</code> <br />
<code style='background-color: grey;'>sudo apt-get install gcc-multilib</code>  </p>

<h3 id="ddd">DDD</h3>

<p>To check if you have ddd installed enter this command in the terminal: <br />
<code style='background-color: grey;'>ddd --version</code>  </p>

<p>To install ddd enter this command: <br />
<code style='background-color: grey;'>sudo apt-get install ddd</code>  </p>

<h2 id="runninganexecutablefile">Running an executable file</h2>

<p>Other than the common prerequisites, running the executable file should not require any additional installations.</p>

<p>To run the executable file, simply download the version for your operating system, extract the zip archive, and double click on the i386ide file.</p>

<p>Sometimes you will have to manually enable the execution of the i386ide file. It can be done this way:</p>

<ol>
<li>Right click on the i386ide file, and go to properties</li>

<li>Go to permissions tab</li>

<li>Make sure the box is checked next to the <code style='background-color: grey;'>Allow executing file as program</code> option.</li>
</ol>

<h2 id="installinganduninstallingusingscripts">Installing and uninstalling using scripts</h2>

<p>To install and uninstall i386ide you can use scripts.</p>

<h3 id="installscript">Install script</h3>

<p>To install simply follow these steps:</p>

<ol>
<li>Download i386ide archive, and extract i386ide file and icon.</li>

<li>Download and extract the scripts in the same folder where i386ide executable file and the icon are located.</li>

<li>Position yourself in the extracted folder and run <code style='background-color: grey;'>sudo bash install.sh</code> to install the program.   </li>
</ol>

<p>This will create a desktop entry, and you will be able to run the program from the terminal, or find it when searching for activities in Ubuntu.</p>

<h3 id="uninstallscript">Uninstall script</h3>

<p>To uninstall previously installed i386ide, simply follow these steps.</p>

<ol>
<li>Download and extract the shell scripts <strong>to any location</strong>.</li>

<li>Position yourself in the extracted folder and run <code style='background-color: grey;'>sudo bash uninstall.sh</code></li>
</ol>

<h2 id="runningtheprogramfromthesourcecode">Running the program from the source code</h2>

<p>To run this program from the source code you need Python 3.6 or higher and you have to install PySide2 library. <br />
Run command is <code style='background-color: grey;'>python3 main.py</code>  </p>

<p>Make sure you have software listed in Common prerequisites installed.</p>

<h3 id="updatingyourfiles">Updating your files</h3>

<p>First you should make sure your files are updated by using these commands: <br />
<code style='background-color: grey;'>sudo apt-get update</code> <br />
<code style='background-color: grey;'>sudo apt-get upgrade</code></p>

<p>You can also restart your computer to make sure all updates are installed and are being used.</p>

<h3 id="ubuntu1804orhigher">Ubuntu 18.04 or higher</h3>

<p>Python 3.6 should come preinstalled on Ubuntu 18.04.</p>

<p>Make sure python3-dev is installed by running the command: <br />
<code style='background-color: grey;'>sudo apt install python3-dev</code>  </p>

<p>It is easy to install Pyside2 using pip.</p>

<h4 id="pip">PIP</h4>

<p>To check if pip is installed for python 3.6 run this command in the terminal: <br />
<code style='background-color: grey;'>pip3 --version</code> <br />
If it is not installed, you should run this command to install it: <br />
<code style='background-color: grey;'>sudo apt-get install python3-pip</code>  </p>

<p>Now you can use pip3 to install additional libraries.</p>

<p>If you have pip installed for Python2, then run all the commands with <code style='background-color: grey;'>pip3</code> instad of <code style='background-color: grey;'>pip</code>.</p>

<h4 id="pyside2">Pyside2</h4>

<p>Now that you have pip3 installed, simply use the following command to install Pyside2: <br />
<code style='background-color: grey;'>pip3 install pyside2</code></p>

<p>After pyside2 is installed, you should be able to run the program from source code. <br />
Simply position yourself in the folder that contains the main.py file, and run it by using the command: <br />
<code style='background-color: grey;'>python3 main.py</code>  </p>

<h3 id="ubuntu1604">Ubuntu 16.04</h3>

<p>Ubuntu 16 comes with Python 3.5 preinstalled, so you will have to install Python 3.6 or higher manually.  </p>

<h4 id="installingpython36">Installing python 3.6</h4>

<p>To install python3.6 on Ubuntu 16.04 run the following commands: <br />
<code style='background-color: grey;'>sudo add-apt-repository ppa:deadsnakes/ppa</code> <br />
<code style='background-color: grey;'>sudo apt update</code> <br />
<code style='background-color: grey;'>sudo apt install python3.6</code> <br />
<code style='background-color: grey;'>sudo apt-get install python3.6-dev</code></p>

<h4 id="pip-1">PIP</h4>

<p>One way to install pip is by using curl.</p>

<p>First install curl by using: <br />
<code style='background-color: grey;'>sudo apt install curl</code>  </p>

<p>After that run the following commands to install pip: <br />
<code style='background-color: grey;'>sudo su</code> <br />
<code style='background-color: grey;'>curl https://bootstrap.pypa.io/ez_setup.py -o - | python3.6</code> <br />
<code style='background-color: grey;'>python3.6 -m easy_install pip</code>  </p>

<p>To check if pip was installed for python 3.6, enter this command: <br />
<code style='background-color: grey;'>python3.6 -m pip --version</code> <br />
or if you don't have pip installed for any other version of python, you can just run: <br />
<code style='background-color: grey;'>pip --version</code>   </p>

<p>You can then restart your system to make sure everything is loaded.</p>

<h4 id="pyside2-1">Pyside2</h4>

<p>Now you can install Pyside2 with pip by using the command: <br />
<code style='background-color: grey;'>sudo -H python3.6 -m pip install pyside2</code> <br />
or if you don't have pip installed for any other version of python: <br />
<code style='background-color: grey;'>sudo -H pip install pyside2</code>  </p>

<p>After pyside2 is installed, you should be able to run the program from source code. <br />
Simply position yourself in the folder that contains the main.py file, and run it by using the command: <br />
<code style='background-color: grey;'>python3 main.py</code>  </p>

<h2 id="makingyourownexecutablewithpyinstaller">Making your own executable with Pyinstaller</h2>

<p>It is possible to make your own executable from the source code by using Pyinstaller.</p>

<p>First follow the steps from <code style='background-color: grey;'>Running the program from the source code</code> section for the appropriate Ubuntu version.</p>

<h4 id="pyinstallerforubuntu1804orhigher">Pyinstaller for Ubuntu 18.04 or higher</h4>

<p>To install pyinstaller just run the command: <br />
<code style='background-color: grey;'>pip install pyinstaller</code>  </p>

<p>If <code style='background-color: grey;'>setuptools</code> is missing then run the command:
<code style='background-color: grey;'>pip install setuptools</code></p>

<h4 id="pyinstallerforubuntu1604">Pyinstaller for Ubuntu 16.04</h4>

<p>One way of installing Pyinstaller (especially if you followed the instructions from <code style='background-color: grey;'>Running the program from the source code</code> section) is to enter these commands: <br />
<code style='background-color: grey;'>sudo -H pip install -U pip setuptools</code> <br />
<code style='background-color: grey;'>sudo -H python3.6 -m pip install pyinstaller</code>  </p>

<h3 id="usingthepyinstaller">Using the pyinstaller</h3>

<p>To make sure all the icons are included in the program, you have to make sure to follow the procedure listed here.</p>

<p>First, position yourself in folder where the main.py file is located.</p>

<h4 id="makeandeditspecfile">Make and edit .spec file</h4>

<p>To pack all resources into one executable file you need to make a .spec file by using: <br />
<code style='background-color: grey;'>pyinstaller main.py --onefile</code>  </p>

<p>If you instead want to put all the resources into one folder with many files, just create a .spec file with: <br />
<code style='background-color: grey;'>pyinstaller main.py</code></p>

<p>Alternatively, you can try to create a spec file by using:
<code style='background-color: grey;'>pyi-makespec main.spec --onefile</code> or <code style='background-color: grey;'>pyi-makespec main.spec</code>   </p>

<p>After that you need to open the main.spec file and edit some lines.
In the <code style='background-color: grey;'>a = Analysis</code> section you need to add the following values to the datas item: <br />
<code style='background-color: grey;'>('./resources/*.png','resources')</code> <br />
<code style='background-color: grey;'>('./resources/*.ico','resources')</code>  </p>

<p>datas should now look like this: <br />
<code style='background-color: grey;'>datas=[('./resources/*.png','resources'),('./resources/*.ico','resources')],</code> <br />
That will add the icons to the executable file that will be created.</p>

<p>In the <code style='background-color: grey;'>exe = EXE</code> section, change the name of the program to: <br />
<code style='background-color: grey;'>name='i386ide',</code> <br />
That will change the name of the executable file that will be created.</p>

<p>Now save the changes to the main.spec file.</p>

<h4 id="maketheexecutablefileandrunit">Make the executable file and run it</h4>

<p>After that, to finally crate an executable file run the following command: <br />
<code style='background-color: grey;'>pyinstaller main.spec</code></p>

<p>When the process is finished, you can find the created file(s) in the <code style='background-color: grey;'>dist</code> folder.</p>

<p>If the spec file was created with the <code style='background-color: grey;'>--onefile</code> option, everything will be packed into one executable file. <br />
If the spec file was created without the <code style='background-color: grey;'>--onefile</code> option, all files will be placed inside a folder.</p>

<p>Now you can double click on the i386ide file in the dist folder to run the program. <br />
To make sure that the i386ide file can be executed do the following:  </p>

<ol>
<li>Right click on the i386ide file, and go to properties</li>

<li>Go to permissions tab</li>

<li>Make sure the box is checked next to the <code style='background-color: grey;'>Allow executing file as program</code> option.</li>
</ol>

<h1 id="debian">Debian</h1>

<p>It is possible to run i386ide on Debian. </p>

<p>It was tested on Debian 10.1.0.</p>

<p>Because of the similarities, you should just follow the guide for <a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Linux#ubuntu">Ubuntu 18.04</a></p>

<h1 id="mint">Mint</h1>

<p>It is possible to run i386ide on Mint.</p>

<p>It was tested on Mint 19.2.</p>

<p>Because of the similarities, you should just follow the guide for <a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Linux#ubuntu">Ubuntu 18.04</a></p>

<h1 id="fedora">Fedora</h1>

<p>We managed to get i386ide working on Fedora 30.1.2.  </p>

<p>This guide may not work on earlier versions of Fedora.</p>

<h2 id="commonprerequisites-1">Common prerequisites</h2>

<p>To properly run, compile and debug <a style='color: #007ACC;'   href="https://gcc.gnu.org/">gcc</a> and <a style='color: #007ACC;'   href="https://www.gnu.org/software/ddd/">ddd</a> are required.</p>

<h3 id="gcc-1">GCC</h3>

<p>To check if you have gcc installed enter this command in the terminal: <br />
<code style='background-color: grey;'>gcc --version</code> <br />
It should list the version of the installed gcc, or tell you if it is not installed.
For 64-bit operating systems gcc-multilib is also needed.</p>

<p>To install gcc enter these commands: <br />
<code style='background-color: grey;'>sudo dnf install gcc</code> <br />
<code style='background-color: grey;'>sudo yum install gcc gcc-c++</code> <br />
<code style='background-color: grey;'>sudo dnf install glibc-devel.i686</code>    </p>

<h3 id="ddd-1">DDD</h3>

<p>To check if you have ddd installed enter this command in the terminal: <br />
<code style='background-color: grey;'>ddd --version</code>  </p>

<p>To install ddd enter this command: <br />
<code style='background-color: grey;'>sudo dnf install ddd</code>  </p>

<h2 id="runninganexecutablefile-1">Running an executable file</h2>

<p>Same <a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Linux#running-an-executable-file">procedure for running</a> as it is for Ubuntu.</p>

<h2 id="installinganduninstallingusingscripts-1">Installing and uninstalling using scripts</h2>

<p>Same <a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Linux#installing-and-uninstalling-using-scripts">procedure for install and uninstall</a> as it is for Ubuntu.</p>

<h2 id="runningtheprogramfromthesourcecode-1">Running the program from the source code</h2>

<p>To run this program from the source code you need Python 3.6 or higher and you have to install PySide2 library. <br />
Run command is <code style='background-color: grey;'>python3 main.py</code>  </p>

<p>Make sure you have software listed in Common prerequisites installed.</p>

<h3 id="updatingyourfiles-1">Updating your files</h3>

<p>First you should make sure your files are updated by using these commands: <br />
<code style='background-color: grey;'>sudo dnf check-update</code> <br />
<code style='background-color: grey;'>sudo dnf upgrade</code>  </p>

<p>You can also restart your computer to make sure all updates are installed and are being used.</p>

<h3 id="fedora3012orhigher">Fedora 30.1.2 or higher</h3>

<p>Python 3.7 should come preinstalled on Fedora 30.1.2.</p>

<p>It is easy to install Pyside2 using pip.</p>

<h4 id="pip-2">PIP</h4>

<p>To check if pip is installed for python 3.7 run this command in the terminal: <br />
<code style='background-color: grey;'>pip3 --version</code> <br />
If it is not installed, you should run this command to install it: <br />
<code style='background-color: grey;'>sudo dnf install python3-pip</code>  </p>

<p>Now you can use pip3 to install additional libraries.</p>

<h4 id="pyside2-2">Pyside2</h4>

<p>Now that you have pip3 installed, simply use the following command to install Pyside2: <br />
<code style='background-color: grey;'>pip3 install pyside2</code></p>

<p>After pyside2 is installed, you should be able to run the program from source code. <br />
Simply position yourself in the folder that contains the main.py file, and run it by using the command: <br />
<code style='background-color: grey;'>python3 main.py</code>  </p>

<h2 id="makingyourownexecutablewithpyinstaller-1">Making your own executable with Pyinstaller</h2>

<p>It is possible to make your own executable from the source code by using Pyinstaller.</p>

<p>First follow the steps from <code style='background-color: grey;'>Running the program from the source code</code> section for the Fedora version.</p>

<h4 id="pyinstallerforfedora3012orhigher">Pyinstaller for Fedora 30.1.2 or higher</h4>

<p>To install pyinstaller just run the command: <br />
<code style='background-color: grey;'>pip install pyinstaller</code>  </p>

<h3 id="usingthepyinstaller-1">Using the pyinstaller</h3>

<p>It is the same <a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Linux#using-the-pyinstaller">procedure for using the pyinstaller</a>  as it is for Ubuntu.</p>""",
        'Tips': """<h1 id="tips">Tips</h1>

<p>Some select features of the i386ide are listed here.
To discover more advanced features, please refer to the user guide.</p>

<h2 id="tabswitcher">Tab switcher</h2>

<p>To switch between the active tabs you can use the Tab switcher by activating it with <code style='background-color: grey;'>Ctrl + Tab</code> buttons.</p>

<p>You can move through tabs from top to bottom with <code style='background-color: grey;'>Ctrl + Tab</code> or <code style='background-color: grey;'>Down arrow key</code>, and in the opposite direction with the <code style='background-color: grey;'>Ctrl + Shift + Tab</code> or <code style='background-color: grey;'>Up arrow key</code>.</p>

<p>When the <code style='background-color: grey;'>Ctrl</code> key is released the selected tab will be opened in the code editor.</p>

<h2 id="projectswitcher">Project switcher</h2>

<p>To switch the currently selected project you can use the Project switcher by activating it with <code style='background-color: grey;'>Ctrl + E</code>.</p>

<p>You can move through project from top to bottom with <code style='background-color: grey;'>Ctrl + E</code>, <code style='background-color: grey;'>Ctrl + Tab</code> or <code style='background-color: grey;'>Down arrow key</code>, and in the opposite direction with the <code style='background-color: grey;'>Ctrl + Shift + Tab</code> or <code style='background-color: grey;'>Up arrow key</code>.</p>

<p>When the <code style='background-color: grey;'>Ctrl</code> key is released the selected project will be set as active in the toolbar.</p>""",
        'User interface': """<h1 id="userinterface">User Interface</h1>

<p>On the one hand, the default interface in i386ide was made with the idea to be helpful and welcoming for the people who have just started programming in Assembly language. <br />
We tried to pick the most useful tools that a beginner will need, and make those tools available from the get-go.</p>

<p>On the other hand, the whole interface is a collection of widgets that the user can individually move, show or hide. <br />
This creates a highly customizable interface that experienced users can tune to their liking.  </p>

<h1 id="basiclayout">Basic Layout</h1>

<p>The basic layout that you encounter when you start the application should feel familiar and intuitive, and consist of the following elements:</p>

<ul>
<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#menu-bar">Menu bar</a> at the top with drop-down menu's.</li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#toolbar">Toolbar</a> just below the menu bar.</li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#workspace-explorer">Workspace explorer</a> on the left side</li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#code-editor">Code editor</a> in the center.</li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#instructions-widget">Instructions widget</a> on the right that can be used to search up any instruction.</li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#ascii-table">ASCII table</a> just below the instructions widget.</li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#terminal">Fully integrated Terminal</a> at the bottom.</li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#status-bar">Status bar</a> just below the terminal.</li>
</ul>

<h2 id="menubar">Menu bar</h2>

<p>The menu bar is located at the top of the application window. It contains the <code style='background-color: grey;'>File</code>, <code style='background-color: grey;'>Edit</code>, <code style='background-color: grey;'>View</code> and <code style='background-color: grey;'>Help</code> drop-down menu's.  </p>

<h3 id="filedropdownmenu">File drop-down menu</h3>

<p>Here you can find the following functionalities:  </p>

<ul>
<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#quick-assembly-project-activated-via-ctrl--p">Quick assembly project</a>(activated via <code style='background-color: grey;'>Ctrl + P</code>)</li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#new-workspace-activated-via-ctrl--n">New workspace</a> (activated via <code style='background-color: grey;'>Ctrl + N</code>)</li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#open-workspace-activated-via-ctrl--o">Open workspace</a> (activated via <code style='background-color: grey;'>Ctrl + O</code>)</li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#switch-workspace-activated-via-ctrl--w">Switch workspace</a> (activated via <code style='background-color: grey;'>Ctrl + W</code>)</li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#save-workspace-activated-via-ctrl--shift--s">Save workspace</a> (activated via <code style='background-color: grey;'>Ctrl + Shift + S</code>)</li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#save-file--activated-via-ctrl--s">Save file</a>  (activated via <code style='background-color: grey;'>Ctrl + S</code>)</li>
</ul>

<h4 id="quickassemblyprojectactivatedviactrlp">Quick assembly project (activated via <code style='background-color: grey;'>Ctrl + P</code>)</h4>

<p>Activating this option will prompt you to enter the name of the project, and then the project and the file with the same name will be created and instantly opened in the <code style='background-color: grey;'>Code editor</code>.</p>

<h4 id="newworkspaceactivatedviactrln">New workspace (activated via <code style='background-color: grey;'>Ctrl + N</code>)</h4>

<p>This option will prompt you to choose a location for a new workspace, and if the location is valid, it will then create and open a new empty workspace.</p>

<h4 id="openworkspaceactivatedviactrlo">Open workspace (activated via <code style='background-color: grey;'>Ctrl + O</code>)</h4>

<p>When activated, you will be prompted to choose the location of the workspace you want to open. <br />
There are a few cases depending on what folder you chose.</p>

<p>If a folder with an existing .metadata file is chosen (indicating it is a Workspace folder), that .metadata file will be loaded and the workspace with all the projects tied to it will be opened.</p>

<p>Alternatively, if the folder you chose does not contain a .metadata file, then a new empty workspace will be created at that location.</p>

<h4 id="switchworkspaceactivatedviactrlw">Switch workspace (activated via <code style='background-color: grey;'>Ctrl + W</code>)</h4>

<p>Switch workspace action work similarly to the <code style='background-color: grey;'>Open Workspace</code> action in that you are prompted to choose a location of the workspace you want to switch to.</p>

<p>If it is a folder with an existing .metadata file, then that workspace and all the project tied to it will be opened.</p>

<p>Otherwise if the folder doesn't contain a .metadata file, then a new empty workspace will be created at that location.</p>

<h4 id="saveworkspaceactivatedviactrlshifts">Save workspace (activated via <code style='background-color: grey;'>Ctrl + Shift + S</code>)</h4>

<p>Using this option will allow you to save all the changes you have made to you files in the editor.</p>

<h4 id="savefileactivatedviactrls">Save file  (activated via <code style='background-color: grey;'>Ctrl + S</code>)</h4>

<p>This option will save the file whose tab is currently active.</p>

<h3 id="editdropdownmenu">Edit drop-down menu</h3>

<p>Here you can find the following actions:</p>

<ul>
<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Basic-editing#find-and-replace">Find and replace</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Settings#default-workspace">Edit default workspace</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Settings#edit-code-snippets">Edit code snippets</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Settings#edit-ide-settings">Edit IDE settings</a></li>
</ul>

<h3 id="viewdropdownmenu">View drop-down menu</h3>

<p>In the view drop-down menu you can toggle the visibility of the widgets in the program such as:</p>

<ul>
<li>Terminal</li>

<li>Workspace explorer</li>

<li>Instructions help</li>

<li>ASCII table</li>

<li>Toolbar</li>
</ul>

<h3 id="helpdropdownmenu">Help drop-down menu</h3>

<p>Here you can find the <code style='background-color: grey;'>About</code> option that displays some basic information's about i386ide.</p>

<p>This whole guide can also be accessed by choosing the <code style='background-color: grey;'>Getting started</code> action.</p>

<h2 id="toolbar">Toolbar</h2>

<p>Toolbar contains the option to select a project and then 'Compile', 'Debug' or 'Run' the selected project. <br />
For more information on those actions see entries for <a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Compiling-code">Compiling</a>, <a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Debugging-code">Debugging</a> and <a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Running-code">Running</a> the code in the user guide.</p>

<h2 id="workspaceexplorer">Workspace explorer</h2>

<p>Workspace explorer displays the current projects and files contained in those projects in the form of a tree view.
It can be moved to the left or the right position of the applications main window.</p>

<p>At the top or the Workspace explorer is the name of the current workspace.</p>

<p>All the projects in the workspace are displayed in the Workspace explorer with the option to expand or contract them to show or hide the contents of the project.</p>

<p>Projects can contain both the Assembly (<code style='background-color: grey;'>.S</code>) and C language (<code style='background-color: grey;'>.C</code>) files.</p>

<h3 id="workspacecontextmenu">Workspace context menu</h3>

<p><code style='background-color: grey;'>Right click</code> on the workspace name or in the empty area in the <code style='background-color: grey;'>Workspace explorer</code> will open a context menu with the following actions:</p>

<ul>
<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#new-project">New project</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#import-project">Import project</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#show-in-files">Show in files</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#quick-assembly-project-activated-via-ctrl--p">Quick assembly project</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#open-file-as-assembly-project">Open file as an assembly project</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#save-workspace-activated-via-ctrl--shift--s">Save workspace</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#quick-assembly-project-activated-via-ctrl--p">Switch workspace</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#rename-workspace">Rename workspace</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#update-workspace">Update workspace</a></li>
</ul>

<h4 id="newproject">New project</h4>

<p>This option will prompt the user to enter the name of the new project, and if the name is not taken, that project will be created in the workspace.</p>

<h4 id="importproject">Import project</h4>

<p>A project with all the <code style='background-color: grey;'>.S</code> and <code style='background-color: grey;'>.C</code> files can be imported by choosing the folder of the project you want to import when this option is selected.</p>

<h4 id="showinfiles">Show in files</h4>

<p>Workspace folder will be opened in file explorer.</p>

<h4 id="openfileasassemblyproject">Open file as assembly project</h4>

<p>This option will prompt you to choose an Assembly (<code style='background-color: grey;'>.S</code>) file, and it will open that file in an completely new project with the same name. If the project with the same name already exists, then an available number will be added to the project name.</p>

<h4 id="renameworkspace">Rename workspace</h4>

<p>This option will allow you to rename the workspace. Simply enter the new workspace name when prompted.</p>

<h4 id="updateworkspace">Update workspace</h4>

<p>Updating the workspace will refresh the contents of the Workspace explorer.</p>

<h3 id="projectcontextmenu">Project context menu</h3>

<p>Right clicking on the project in the Workspace explorer will bring up the context menu with  the following options:</p>

<ul>
<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#save-project">Save project</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Compiling-code#compiler-options">Compiler options</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Compiling-code">Compile project</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Debugging-code">Debug project</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Running-code">Run project</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#show-in-files-1">Show in files</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#new-file">New file</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#import-file">Import file</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#rename-project">Rename project</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#remove-project">Remove project</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#delete-project-from-disk">Delete project from disk</a></li>
</ul>

<h4 id="saveproject">Save project</h4>

<p>This option will save the files that are contained in the project.</p>

<h4 id="showinfiles-1">Show in files</h4>

<p>This will open the project folder in the file explorer.</p>

<h4 id="newfile">New file</h4>

<p>This option will prompt to you to enter the file name and choose the file type. If the file with the same name doesn't already exist in the project, then the file will be created.</p>

<h4 id="importfile">Import file</h4>

<p>You will be prompted to choose a location of the file you want to import in the current project. You can only import the file if the file with the same name doesn't already exist in the same project.</p>

<h4 id="renameproject">Rename project</h4>

<p>Using this action will prompt you to type in the new name for the project. If the name if unique for the current workspace (and there is not a file with the same name on the dist at the same location), then the name of the project will be changed.</p>

<h4 id="removeproject">Remove project</h4>

<p>This option will prompt the user to remove the project from the current workspace.</p>

<h4 id="deleteprojectfromdisk">Delete project from disk</h4>

<p>This option will prompt the user to delete the project contents from both the disk and the workspace.</p>

<h3 id="filecontextmenu">File context menu</h3>

<p>The following actions are available for files in the context menu:</p>

<ul>
<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#show-in-files-2">Show in files</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#save-file">Save file</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#rename-file">Rename file</a></li>

<li><a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/User-interface#delete-file">Delete file</a></li>
</ul>

<h4 id="showinfiles-2">Show in files</h4>

<p>This action will open the location on the disc where the file is located, and highlight the file in the file explorer.</p>

<h4 id="savefile">Save file</h4>

<p>This option will save just the selected file at the location where it is located.</p>

<h4 id="renamefile">Rename file</h4>

<p>User will be prompted to enter the new name for the file. If the new name is unique to the project where the file is located then the rename action will be successful.</p>

<h4 id="deletefile">Delete file</h4>

<p>This option will  delete the file from the disc.</p>

<h3 id="draganddrop">Drag and drop</h3>

<p>It is possible to drag and drop files, or even whole projects into the current workspace by simply dragging and dropping the file from the file system into the Workspace explorer.</p>

<p>If the file is dropped in the text field, then the path to that file will be inserted in that text fiels.</p>

<h4 id="importingprojectswithdraganddrop">Importing projects with drag and drop</h4>

<p>To import a whole project, simply drag it into the Workspace explorer, and the project will be included in the workspace.
If the project with the same name already exists in the workspace, first available number will be added to the imported projects name.</p>

<h4 id="importingfileswithdraganddrop">Importing files with drag and drop</h4>

<p>To import the file in the project, simply drag the file from the file explorer to the project you want to import it in. If the file with the same name already exists in the project it will not be imported.  </p>

<p>Importing multiple files to the project works the same way. Simply select multiple files in the files explorer, and drag and drop them into the project you want to import them in.</p>

<p>Files can also be imported as individual project. To create an individual project from file simply drag the file from the file explorer to the empty area of the Workspace explorer or to the Workspace name and the new project with the same name will be created. If the project with the same name already exists, first available number will be added to the imported projects name.</p>

<p>If multiple files are selected and dragged into the Workspace explorer from the file explorer, then a new project will be created that will include all the selected files.</p>

<h2 id="codeeditor">Code editor</h2>

<p>Code editor takes the central place in the application. It is used to display the content of the opened file, and to allow you to edit and create your own content.</p>

<h3 id="syntaxhighlighting">Syntax highlighting</h3>

<p>Text is highlighted based on the type of file that is opened. </p>

<p>In assembly files many different elements are highlighted such as comments (both singleline and multiline), sections, instructions, registers, various value types, macros, labels, variables and much more.</p>

<p>I C files elements such as functions, variables, types etc. are highlighted.</p>

<h3 id="otherprominentfeatures">Other prominent features</h3>

<p>It supports a variety of other features such as <a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Code-completion">code completion</a>, <a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Code-navigation">smart navigation</a> etc. You can read about those feature in more detail in the <a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Basic-editing">user guide</a>.</p>

<h3 id="workingwithtabs">Working with tabs</h3>

<p>When a file is opened in i386ide by double clicking on the file in the Workspace explorer, a new tab is created. That tab is unique for that file, and will show the name of the file, and indicate if the file has been changed with the <code style='background-color: grey;'>*</code> sign.</p>

<p>It is possible to open multiple files in multiple tabs. </p>

<p>One way to close the tab is to click on the <code style='background-color: grey;'>X</code> button in the top right corner of the tab.
If the file you are about to close was changed, you will be prompted to cancel you action or save or discard the changes you have made to that file.</p>

<p>It is also possible to bring up the context menu for tabs by right clicking on the tab.
Context menu actions are self explanatory and include the following options:</p>

<ul>
<li>Close</li>

<li>Close Others</li>

<li>Close All</li>

<li>Close Unmodified</li>

<li>Close All to the Left</li>

<li>Close All to the Right</li>
</ul>

<p>When the current workspace is about to be closed, files opened in tabs are checked for any unsaved changes. If there are unsaved changes user will be prompted to save or discard those changes, or cancel the closing action.</p>

<h2 id="instructionswidget">Instructions widget</h2>

<p>Instructions widget is located on the right side of the main window and it is used for looking up information about the various instructions available in the assembly language.</p>

<p>These are the same descriptions that are shown in the tooltips that appear when you hover over the instruction in the code editor.</p>

<h3 id="searchingforinstructions">Searching for instructions</h3>

<p>To search for an instruction simply enter the name of the instruction you want to know about in the input field. <br />
Once the name is entered, if available, information about that instruction will be displayed below the input field.</p>

<h2 id="asciitable">ASCII table</h2>

<p>You can find this widget on the right side, just below the Instructions widget. </p>

<p>It is used to display the values of the first 128 ASCII characters. It show the decimal, octal and hexadecimal value of each character.</p>

<h2 id="terminal">Terminal</h2>

<p>Terminal is located at the bottom half of the main window. It show the user all the previous commands that were entered, and also allows him to enter his own commands just like he would do in built-in system terminal.</p>

<p>You can read more about the various features of the Terminal at the <a style='color: #007ACC;'   href="https://github.com/dusanerdeljan/i386ide/wiki/Integrated-terminal">user guide section for terminal</a>.</p>

<h2 id="statusbar">Status bar</h2>

<p>Status bar is located at the bottom of the main window. It show information about the currently selected syntax for the file that is opened, as well as the tab width.</p>

<p>Tab width can be changed to 2, 4 or 8 spaces in the status bar.</p>""",
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
To save the changes you made click on the <code style='background-color: grey;'>Save changes</code> button. To discard the changes, click on the <code style='background-color: grey;'>Cancel</code> button.</p></h1>

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

<p>For more information on gcc compiler options please visit the <a style='color: #007ACC;'   href="https://gcc.gnu.org/onlinedocs/gcc/Option-Summary.html">https://gcc.gnu.org/onlinedocs/gcc/Option-Summary.html</a>.</p>

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

<p>For more information about debugging with Data Display Debugger please visit the <a style='color: #007ACC;'   href="https://www.gnu.org/software/ddd/">https://www.gnu.org/software/ddd/</a>.</p>

<h2 id="manualdebuggingfromtheterminal">Manual debugging from the terminal</h2>

<p>When manually debugging, you can use <code style='background-color: grey;'>ddd</code> or <code style='background-color: grey;'>gdb</code>. <br />
Just position yourself in the project folder by using the <code style='background-color: grey;'>cd</code> commands, and type the desired command in the build in terminal.</p>""",
        'Running code': """<h1 id="runningcode">Running code</h1>

<p>To run the code in the project, simply click on the <code style='background-color: grey;'>Run</code> button in the toolbar, or use the default hotkey <code style='background-color: grey;'>F5</code>.</p>

<p>Project files will be automatically compiled and linked using the specified compiler options for the project. Then the created <code style='background-color: grey;'>.out</code> file will be started in a separate thread in a new window.</p>

<h2 id="manuallyrunthefilefromtheterminal">Manually run the file from the terminal</h2>

<p>To manually run the compiled file just use <code style='background-color: grey;'>./{name_of_the_file.out}</code> <br />
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
