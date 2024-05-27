import os
import sys
import logging
import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime as dt

# Set up directory structure
CWD = os.getcwd()
DIR_INCLUDES = os.path.join(CWD, "includes")
DIR_COGS = os.path.join(CWD, "cogs")
DIR_LOGS = os.path.join(CWD, "logs")
CONFIG_FILE = os.path.join(DIR_INCLUDES, "config.py")
os.makedirs(DIR_LOGS, exist_ok=True)

# Set up logging
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

# Cog class
class QR(commands.Cog, name="qr"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="qr")
    async def my_command(self, context, *, msg):
        """
        Generates a QR code from entered text.
        """
        qrobj = pyqrcode.create(msg)
        qrobj.png('qr.png', scale=8)
        await context.send(file=discord.File('qr.png'))
        os.remove("qr.png")

# Cog setup function
async def setup(bot):
    cog = QR
    try:
        await bot.add_cog(cog(bot))
        log(f"{cog.__name__} has been loaded successfully.")
    except Exception as e:
        log(f'Failed to load {cog.__name__}: {str(e)}', level=logging.ERROR)
