# discord-devros: Discord Bot for AI Queries
This is a Discord bot that integrates with OpenWebUI to query AI models. It allows users to interact with the AI directly on Discord, making use of the `ask` command to send queries to your OpenWebUI server and receive responses. The bot also provides an easy-to-use interface for setting up and interacting with AI models in Discord servers.

# Packaging File Structure

```
/discord-devros/
├── bin/                        # Folder for executables
│   └── start_bot               # File should be executable and contain code to run bot.py
├── lib/                        # Folder for libraries (if any)
├── share/                      # Folder for data files 
│   └── discord_devros/         # This is where your Python scripts will reside
│      ├── commands/            # Command-specific code
│      │   ├── __init__.py      # Imports commands
│      │   └── ask.py           # Ask command logic
│      ├── __init__.py          # Imports Discord bot files
│      ├── bot.py               # Main bot script
│      └── utils.py             # Helper functions
├── etc/                        # Configuration files
│   └── discord_devros/         # Stores configuration for the bot
│      ├── .env                 # Sensitive data (not committed)
│      └── settings.json        # Configuration settings (command prefix, model name, etc.)
├── DEBIAN/                     # Folder for package metadata
│   ├── control                 # Package metadata file
│   ├── postinst                # Post installation script 
│   ├── prerm                   # Pre-removal script (optional)
│   ├── postrm                  # Post-removal script (optional)
│   ├── preinst                 # Pre-installation script (optional)
├── .gitignore                  # Prevents sensitive files from being committed
├── README.md                   # This file
└── requirements.txt            # Python dependency list 
```

## Features
- **Discord Bot Integration**: A fully functioning Discord bot that interacts with users on your server.
- **AI Queries**: Uses the `ask` command to send user questions to an OpenWebUI instance running on your Raspberry Pi.
- **Modular Command System**: Easily extend the bot by adding new commands or modifying the existing ones.

## Requirements
- A Raspberry Pi with Raspbian OS (or another compatible OS).
- Python 3.6+ installed on the Raspberry Pi.
- OpenWebUI server already set up and running. If you haven’t set up OpenWebUI yet, follow the [OpenWebUI setup guide](https://github.com/OpenWebUI/OpenWebUI) to get started.
- Access to your Raspberry Pi's terminal (either directly or through SSH).
- A Discord bot token (you can create one by following the [Discord Developer Documentation](https://discord.com/developers/docs/intro)).

## Setup Instructions

### 1. Clone the Repository
- First, clone the repository from GitHub onto your Raspberry Pi:
```bash
git clone git@github.com:GuamBoi/discord-devros.git
cd discord-devros
```

### 2. Install Dependencies
This bot uses several Python libraries that need to be installed. You will install them in a virtual environment for isolation:
1. **Create and activate a virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate
```
  
2. **Install the required dependencies**:
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
The bot requires certain environment variables to run, such as your Discord bot token and OpenWebUI server details. You can store these securely in a `.env` file.

1. **Edit the `.env` file** in the `etc/discord-devros/` directory:
```bash
nano etc/discord-devros/.env
```

2. **Add your environment variables**:
	- Open the `.env` file in a text editor and add the following, replacing with your actual information:
```text
DISCORD_BOT_TOKEN="your_discord_bot_token"
OPEN_WEBUI_API_KEY="your_openwebui_api_key"
OPEN_WEBUI_API_URL="http://localhost:8080/v1/chat/completions"  # Replace with your OpenWebUI API URL
```
 > Replace `your_discord_bot_token` with the token you obtained when creating your Discord bot.
> Replace `your_openwebui_api_key` with the API key for your OpenWebUI instance.
> Adjust the `OPEN_WEBUI_API_URL` if your OpenWebUI server is hosted on a different IP or port.

### 4. Configure the Bot
- You can customize some bot settings via the `settings.json` file. For example, you can change the bot's command prefix and the model name used by OpenWebUI.
1. **Create the `settings.json` file** in the `etc/discord-devros/` directory:
```bash
nano etc/discord-devros/settings.json
```

2. **Edit the `settings.json` file** to include your preferences:
```json
{
"command_prefix": "?",
"openwebui_model_name": "devros-mini",
"max_message_length": 2000
}
```
- `command_prefix`: The prefix used for bot commands (e.g., `?ask What is AI?`).
- `openwebui_model_name`: The model to query on OpenWebUI (make sure it's available).
- `max_message_length`: The maximum length of a message before it gets truncated.

### 5. Run the Bot
To start the bot, you can run the `start_bot` script, which activates the virtual environment and starts the bot.

1. **Make the script executable**:
```bash
chmod +x bin/start_bot
```

- You can now run the bot by executing the following commands:
```bash
cd ~/discord-devros/share/discord-devros
source ~/discord-devros/venv/bin/activate
python3 bot.py
```
### 6. Additional Configuration
- The bot's configuration, including custom commands and logic, can be found in the `share/discord-devros/commands/` and `share/discord-devros/utils.py` files. You can modify these to add new commands or alter existing ones. The main bot logic is located in `share/discord-devros/bot/bot.py`.
- If you want to add more commands, you can create new Python files in the `commands/` directory and import them in `share/discord-devros/commands/__init__.py`.

### 7. Troubleshooting
- **Bot not starting?** Double-check that your `.env` file contains the correct values and that the virtual environment is activated.
- **API issues?** Ensure that your OpenWebUI server is running and accessible at the URL specified in the `.env` file.
- **Bot is unresponsive?** Check the logs for any errors, and ensure that the necessary intents are enabled on the Discord Developer Portal.

### 8. Uninstallation
- If you want to uninstall the bot, you can run the following:
1. Deactivate the virtual environment:
```bash
deactivate
```
2. Remove the bot directory:
```bash
rm -rf discord-devros
```
- You can also use `dpkg` if you packaged it into a `.deb` file.
