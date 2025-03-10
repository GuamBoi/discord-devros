#!/bin/bash
set -e  # Exit on error

# Get the logged-in user's username
USER_NAME=$(whoami)

# Set up the bot directory
BOT_DIR="/opt/discord-devros"

# Ensure the repository is cloned and available
if [ ! -d "$BOT_DIR" ]; then
    echo "Error: $BOT_DIR does not exist. Please clone the repository first using \`git clone https://github.com/GuamBoi/discord-devros.git\`"
    exit 1
fi

# Install system dependencies (git, dpkg, python3, python3-pip)
echo "Installing necessary system dependencies..."
sudo apt update
sudo apt install -y git dpkg python3 python3-pip

# Install Python dependencies listed in requirements.txt
echo "Installing Python dependencies from requirements.txt..."
cd "$BOT_DIR"
pip3 install --upgrade -r requirements.txt

# Build the .deb package
echo "Building the .deb package..."
dpkg --build "$BOT_DIR"

# Install the package
echo "Installing the package..."
sudo dpkg -i "$BOT_DIR/discord-devros.deb"

# Handle missing dependencies after installation
echo "Fixing broken packages (if any)..."
sudo apt --fix-broken install

# Set proper permissions for bot files
echo "Setting correct file permissions..."

# Ensure the bot directory and its contents are owned by the current user
sudo chown -R $USER_NAME:$USER_NAME "$BOT_DIR"

# Set the correct permissions for executable scripts
chmod +x "$BOT_DIR/bin/start_bot"

# Set permissions for Python scripts in the commands directory
find "$BOT_DIR/share/commands/" -type f -name "*.py" -exec chmod +x {} \;

# Set up proper permissions for log files (if necessary)
LOG_FILE="/home/$USER_NAME/discord-devros/var/log/bot.log"
if [ ! -f "$LOG_FILE" ]; then
    sudo touch "$LOG_FILE"
fi

# Set the correct permissions for the log file
sudo chown $USER_NAME:$USER_NAME "$LOG_FILE"
sudo chmod 664 "$LOG_FILE"

# Check if start_bot command is available and start the bot
echo "Setup complete! Starting the bot..."
if command -v start_bot &> /dev/null
then
    echo "Starting bot using the start_bot command..."
    start_bot
else
    echo "start_bot command not found! Checking default path..."
    if [ -f "/usr/local/bin/start_bot" ]; then
        echo "Found start_bot in /usr/local/bin, starting bot..."
        /usr/local/bin/start_bot
    else
        echo "start_bot not found in any expected locations."
        echo "Please make sure the bot installation includes the start_bot command."
        exit 1
    fi
fi
