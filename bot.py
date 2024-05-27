import os
import sys
import discord
import logging
import asyncio
from discord.ext.commands import Bot
from datetime import datetime as dt

# Set up directory structure
CWD = os.getcwd()
DIR_INCLUDES = os.path.join(CWD, "includes")
CONFIG_FILE = os.path.join(DIR_INCLUDES, "config.py")
DIR_LOGS = os.path.join(CWD, "logs")
os.makedirs(DIR_LOGS, exist_ok=True)
DIR_COGS = os.path.join(CWD, "cogs")

# Configure logging
logging.basicConfig(
    filename=os.path.join(DIR_LOGS, 'app.log'),
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Logging function
def log(message, level=logging.INFO):
    formatted_message = logging.getLogger('').handlers[0].format(
        logging.makeLogRecord(
            {'msg': message, 'levelname': logging.getLevelName(level)}
        )
    )
    print(formatted_message)
    {
        logging.WARNING: lambda: logging.warning(message),
        logging.ERROR: lambda: logging.error(message)
    }.get(level, lambda: logging.info(message))()

# Import configuration
if not os.path.isfile(CONFIG_FILE):
    log(f"'{CONFIG_FILE}' not found, exiting", logging.ERROR)
    sys.exit()
else:
    from includes import config

# Initialize bot
intents = discord.Intents.all()
bot = Bot(command_prefix=config.BOT_PREFIX, intents=intents)
bot.remove_command("help")

# Load all cogs dynamically
async def loadcogs():
    for filename in os.listdir(DIR_COGS):
        if filename.endswith('.py') and not filename.startswith('_'):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f'cogs.{cog_name}')
            except Exception as e:
                log(f"Failed to load cog '{cog_name}': {str(e)}", logging.ERROR)

# Command dispatch
@bot.event
async def on_message(message):
    if message.author is bot.user:
        return
    await bot.process_commands(message)

# Run bot
async def main():
    async with bot:
        await loadcogs()
        log("Waiting for the bot to be ready...")
        await bot.start(config.BOT_SECRETS_TOKEN)

asyncio.run(main())