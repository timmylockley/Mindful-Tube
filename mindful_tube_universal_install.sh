#!/bin/bash
set -e

echo "Starting universal MindfulTube installation..."
cd ~/Desktop/Development/Code/Python

# 1. Install PyInstaller if not already present
if ! command -v pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

# 2. Build a standalone single-file binary
echo "Compiling Python script into a standalone executable..."
pyinstaller --onefile --windowed mindful_tube.py

# 3. Create system-wide installation directories
echo "Installing application files..."
sudo mkdir -p /usr/local/share/mindful-tube
sudo mkdir -p /usr/local/bin
sudo mkdir -p /usr/share/pixmaps

# 4. Copy the compiled binary and icon to standard global paths
sudo cp dist/mindful_tube /usr/local/bin/mindful-tube
sudo cp mindful-tube.png /usr/share/pixmaps/mindful-tube.png

# 5. Create a universal Desktop Entry (for all Linux application menus)
echo "Creating desktop shortcut..."
sudo bash -c 'cat > /usr/share/applications/mindful-tube.desktop << 'DESKTOP'
[Desktop Entry]
Name=MindfulTube
Comment=Distraction-free YouTube player
Exec=mindful-tube
Icon=mindful-tube
Terminal=false
Type=Application
Categories=AudioVideo;Player;
DESKTOP'

# 6. Refresh desktop database
if command -v update-desktop-database &> /dev/null; then
    sudo update-desktop-database -q
fi

echo "MindfulTube installed universally and successfully!"
