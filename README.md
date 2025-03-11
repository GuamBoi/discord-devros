# discord-devros: Discord Bot for AI Queries
This is a Discord bot that integrates with OpenWebUI to query AI models. It allows users to interact with the AI directly on Discord, making use of the `ask` command to send queries to your OpenWebUI server and receive responses. The bot also provides an easy-to-use interface for setting up and interacting with AI models in Discord servers.

# Packaging File Structure

```
/discord-devros/
├── bin/                     # Folder for executables
│   └── start_bot            # Executable / runs bot.py
|
├── var/                     # Folder for data files 
│   └── log/                 # Log folder
│      └── bot.log           # Error log file
│
├── share/                   # Folder for data files 
│   └── discord_devros/      # This is where Python scripts reside
│      ├── commands/         # Command-specific code
│      │   ├── __init__.py   # Imports commands
│      │   └── ask.py        # Ask command logic
│      ├── __init__.py       # Imports Discord bot files
│      ├── bot.py            # Main bot script
│      └── utils.py          # Helper functions
│
├── etc/                     # Configuration files
│   └── discord_devros/      # Stores configuration for the bot
│      ├── .env              # Sensitive data (not committed)
│      └── settings.json     # Configuration settings
│
├── DEBIAN/                  # Folder for package metadata
│   ├── control              # Package metadata file
│   ├── postinst             # Post installation script 
│   ├── prerm                # Pre-removal script
│   ├── postrm               # Post-removal script
│   └── preinst              # Pre-installation script
│
├── .gitignore               # Prevents sensitive files being committed
├── README.md                # This file
├── requirements.txt         # Python dependency list 
└── setup.sh                 # Sets up the Bot environment properly
```

## Features
- **Discord Bot Integration**: A fully functioning Discord bot that interacts with users on your server.
- **AI Queries**: Uses the `ask` command to send user questions to an OpenWebUI instance running on your Raspberry Pi.
- **Modular Command System**: Easily extend the bot by adding new commands or modifying the existing ones.

### Prerequisites:

1. **Ensure your Raspberry Pi is set up**:
    
    - Running Raspbian OS (or another compatible OS).
    - Python 3.6+ installed.
    - OpenWebUI server already set up and running.
    - A Discord bot token (you can create one on [Discord Developer Portal](https://discord.com/developers/docs/intro)).
2. **Access your Raspberry Pi terminal** (via SSH or directly).

---

### Step-by-Step Installation Guide:

#### 1. **Clone the Repository**

First, clone your `discord-devros` repository from GitHub:

```bash
git clone https://github.com/GuamBoi/discord-devros.git
cd discord-devros
```

#### 2. **Configure the Bot**

You need to configure a few settings:

1. **Set up the environment variables** for your Discord bot and OpenWebUI. Create the `.env` file:

```bash
sudo nano /etc/discord_devros/.env
```

2. Add the following to the `.env` file (replacing with your actual values):

```bash
DISCORD_BOT_TOKEN="your_discord_bot_token"
OPEN_WEBUI_API_KEY="your_openwebui_api_key"
OPEN_WEBUI_API_URL="http://localhost:8080/v1/chat/completions"  # Adjust if necessary
```

3. **Configure the bot settings** by editing the `settings.json`:

```bash
sudo nano /etc/discord_devros/settings.json
```

4. Add your desired settings, such as the bot's command prefix and the OpenWebUI model name:

```json
{
  "command_prefix": "?",
  "openwebui_model_name": "devros-mini",
  "max_message_length": 2000
}
```

#### 3. Make the `setup.sh` file executable, and run it:
1. Make the script executable:

	```shell
	chmod +x setup.sh
	```

2. Run the setup script:

	```
	./setup.sh
	```

---

### Troubleshooting:

- **Bot not starting**: Double-check your `.env` file and ensure the virtual environment is activated.
- **API issues**: Make sure your OpenWebUI server is running and accessible.
- **Bot unresponsive**: Check the bot logs (`/lib/bot.log`) for any errors.

