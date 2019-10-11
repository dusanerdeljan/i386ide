#!/bin/bash
USERNAME=$SUDO_USER
sudo rm -rf /home/${USERNAME}/Desktop/.i386ide_application_data
sudo rm -rf /usr/share/applications/i386ide.desktop
sudo rm -rf /usr/local/bin/i386ide
