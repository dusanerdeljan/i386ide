#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
EXE_PATH="${DIR}/i386ide"
if [ ! -f "$EXE_PATH" ]; then
	echo "Error: Executable ${EXE_PATH} does not exist!"
	exit 1
fi
ICON_PATH="${DIR}/icon.png"
if [ ! -f "$ICON_PATH" ]; then
	echo "Error: Icon ${ICON_PATH} does not exist!"
	exit 1
fi
DESKTOP_FILE_PATH="${DIR}/i386ide.desktop"
USERNAME=$SUDO_USER
DEST_PATH="/home/${USERNAME}/Desktop/.i386ide_application_data"
if [ -d "$DEST_PATH" ]; then
	echo "Error: ${DIR} already exists! Please uninstall the program first!"
	exit 1
else
	mkdir $DEST_PATH
fi
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
SCRIPT_NAME="$(basename "$(test -L "$0" && readlink "$0" || echo "$0")")"
sudo rm -f "${DIR}/${SCRIPT_NAME}"
