#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
EXE_PATH="${DIR}/i386ide"
ICON_PATH="${DIR}/icon.png"
DESKTOP_FILE_PATH="${DIR}/i386ide.desktop"
USERNAME=$SUDO_USER
DEST_PATH="/home/${USERNAME}/Desktop/.i386ide_application_data"
mkdir $DEST_PATH
DEST_EXE_PATH="${DEST_PATH}/i386ide"
DEST_ICON_PATH="${DEST_PATH}/icon.png"
sudo mv $EXE_PATH $DEST_EXE_PATH
sudo mv $ICON_PATH $DEST_ICON_PATH
touch ./i386ide.desktop 
chmod +x $DEST_EXE_PATH
> ./i386ide.desktop
echo "[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
Terminal=false
Exec=${DEST_EXE_PATH}
Name=i386ide
Icon=${DEST_ICON_PATH}" >> ./i386ide.desktop
sudo mv $DESKTOP_FILE_PATH /usr/share/applications/
sudo install -m 0755 ${DEST_EXE_PATH} /usr/local/bin

