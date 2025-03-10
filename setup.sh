#!/bin/bash
set -e  # Exit on error

echo "Building the .deb package..."
dpkg --build discord-devros

echo "Installing the package..."
sudo dpkg -i discord-devros.deb

echo "Setup complete! Starting the bot..."
/usr/bin/start_bot
