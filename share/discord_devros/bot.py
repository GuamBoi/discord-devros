import logging
import os
import json
from discord.ext import commands
from discord import Intents 
import sys
import getpass  # Import getpass to get the username of the logged-in user
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load environment variables from the .env file
load_dotenv()

# Get the logged-in user's username
USER_NAME = getpass.getuser()

# Append the path to the `discord_devros` module
sys.path.append(f'/home/{USER_NAME}/discord-devros/share/discord_devros')

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

# Bot setup
base_dir = os.path.dirname(os.path.abspath(__file__))

# Load settings
settings_path = os.path.join(base_dir, "settings.json")
if os.path.exists(settings_path):
    with open(settings_path, "r") as f:
        settings = json.load(f)
else:
    settings = {}

command_prefix = settings.get("command_prefix")
disabled_commands = settings.get("disabled_commands", [])

# Configure intents
intents = Intents.default()  # Enable the default set of intents. You can customize further if needed.
intents.messages = True  # Example of enabling a specific intent (message events)

bot = commands.Bot(command_prefix=command_prefix, intents=intents)

async def load_commands():
    """Loads all command extensions in the bot."""
    commands_folder = os.path.join(base_dir, "commands")  # Correct path
    logging.info(f"Commands folder path: {commands_folder}")  # Add this line to debug
    command_files = [f[:-3] for f in os.listdir(commands_folder) if f.endswith(".py") and f != "__init__.py"]
    
    failed_commands = []

    async def load_command(command):
        if command in disabled_commands:
            logging.info(f"Skipping disabled command: {command}")
            return
        try:
            await bot.load_extension(f"commands.{command}")
            logging.info(f"Successfully loaded command: {command}")
        except Exception as e:
            logging.error(f"Failed to load command {command}: {e}")
            failed_commands.append(command)
            traceback.print_exc()
    
    await asyncio.gather(*(load_command(cmd) for cmd in command_files))
    
    if failed_commands:
        logging.warning(f"Some commands failed to load: {', '.join(failed_commands)}")

# Run bot
if __name__ == "__main__":
    # Get the bot token from the environment variables
    bot_token = os.getenv("DISCORD_BOT_TOKEN")

    # Start the bot
    if bot_token:
        bot.run(bot_token)  # Make sure to use the correct token variable
    else:
        logging.error("No bot token found. Make sure to set the DISCORD_BOT_TOKEN in your .env file.")
