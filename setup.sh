#!/bin/bash
set -e  # Exit on error

# Get the logged-in user's username
USER_NAME=$(whoami)

# Set up the bot directory
BOT_DIR="/home/$USER_NAME/discord-devros"
VENV_DIR="$BOT_DIR/venv"

# Ensure the repository is cloned and available
if [ ! -d "$BOT_DIR" ]; then
    echo "Error: $BOT_DIR does not exist. Please clone the repository first using:"
    echo "  git clone https://github.com/GuamBoi/discord-devros.git"
    exit 1
fi

# Install system dependencies (git, dpkg, python3, python3-venv)
echo "Installing necessary system dependencies..."
sudo apt update
sudo apt install -y git dpkg python3 python3-venv build-essential devscripts debhelper fakeroot
pip install -r "$BOT_DIR/requirements.txt"

# Set up a Python virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating a Python virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip inside the virtual environment
pip install --upgrade pip

# Install Python dependencies listed in requirements.txt
echo "Installing Python dependencies from requirements.txt inside virtual environment..."
pip install -r "$BOT_DIR/requirements.txt"

# Deactivate virtual environment
deactivate

# Update permissions for the control file, preinst, postinst, postrm, and prerm scripts
echo "Updating permissions for control, preinst, postinst, postrm, and prerm scripts..."
chmod 755 "$BOT_DIR/DEBIAN/control"
chmod 755 "$BOT_DIR/DEBIAN/preinst"
chmod 755 "$BOT_DIR/DEBIAN/postinst"
chmod 755 "$BOT_DIR/DEBIAN/postrm"
chmod 755 "$BOT_DIR/DEBIAN/prerm"

# Set the working directory to the bot's root directory
cd "$BOT_DIR" || exit 1

# Build the .deb package (if necessary)
echo "Building the .deb package..."
dpkg-deb --build --root-owner-group . ../discord-devros.deb

# Install the package
echo "Installing the package..."
sudo dpkg -i ../discord-devros.deb

# Handle missing dependencies after installation
echo "Fixing broken packages (if any)..."
sudo apt --fix-broken install

# Set proper permissions for bot files
echo "Setting correct file permissions..."
sudo chown -R "$USER_NAME:$USER_NAME" "$BOT_DIR"
chmod +x "$BOT_DIR/bin/start_bot"

# Set permissions for Python scripts in the commands directory
find "$BOT_DIR/share/commands/" -type f -name "*.py" -exec chmod +x {} \;

# Set up proper permissions for log files (if necessary)
LOG_FILE="$BOT_DIR/var/log/bot.log"
if [ ! -f "$LOG_FILE" ]; then
    sudo touch "$LOG_FILE"
fi
sudo chown "$USER_NAME:$USER_NAME" "$LOG_FILE"
sudo chmod 664 "$LOG_FILE"

# Check if start_bot command is available and start the bot
echo "Setup complete! Starting the bot..."

# Activate virtual environment and start the bot
source "$VENV_DIR/bin/activate"
python3 "$BOT_DIR/bin/start_bot"
deactivate
