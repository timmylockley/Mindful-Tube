#!/bin/bash
set -e

# Repository configuration
REPO_USER="timmylockley"
REPO_NAME="Mindful-Tube"
BRANCH="main"

SCRIPT_URL="https://raw.githubusercontent.com/${REPO_USER}/${REPO_NAME}/${BRANCH}/mindful_tube.py"
ICON_URL="https://raw.githubusercontent.com/${REPO_USER}/${REPO_NAME}/${BRANCH}/mindful-tube.png"

echo "=== MindfulTube Universal Installer ==="

# 1. Check for Python 3 and pip
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed." >&2
    exit 1
fi

# 2. Install PyInstaller if not present
if ! command -v pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip3 install --user pyinstaller
    export PATH="$HOME/.local/bin:$PATH"
fi

# 3. Create a temporary working workspace
WORK_DIR=$(mktemp -d)
cd "$WORK_DIR"
echo "Downloading source files from GitHub..."

# 4. Pull the script and icon directly from your repository
curl -sSL "$SCRIPT_URL" -o mindful_tube.py
curl -sSL "$ICON_URL" -o mindful-tube.png

if [ ! -f "mindful_tube.py" ]; then
    echo "Error: Failed to download mindful_tube.py from GitHub." >&2
    exit 1
fi

# 5. Compile into a standalone executable using PyInstaller
echo "Compiling application executable..."
pyinstaller --onefile --windowed mindful_tube.py

# 6. Install globally onto the system
echo "Installing application files system-wide..."
sudo mkdir -p /usr/local/share/mindful-tube
sudo mkdir -p /usr/local/bin
sudo mkdir -p /usr/share/pixmaps

sudo cp dist/mindful_tube /usr/local/bin/mindful-tube
sudo cp mindful-tube.png /usr/share/pixmaps/mindful-tube.png

# 7. Create system-wide Desktop Menu Shortcut
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

# 8. Refresh Desktop Database
if command -v update-desktop-database &> /dev/null; then
    sudo update-desktop-database -q
fi

# Clean up temporary files
cd ~
rm -rf "$WORK_DIR"

echo "=== Installation Complete! MindfulTube is ready to use. ==="
